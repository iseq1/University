import numpy as np

from orb_keypoint_descriptors_class import *


class ObjectFinder(KeypointDescriptor):
    def __init__(self):
        super().__init__()
        self.image1, self.image2 = None, None
        self.image1_array, self.image2_array = None, None
        self.image1_gray, self.image2_gray = None, None
        self.image1_gray_array, self.image2_gray_array = None, None

    def scale(self, image, s_resized):
        """
        img = np.array([[1, 2, 3, 4],
                        [5, 6, 7, 8],
                        [9, 10, 11, 12],
                        [13, 14, 15, 16]])

        array([[3, 5],
               [11, 13]])
        """
        w = image.shape[0]
        h = image.shape[1]

        newI = np.zeros((w // s_resized, h // s_resized), dtype=int)

        for i in range(0, w // s_resized):
            for j in range(0, h // s_resized):
                newI[i, j] = int(np.mean(image[i * s_resized:s_resized * (i + 1), j * s_resized:s_resized * (j + 1)]))

        return newI

    def set_images(self, image1_path, image2_path):
        image1 = Image.open(image1_path)
        image2 = Image.open(image2_path)
        self.image1 = image1
        self.image2 = image2
        self.image1_array = np.array(image1)
        self.image2_array = np.array(image2)

    def get_images(self, file_path):
        '''
        Показываю оригинальную картинку
        :return:
        '''
        plt.figure(figsize=(10, 5))
        plt.subplot(1, 2, 1)
        plt.title("box")
        plt.imshow(self.image1, cmap='gray')

        plt.subplot(1, 2, 2)
        plt.title("box_in_scene")
        plt.imshow(self.image2, cmap='gray')
        plt.savefig(f'{file_path}', bbox_inches='tight')
        plt.show()

    def get_hamming_distance(self, desc1, desc2):
        return sum(np.absolute(desc1-desc2))

    def set_hamming_matrix(self, desc_box, desc_box_in_scene):
        """
        Создаёт матрицу расстояний Хэмминга для двух наборов ключевых точек.

        каждая строка соответствует точке из первого изображения, а каждая колонка — точке из второго изображения:
        пересечение строки и столбца = расстояние между i точкой 1 изо. и j точкой 2 изо.
        """
        count_desc_box = len(desc_box)
        count_desc_bis = len(desc_box_in_scene)
        hamming_matrix = np.zeros((count_desc_box, count_desc_bis), dtype=int)

        for i in range(count_desc_box):
            for j in range(count_desc_bis):

                desc1 = desc_box[i]
                desc2 = desc_box_in_scene[j]
                hamming_matrix[i, j] = self.get_hamming_distance(np.array(desc1), np.array(desc2))

        return hamming_matrix

    def get_hamming_matrix(self):
        box_img_data = self.load_keypoints_data_from_file('box_keypoints_full_data.json')
        box_in_scene_img_data = self.load_keypoints_data_from_file('box_in_scene_keypoints_full_data.json')

        box_descriptors = [_dict["descriptor"] for _dict in box_img_data["0"]]
        box_in_scene_descriptors = [_dict["descriptor"] for _dict in box_in_scene_img_data["0"]]

        return self.set_hamming_matrix(box_descriptors, box_in_scene_descriptors)

    def set_lower_test(self, points_1, points_2, hamming_matrix, R_Lowe = 0.8):
        height, width = hamming_matrix.shape
        force_matches, reverse_matches = [], []

        for i in range(height):
            distance = sorted(hamming_matrix[i])
            for t in range(len(distance)-1):
                nearest, second_nearest = distance[t:t+2]
                ratio = nearest / second_nearest
                if ratio < R_Lowe:
                    index_match = list(hamming_matrix[i]).index(nearest)
                    force_matches.append([points_1[i], points_2[index_match]])
                    break

        for i in range(width):
            distance = sorted(hamming_matrix[:, i])
            for t in range(len(distance)-1):
                nearest, second_nearest = distance[t:t + 2]
                ratio = nearest / second_nearest
                if ratio < R_Lowe:
                    index_match = list(hamming_matrix[:, i]).index(nearest)
                    reverse_matches.append([points_1[index_match], points_2[i]])
                    break

        return [force_matches, reverse_matches]

    def get_lower_test(self):
        box_img_data = self.load_keypoints_data_from_file('box_keypoints_full_data.json')
        box_in_scene_img_data = self.load_keypoints_data_from_file('box_in_scene_keypoints_full_data.json')

        box_keypoints = [_dict["keypoint"] for _dict in box_img_data["0"]]
        box_in_scene_keypoints = [_dict["keypoint"] for _dict in box_in_scene_img_data["0"]]

        return self.set_lower_test(box_keypoints, box_in_scene_keypoints, self.get_hamming_matrix())

    def set_cross_test(self, lowe_test_result):
        filtered_points1 = []
        filtered_points2 = []

        # Верхний цикл - прямые соответствия
        for i in range(len(lowe_test_result[0])):
            point1, point2 = lowe_test_result[0][i]  # точки прямого соответствия

            # Эта же пара в обратных соответствиях
            for j in range(len(lowe_test_result[1])):
                point1_reverse, point2_reverse = lowe_test_result[1][j]

                # В обоих направлениях есть эта пара
                if point1 == point1_reverse and point2 == point2_reverse:
                    filtered_points1.append(point1)
                    filtered_points2.append(point2)
                    break

        return [filtered_points1, filtered_points2]

    def get_cross_test(self):
        return self.set_cross_test(self.get_lower_test())

    def bresenham(self, x0, y0, x1, y1, max_size):

        dx = abs(x1 - x0)
        dy = abs(y1 - y0)

        step_x = 1 if x0 < x1 else -1
        step_y = 1 if y0 < y1 else -1

        error = dx - dy

        line_points = []
        x, y = x0, y0

        while True:
            if 0 <= x < max_size and 0 <= y < max_size:
                line_points.append([x, y])

            if x == x1 and y == y1:
                break

            error2 = error * 2

            if error2 > -dy:
                error -= dy
                x += step_x

            if error2 < dx:
                error += dx
                y += step_y

        return line_points

    def draw(self, image, points, color=[0, 0, 255]):

        height, width = image.shape

        result_image = np.zeros((height, width, 3), dtype=int)

        for i in range(height):
            for j in range(width):
                result_image[i, j, :] = image[i, j]

        for center_x, center_y in points:
            result_image[center_x - 1:center_x + 2, center_y - 3] = color

            result_image[center_x + 2, center_y - 2] = color

            result_image[center_x + 3, center_y - 1:center_y + 2] = color

            result_image[center_x + 2, center_y + 2] = color

            result_image[center_x - 1:center_x + 2, center_y + 3] = color

            result_image[center_x - 2, center_y + 2] = color

            result_image[center_x - 3, center_y - 1:center_y + 2] = color

            result_image[center_x - 2, center_y - 2] = color

        return result_image

    def set_visualize_matches(self, image1, image2, points1, points2):

        img1_with_points = self.draw(image1, points1)
        img2_with_points = self.draw(image2, points2)

        # Размеры для объединенного изображения
        total_width = img1_with_points.shape[1] + img2_with_points.shape[1]
        height = img2_with_points.shape[0]
        width2 = img2_with_points.shape[1]

        result = np.ones((height, total_width, 3), dtype=int) * 255

        result[0:img2_with_points.shape[0], 0:width2] = img2_with_points
        result[0:img1_with_points.shape[0], width2:] = img1_with_points

        color = [0, 0, 255]
        for i in range(len(points1)):
            x1, y1 = points1[i]
            y1 += width2
            x2, y2 = points2[i]

            line_points = self.bresenham(x1, y1, x2, y2, total_width)

            for x, y in line_points:
                result[x, y] = color

        return result

    def get_visualize_matches(self, file_path):
        target_keypoint_1, target_keypoint_2 = self.get_cross_test()
        result = self.set_visualize_matches(self.image1_array, self.image2_array, target_keypoint_1, target_keypoint_2)
        plt.figure(figsize=(10, 8))
        plt.imshow(result, vmin=0, vmax=255)
        plt.savefig(f'{file_path}', bbox_inches='tight')
        plt.show()

    def get_affine_transformation_parameters(self, src_points, dst_points):
        """

        src_points - три точки исходного изображения [(x1,y1), (x2,y2), (x3,y3)]
        dst_points - три соответствующие точки целевого изображения [(u1,v1), (u2,v2), (u3,v3)]

        T - вектор переноса
        M - матрица поворота и масштаба
        """

        src = np.array(src_points)  # исходные точки
        dst = np.array(dst_points)  # целевые точки

        x1, y1 = src[0]
        x2, y2 = src[1]
        x3, y3 = src[2]

        u1, v1 = dst[0]
        u2, v2 = dst[1]
        u3, v3 = dst[2]

        # определитель первой матрицы
        det1 = (x1 - x3) * (y1 - y2) - (x1 - x2) * (y1 - y3)
        # определитель второй матрицы
        det2 = y1 - y2

        if abs(det1) < 1e-10 or abs(det2) < 1e-10:
            return None, None

        # [u] = [m1 m2] [x] + [tx]
        # [v] = [m3 m4] [y] + [ty]

        # u = m1*x + m2*y + tx
        # v = m3*x + m4*y + ty

        # Для каждой u (пример):
        # u1 = m1*x1 + m2*y1 + tx
        # u2 = m1*x2 + m2*y2 + tx
        # u3 = m1*x3 + m2*y3 + tx

        # Метод Крамера
        # (1)-(3): u1-u3 = m1(x1-x3) + m2(y1-y3)
        # (1)-(2): u1-u2 = m1(x1-x2) + m2(y1-y2)

        # Матрица коэффициентов
        # A1 = | u1-u3  y1-y3 |
        #      | u1-u2  y1-y2 |

        # Нахождение неизвестной
        # m1 = ((u1-u3)(y1-y2) - (u1-u2)(y1-y3)) / det1

        try:
            m1 = ((u1 - u3) * (y1 - y2) - (u1 - u2) * (y1 - y3)) / det1
            m2 = ((u1 - u2) - m1 * (x1 - x2)) / det2
            tx = u1 - m1 * x1 - m2 * y1

            m3 = ((v1 - v3) * (y1 - y2) - (v1 - v2) * (y1 - y3)) / det1
            m4 = ((v1 - v2) - m3 * (x1 - x2)) / det2
            ty = v1 - m3 * x1 - m4 * y1

            M = np.array([[m1, m2], [m3, m4]])
            T = np.array([tx, ty])

            return M, T

        except:
            return None, None

    def Affine_transformation(self, points, M, T):

        M = np.array(M)
        T = np.array(T)
        points = np.array(points)

        x = points[:, 0]
        y = points[:, 1]

        # x' = m11*x + m12*y + tx
        # y' = m21*x + m22*y + ty
        x_new = M[0][0] * x + M[0][1] * y + T[0]
        y_new = M[1][0] * x + M[1][1] * y + T[1]

        # Преобразованные координаты -> массив точек
        return np.column_stack((x_new, y_new))

    # Оценка параметров афинного преобразования методом наименьших квадратов
    def MNK(self, points):
        """
        Система уравнений для каждой пары точек (x,y) -> (u,v):
        u = m1*x + m2*y + tx
        v = m3*x + m4*y + ty

        Матричная форма A*X = B
        A = [x y 0 0 1 0] для u
            [0 0 x y 0 1] для v
        X = [m1 m2 m3 m4 tx ty]^T
        B = [u v]^T
        """
        if len(points) < 3:
            print("Недостаточно точек")
            return None, None

        A = []  # матрица коэффициентов
        B = []  # вектор значений
        for (x, y), (u, v) in points:
            # Уравнение для u
            A.append([x, y, 0, 0, 1, 0])
            B.append(u)
            # Уравнение для v
            A.append([0, 0, x, y, 0, 1])
            B.append(v)

        A = np.array(A, dtype=np.float64)
        # Массив [u1,v1,u2,v2,...] -> столбец [[u1],[v1],[u2],[v2],...]
        B = np.array(B, dtype=np.float64).reshape(-1, 1)

        # Решение МНК: X = (A^T * A)^(-1) * A^T * B
        X = np.linalg.inv(A.T @ A) @ A.T @ B

        # матрица M и вектор T
        M = X[0:4].reshape(2, 2)
        T = X[4:6].reshape(2, 1)

        return M, T

    def RANSAC(self, points1, points2, num_iterations=5, distance_threshold=2):
        """
        points1, points2 - соответствующие точки двух изображений
        num_iterations: количество итераций
        distance_threshold: порог
        """
        min_points = 3  # минимальное количество точек для аффинного преобразования

        # Проверка количества точек
        if len(points1) < min_points:
            return None, None

        # Инициализация лучших параметров
        best_inliers_count = -1
        total_points = len(points1)
        best_matching_points = []
        best_transform_matrix = None
        best_translation = None

        try:
            # Цикл N итераций
            for _ in range(num_iterations):

                # Случайное множество сопоставленных точек (по минимальному количеству)
                random_indices = random.sample(range(len(points1)), min_points)
                sample_points1 = [points1[i] for i in random_indices]
                sample_points2 = [points2[i] for i in random_indices]

                # Оценка параметров через СЛАУ
                transform_matrix, translation = self.get_affine_transformation_parameters(
                    sample_points1, sample_points2
                )
                if transform_matrix is None or translation is None:
                    continue

                # Преобразование точек
                transformed_points = self.Affine_transformation(points1, transform_matrix, translation)

                # Подсчет верных соответствий (inliers)
                current_matching_points = []
                inliers_count = 0

                # Нахождение не-выбросов (inliers) по порогу расстояния
                for idx in range(len(points2)):
                    x_transformed, y_transformed = transformed_points[idx]
                    x_target, y_target = points2[idx]

                    # Проверка расстояния
                    if (abs(x_transformed - x_target) < distance_threshold and
                            abs(y_transformed - y_target) < distance_threshold):
                        x_source, y_source = points1[idx]
                        inliers_count += 1
                        # Пара точек исходная -> целевая
                        current_matching_points.append([[x_source, y_source],
                                                        [x_target, y_target]])

                # Обновление лучшего результата
                # Все точки совпали - идеальный случай
                if inliers_count == total_points:
                    best_matching_points = current_matching_points
                    best_transform_matrix = transform_matrix
                    best_translation = translation
                    break

                # Обновление лучшего результата (если больше inliers)
                if inliers_count > best_inliers_count:
                    best_inliers_count = inliers_count
                    best_matching_points = current_matching_points
                    best_transform_matrix = transform_matrix
                    best_translation = translation

            # Финальное уточнение методом наименьших квадратов
            if best_matching_points:
                best_transform_matrix, best_translation = self.MNK(best_matching_points)

            print(f"M:\n{best_transform_matrix}\nT:\n{best_translation}")
            return best_transform_matrix, best_translation

        except Exception as e:
            print(f"Ошибка RANSAC: {str(e)}")
            return None, None

    def detect_query(self, box, scene, transform_matrix, translation):

        height, width = box.shape

        object_points = []
        for y in range(height):
            for x in range(width):
                object_points.append([y, x])

        transformed_points = self.Affine_transformation(
            object_points,
            transform_matrix,
            translation
        )

        polygon_points = np.array(transformed_points, dtype=int)

        if len(scene.shape) == 2:
            # Приведение к RGB
            result_scene = np.stack([scene] * 3, axis=-1)
        else:
            result_scene = scene.copy()

        scene_height, scene_width = result_scene.shape[:2]
        for point in polygon_points:
            y, x = point
            if 0 <= y < scene_height and 0 <= x < scene_width:
                result_scene[y, x] = [255, 0, 0]

        return result_scene

    def get_detected_img(self, M, T, file_path):

        detected_query = self.detect_query(self.image1_array, self.image2_array, M, T)

        plt.figure()
        plt.imshow(detected_query, cmap='gray', vmin=0, vmax=255)
        plt.savefig(f'{file_path}', bbox_inches='tight')
        plt.show()
