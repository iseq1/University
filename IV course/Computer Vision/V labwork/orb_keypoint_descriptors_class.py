import json

from hough_transform_class import *
import math


class KeypointDescriptor(HoughTransform):
    def __init__(self):
        super().__init__()
        self.keypoints = []
        self.keypoints_image = None
        self.filtered_keypoints_image = None
        self.harris_criteria = None
        self.filtered_keypoints_with_orient_image = None
        self.orientation, self.C, self.angle = None, None, None
        self.descriptors = None

    def check_fast_conditions(self, I, x, y):
        """Проверка последовательности для центральной точки (x, y) и порога t."""
        t = 30
        r = 3
        n = 12

        circle_points = [(3, 0), (3, 1), (2, 2), (1, 3), (0, 3), (-1, 3), (-2, 2), (-3, 1), (-3, 0), (-3, -1), (-2, -2),
                         (-1, -3), (0, -3), (1, -3), (2, -2), (3, -1)]
        # Проверяем 1,9 и 5,13 (пиксели для ускоренной проверки)
        points_to_check = [circle_points[i] for i in [0, 8, 4, 12]]
        result = []
        for dx, dy in points_to_check:
            px, py = x + dx, y + dy
            if not (0 <= px < I.shape[1] and 0 <= py < I.shape[0]):
                # continue
                return False
            if I[y, x] + t < I[py, px]:
                # Интенсивность больше -> 1
                result.append(1)
            elif I[y, x] - t > I[py, px]:
                # Интенсивность меньше -> -1
                result.append(-1)
            else:
                # Интенсивность ~такая же -> 0
                result.append(0)
        # если обозреваемая точка - ~контрольная: result -> [1, 1, 1, 0/-1] [0/-1, 1, 1, 1] [-1, -1, -1, 0/1] [0/1, -1, -1, -1]
        for i in range(2):
            # print(f'exampl: {result[i:i+3]} and sum is {sum(result[i:i+3])}')
            if sum(result[i:i + 3]) != 3 and sum(result[i:i + 3]) != -3:
                # print(f'exampl: {result[i:i + 3]} and sum is {sum(result[i:i + 3])}')
                return False

        # Проверяем последовательность из 12 пикселей
        result = []
        for i in range(16):
            dx, dy = circle_points[i]
            px, py = x + dx, y + dy
            if not (0 <= px < I.shape[1] and 0 <= py < I.shape[0]):
                continue
            if I[y, x] + t < I[py, px]:
                # Интенсивность больше -> 1
                result.append(1)
            elif I[y, x] - t > I[py, px]:
                # Интенсивность меньше -> -1
                result.append(-1)
            else:
                # Интенсивность ~такая же -> 0
                result.append(0)

        for i in range(5):
            if sum(result[i:i + 12]) != 12 and sum(result[i:i + 12]) != -12:
                return False

        return True

    def set_keypoint_detection(self, image):
        I = np.array(image)
        keypoints = []
        for y in range(3, I.shape[0] - 3):
            for x in range(3, I.shape[1] - 3):  #
                if self.check_fast_conditions(I, x, y):
                    keypoints.append((x, y))
        print(len(keypoints))
        return keypoints

    def get_keypoint_detection(self, file_path, image_to_work=None):
        self.keypoints = self.set_keypoint_detection(self.gray_image if image_to_work is None else image_to_work)

        self.keypoints_image = np.stack([self.gray_image_array if image_to_work is None else image_to_work] * 3,
                                        axis=-1)
        for (x, y) in self.keypoints:
            if 0 <= x < self.keypoints_image.shape[1] and 0 <= y < self.keypoints_image.shape[0]:
                self.keypoints_image[y, x] = [255, 0, 0]

        plt.figure(figsize=(10, 10))
        plt.imshow(self.keypoints_image)
        plt.axis('off')
        plt.savefig(f'{file_path}', bbox_inches='tight')
        plt.show()

    def set_harris_filtration(self, image_to_work=None):
        if self.grad_x is None and self.grad_y is None:
            # print(f"Я вхожу в set_harris_filtration сглаживать: {image_to_work}")
            self.get_blured_image(file_path="images/blured_image", image_to_work=image_to_work)
            self.get_gradient_n_magnitude(file_path=[
                'images/gradient_by_x_image',
                'images/gradient_by_y_image',
                'images/gradient_magnitude_image',
                'images/gradient_direction_image',
            ])

        R = []
        sigma = 1
        kernel_size = 5

        # w(x,y) - весовое окно
        gaussian_window = self.gaussian_kernel(sigma=sigma, size=kernel_size)

        for x, y in self.keypoints:
            x_min = max(0, x - kernel_size // 2)
            x_max = min(self.grad_x.shape[0], x + kernel_size // 2 + 1)
            y_min = max(0, y - kernel_size // 2)
            y_max = min(self.grad_y.shape[1], y + kernel_size // 2 + 1)

            window_x = self.grad_x[x_min:x_max, y_min:y_max]
            window_y = self.grad_y[x_min:x_max, y_min:y_max]
            gauss_weights = gaussian_window[:window_x.shape[0], :window_x.shape[1]]

            # элементы матрицы M - структурный тензор
            I_xx = np.sum(gauss_weights * (window_x ** 2))
            I_yy = np.sum(gauss_weights * (window_y ** 2))
            I_xy = np.sum(gauss_weights * (window_x * window_y))

            # Тот самый тензор
            M = np.array([[I_xx, I_xy],
                          [I_xy, I_yy]])

            det_M = (M[0][0] * M[1][1]) - (M[0][1] * M[1][0])
            trace_M = M[0][0] + M[1][1]
            k = 0.05
            r = det_M - k * (trace_M ** 2)
            R.append(r)

        return R

    def set_harris_criteria_filtering(self, image_to_work=None):
        # Тут выбрал разбить изображение на сетку и оставить в каждой сетке по M сильных точек
        img = self.gray_image_array if image_to_work is None else image_to_work
        self.harris_criteria = self.set_harris_filtration(img)
        M = 10
        grid_size = (8, 8)
        height, width = img.shape[:2]
        grid_height = height // grid_size[0]
        grid_width = width // grid_size[1]

        grid_cells = {}

        for point, r in zip(self.keypoints, self.harris_criteria):
            y, x = point
            grid_x = x // grid_width
            grid_y = y // grid_height
            cell = (grid_y, grid_x)

            if cell not in grid_cells:
                grid_cells[cell] = []

            grid_cells[cell].append((r, point))

        filtered_points = []
        for cell, points in grid_cells.items():
            points.sort(reverse=True, key=lambda x: x[0])  # сортируем по r
            filtered_points.extend([point for _, point in points[:M]])

        return filtered_points

    def get_harris_criteria_filtering(self, file_path, image_to_work=None):
        self.keypoints = self.set_harris_criteria_filtering(image_to_work)
        print(len(self.keypoints))
        self.filtered_keypoints_image = np.stack(
            [self.gray_image_array if image_to_work is None else image_to_work] * 3, axis=-1)
        for (x, y) in self.keypoints:
            if 0 <= x < self.filtered_keypoints_image.shape[1] and 0 <= y < self.filtered_keypoints_image.shape[0]:
                self.filtered_keypoints_image[y, x] = [255, 0, 0]

        plt.figure(figsize=(10, 10))
        plt.imshow(self.filtered_keypoints_image)
        plt.axis('off')
        plt.savefig(f'{file_path}', bbox_inches='tight')
        plt.show()

    def set_orientation_keypoints(self, image):
        orientations, C, angle = [], [], []
        radius = patch_size = 31

        for point in self.keypoints:
            y, x = point

            x_min = max(0, x - patch_size)
            x_max = min(self.grad_x.shape[0], x + patch_size + 1)
            y_min = max(0, y - patch_size)
            y_max = min(self.grad_y.shape[1], y + patch_size + 1)

            patch = image[y_min:y_max, x_min:x_max]
            Y, X = np.ogrid[:patch.shape[0], :patch.shape[1]]
            dist = (Y - radius) ** 2 + (X - radius) ** 2
            mask = dist <= radius ** 2  # маска окружности внутри патча

            # моментц считаем
            m_00 = np.sum(mask * patch)
            m_01 = np.sum(mask * patch * (Y - radius))
            m_10 = np.sum(mask * patch * (X - radius))

            orientations.append((m_00, m_01, m_10))
            C.append((m_10 / m_00 if m_00 != 0 else 0, m_01 / m_00 if m_00 != 0 else 0))
            angle.append(math.atan2(m_01, m_10))

        return orientations, C, angle

    def get_orientation_keypoints(self, file_path, image_to_work=None):
        self.orientation, self.C, self.angle = self.set_orientation_keypoints(self.gray_image_array if image_to_work is None else image_to_work)
        self.filtered_keypoints_with_orient_image = np.stack([self.gray_image_array if image_to_work is None else image_to_work] * 3, axis=-1)

        plt.figure(figsize=(10, 10))
        plt.title("Ключевые точки с ориентацией")
        plt.axis('off')

        for point, centroid, orientation_angle in zip(self.keypoints, self.C, self.angle):
            y, x = point  # Координаты ключевой точки
            self.filtered_keypoints_with_orient_image[x, y] = [255, 0, 0]

            # окружность
            circle = plt.Circle((y, x), 31, color='red', fill=False, linewidth=0.5)
            plt.gca().add_patch(circle)

            # Нарисовать вектор ориентации
            dx = 31 * np.cos(orientation_angle)  # Смещение по x
            dy = 31 * np.sin(orientation_angle)  # Смещение по y
            plt.arrow(y, x, dy, dx, color='red', head_width=2, head_length=2, linewidth=0.8)

            # Отметить саму ключевую точку
            plt.scatter(y, x, c='green', s=5)

        plt.imshow(self.filtered_keypoints_with_orient_image)
        plt.savefig(f'{file_path}', bbox_inches='tight')
        plt.show()

    def generate_matrix_S(self, patch_size=31, descriptor_length=256):
        """
        Генерация случайных пар точек для построения дескрипторов.
        Координаты точек генерируются с нормальным распределением.
        """
        p = patch_size
        scale = p ** 2 / 25  # дисперсия для нормального распределения
        random_pairs = np.random.normal(0, scale, (descriptor_length, 2, 2))
        random_pairs = np.clip(random_pairs, -p // 2, p // 2)  # Ограничиваем внутри патча
        random_pairs = random_pairs.astype(int)  # Делаем индексы целыми числами
        return random_pairs

    def generate_matrix_S_thetha(self, S):
        """
        Предвычисление S_поворота для 30 углов (шаг 2pi/30).
        """
        rotated_pairs_by_angle = {}
        angles = np.linspace(0, 2 * np.pi, 30, endpoint=False)  # Углы от 0 до 2pi с шагом 2pi/30

        for angle in angles:
            # Матрица поворота
            cos_theta = np.cos(angle)
            sin_theta = np.sin(angle)
            rotation_matrix = np.array([[cos_theta, -sin_theta], [sin_theta, cos_theta]])

            rotated_pairs = np.dot(S, rotation_matrix.T)  # Поворачиваем пары точек
            rotated_pairs_by_angle[angle] = rotated_pairs

        return rotated_pairs_by_angle

    def find_closest_angle(self, angle):
        step = 2 * np.pi / 30

        normalized_angle = angle % (2 * np.pi)

        # Вычисление индекса ближайшего угла
        closest_index = round(normalized_angle / step) % 30  # Модуль на случай превышения 30
        closest_angle = closest_index * step  # Угол, соответствующий индексу

        return closest_angle

    def bilinear_interpolation(self, img, x, y):
        """
        Выполняет биллинейную интерполяцию для дробных координат (x, y).

        :param img: 2D-массив (изображение)
        :param x: дробная координата по оси X
        :param y: дробная координата по оси Y
        :return: интенсивность пикселя после интерполяции
        """
        # Координаты соседних пикселей
        x0, y0 = int(x), int(y)
        x1, y1 = x0 + 1, y0 + 1

        # Проверяем границы изображения
        if x0 < 0 or x1 >= img.shape[1] or y0 < 0 or y1 >= img.shape[0]:
            return 0  # За пределами изображения

        # Значения в четырех соседних пикселях
        I00 = img[y0, x0]
        I10 = img[y0, x1]
        I01 = img[y1, x0]
        I11 = img[y1, x1]

        # Дробные части координат
        dx = x - x0
        dy = y - y0

        # Биллинейная интерполяция
        I = (1 - dx) * (1 - dy) * I00 + dx * (1 - dy) * I10 + \
            (1 - dx) * dy * I01 + dx * dy * I11

        return I

    def compute_brief_for_keypoint(self, image, keypoint, angle, S_thetha, patch_size=31):
        """
        Вычисление дескриптора BRIEF для одной ключевой точки.
        :param keypoint: координаты ключевой точки (x, y)
        :return: бинарный дескриптор (numpy array) или None, если точка близка к границе изображения
        """
        x, y = keypoint
        half_size = patch_size // 2

        # Проверка на границы изображения
        if (x - half_size < 0 or y - half_size < 0 or
                x + half_size >= image.shape[1] or
                y + half_size >= image.shape[0]):
            return None

        # Извлекаем патч вокруг ключевой точки
        patch = image[y - half_size: y + half_size + 1,
                x - half_size: x + half_size + 1]

        closest_angle = self.find_closest_angle(angle)
        rotated_pairs = S_thetha[closest_angle]

        # Строим дескриптор
        descriptor = []
        for (p1, p2) in rotated_pairs:
            # Координаты точек в патче - жалуется на дробные координаты
            # x1, y1 = half_size + p1[0], half_size + p1[1]
            # x2, y2 = half_size + p2[0], half_size + p2[1]

            # y1, x1 = int(round(p1[0])), int(round(p1[1]))
            # y2, x2 = int(round(p2[0])), int(round(p2[1]))
            #
            # # Сравнение интенсивностей
            # if patch[y1, x1] < patch[y2, x2]:
            #     descriptor.append(1)
            # else:
            #     descriptor.append(0)

            intensity1 = self.bilinear_interpolation(patch, p1[0], p1[1])
            intensity2 = self.bilinear_interpolation(patch, p2[0], p2[1])

            descriptor.append(1 if intensity1 < intensity2 else 0)

        return np.array(descriptor)

    def get_brief_descriptors(self):

        if self.blurred_image is None:
            self.get_blured_image(file_path='images/blured_image')

        # Генерация пар точек
        S_thetha = self.generate_matrix_S_thetha(self.generate_matrix_S())

        # Вычисление дескрипторов
        valid_keypoints = []
        valid_angles = []
        valid_centriods = []
        valid_orientation = []
        self.descriptors = []
        for keypoint, angle, c, orient in zip(self.keypoints, self.angle, self.C, self.orientation):
            descriptor = self.compute_brief_for_keypoint(self.blurred_image, keypoint, angle, S_thetha)
            if descriptor is not None:
                self.descriptors.append(descriptor)
                valid_keypoints.append(keypoint)
                valid_angles.append(angle)
                valid_centriods.append(c)
                valid_orientation.append(orient)

        self.descriptors = np.array(self.descriptors)
        return self.descriptors, valid_keypoints, valid_angles, valid_centriods, valid_orientation

    def set_image_pyramid(self, image, levels=5, sigma=1, kernel_size=5):
        """Создание пирамиды изображений."""
        pyramid = [image]  # Начальный уровень - исходное изображение
        kernel = self.gaussian_kernel(sigma, kernel_size)

        for i in range(1, levels):
            # Размытие и уменьшение размера изображения
            # blurred = self.apply_gaussian_blur(pyramid[-1], kernel)

            reduced_image = pyramid[-1][::2, ::2]  # Субдискретизация по обоим осям
            # reduced_image = blurred[::2, ::2]  # Субдискретизация по обоим осям
            pyramid.append(reduced_image)

        return pyramid

    def get_descriptor_from_pyramid(self):
        full_data = {}

        pyramid = self.set_image_pyramid(self.gray_image_array)
        for index, img in enumerate(pyramid):
            level_full_data = []

            self.get_keypoint_detection(file_path=f'images/keypoint_detection_image_level_{index + 1}',
                                        image_to_work=img)
            self.get_harris_criteria_filtering(file_path=f'images/filtered_keypoint_detection_image_level_{index + 1}',
                                               image_to_work=img)
            self.get_orientation_keypoints(file_path=f'images/orientation_keypoints_image_level_{index + 1}', image_to_work=img)
            descriptors, keypoints, angles, centroids, orientations = self.get_brief_descriptors()

            for desc, keypoint, angle, c, orientation in zip(descriptors, keypoints, angles, centroids, orientations):
                print(orientation)
                level_full_data.append({
                    "keypoint": keypoint,
                    "angle": angle,
                    "descriptor": np.array(desc).tolist(),
                    "centroid": c,
                    "orientation": [int(item) for item in orientation],
                    "level": index
                })
            full_data[index] = level_full_data
            self.grad_x, self.grad_y = None, None

        self.save_keypoints_data_to_file(full_data)


    def save_keypoints_data_to_file(self, keypoints_data, filename="keypoints_full_data.json"):
        with open(filename, 'w') as f:
            json.dump(keypoints_data, f, ensure_ascii=False, indent=4)

    def load_keypoints_data_from_file(self, filename="keypoints_full_data.json"):
        with open(filename, 'r') as f:
            keypoints_data = json.load(f)
        return keypoints_data