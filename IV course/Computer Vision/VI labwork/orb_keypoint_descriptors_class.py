from hough_transform_class import *
import json
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

        circle_points = [(3, 0), (3, 1), (2, 2), (1, 3), (0, 3), (-1, 3), (-2, 2), (-3, 1), (-3, 0), (-3, -1), (-2, -2), (-1, -3), (0, -3), (1, -3), (2, -2), (3, -1)]
        # Проверяем 1,9 и 5,13 (пиксели для ускоренной проверки)
        points_to_check = [circle_points[i] for i in [0, 8, 4, 12]]
        result = []
        for dx, dy in points_to_check:
            px, py = x + dx, y + dy
            if not (0 <= px < I.shape[1] and 0 <= py < I.shape[0]):
                # continue
                return False
            if I[y, x] + t < I[py,px]:
                # Интенсивность больше -> 1
                result.append(1)
            elif I[y, x] - t > I[py,px]:
                # Интенсивность меньше -> -1
                result.append(-1)
            else:
                # Интенсивность ~такая же -> 0
                result.append(0)
        # если обозреваемая точка - ~контрольная: result -> [1, 1, 1, 0/-1] [0/-1, 1, 1, 1] [-1, -1, -1, 0/1] [0/1, -1, -1, -1]
        for i in range(2):
            # print(f'exampl: {result[i:i+3]} and sum is {sum(result[i:i+3])}')
            if sum(result[i:i+3]) != 3 and sum(result[i:i+3]) != -3:
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
            if sum(result[i:i+12]) != 12 and sum(result[i:i+12]) != -12:
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

    def get_keypoint_detection(self, file_path):
        self.keypoints = self.set_keypoint_detection(self.gray_image)

        self.keypoints_image = np.stack([self.gray_image_array] * 3, axis=-1)
        for (x, y) in self.keypoints:
            if 0 <= x < self.keypoints_image.shape[1] and 0 <= y < self.keypoints_image.shape[0]:
                self.keypoints_image[y, x] = [255, 0, 0]

        plt.figure(figsize=(10, 10))
        plt.imshow(self.keypoints_image)
        plt.axis('off')
        plt.savefig(f'{file_path}', bbox_inches='tight')
        plt.show()

    def set_harris_filtration(self):
        if self.grad_x is None and self.grad_y is None:
            self.get_blured_image(file_path="images/blured_image")
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

    def set_harris_criteria_filtering(self):
        # Тут выбрал разбить изображение на сетку и оставить в каждой сетке по M сильных точек
        self.harris_criteria = self.set_harris_filtration()
        M = 10
        grid_size = (8, 8)
        height, width = self.gray_image_array.shape[:2]
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

            grid_cells[cell].append((r,point))

        filtered_points = []
        for cell, points in grid_cells.items():
            points.sort(reverse=True, key=lambda x: x[0]) # сортируем по r
            filtered_points.extend([point for _, point in points[:M]])

        return filtered_points

    def get_harris_criteria_filtering(self, file_path):
        self.keypoints = self.set_harris_criteria_filtering()
        print(len(self.keypoints))
        self.filtered_keypoints_image = np.stack([self.gray_image_array] * 3, axis=-1)
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
            mask = dist <= radius ** 2 # маска окружности внутри патча

            # моментц считаем
            m_00 = np.sum(mask * patch)
            m_01 = np.sum(mask * patch * (Y - radius))
            m_10 = np.sum(mask * patch * (X - radius))

            orientations.append((m_00, m_01, m_10))
            C.append((m_10/m_00 if m_00 != 0 else 0, m_01/m_00 if m_00 != 0 else 0))
            angle.append(math.atan2(m_01, m_10))

        return orientations, C, angle

    def get_orientation_keypoints(self, file_path):
        self.orientation, self.C, self.angle = self.set_orientation_keypoints(self.gray_image_array)
        self.filtered_keypoints_with_orient_image = np.stack([self.gray_image_array] * 3, axis=-1)

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

    def generate_random_pairs(self, n, patch_size):
        """Генерация n пар точек внутри патча размером patch_size x patch_size."""
        sigma = patch_size ** 2 / 25  # Стандартное отклонение
        pairs = np.random.normal(loc=0, scale=np.sqrt(sigma), size=(n, 2, 2))
        pairs = np.clip(pairs + patch_size // 2, 0, patch_size - 1).astype(int)  # Ограничение в пределах патча
        return pairs

    def apply_rotation(self, pairs, angle, patch_center):
        """Поворот пар точек на заданный угол вокруг центра патча."""
        rotation_matrix = np.array([[np.cos(angle), -np.sin(angle)],
                                    [np.sin(angle), np.cos(angle)]])
        rotated_pairs = []
        for p1, p2 in pairs:
            p1_rot = np.dot(rotation_matrix, p1 - patch_center) + patch_center
            p2_rot = np.dot(rotation_matrix, p2 - patch_center) + patch_center
            rotated_pairs.append((p1_rot, p2_rot))
        return np.array(rotated_pairs).astype(int)

    def compute_brief_descriptor(self, image, keypoint, pairs, angle, patch_size=31):
        """Вычисляет BRIEF-дескриптор для одной ключевой точки."""
        x, y = keypoint
        patch = image[y - patch_size // 2 : y + patch_size // 2 + 1,
                      x - patch_size // 2 : x + patch_size // 2 + 1]

        # Центр патча
        patch_center = np.array([patch_size // 2, patch_size // 2])

        # Повернуть пары точек в соответствии с ориентацией
        rotated_pairs = self.apply_rotation(pairs, angle, patch_center)

        # Построение бинарного дескриптора
        descriptor = []
        for (x1, y1), (x2, y2) in rotated_pairs:
            if 0 <= x1 < patch_size and 0 <= y1 < patch_size and 0 <= x2 < patch_size and 0 <= y2 < patch_size:
                descriptor.append(int(patch[y1, x1] < patch[y2, x2]))
            else:
                descriptor.append(0)  # Если точка выходит за границы

        return np.array(descriptor, dtype=np.uint8)

    def compute_descriptors(self, image, keypoints, angles, patch_size=31, n_pairs=256):
        """Вычисляет дескрипторы для всех ключевых точек."""
        # Генерация случайных пар точек
        pairs = self.generate_random_pairs(n_pairs, patch_size)

        # Построение дескрипторов
        descriptors = []
        for keypoint, angle in zip(keypoints, angles):
            descriptor = self.compute_brief_descriptor(image, keypoint, pairs, angle, patch_size)
            descriptors.append(descriptor)

        return np.array(descriptors)

    def set_descriptor(self):
        if self.blurred_image is None:
            self.get_blured_image(file_path='images/blured_image')

        self.descriptors = self.compute_descriptors(self.blurred_image, self.keypoints, self.angle, patch_size=31, n_pairs=256)

    def get_descriptor(self, file_path):
        """
        Визуализация ключевых точек на изображении и их дескрипторов.
        """
        self.set_descriptor()
        self.save_descriptors('descriptor_data', self.keypoints, self.angle, self.descriptors, self.generate_random_pairs(256, 31))
        plt.figure(figsize=(10, 10))
        plt.imshow(self.blurred_image, cmap='gray')

        for i, (x, y) in enumerate(self.keypoints):  # Ограничимся первыми 30 точками
            plt.scatter(x, y, color="red", s=10)
            plt.text(x, y, f"{i}", color="yellow", fontsize=8)
            print(f"Ключевая точка {i}: ({x}, {y}), Дескриптор: {np.array(self.descriptors).tolist()[i]}")

        plt.title("Ключевые точки с номерами")
        plt.axis("off")
        plt.savefig(f'{file_path}')
        plt.show()

    def save_descriptors(self, file_path, keypoints, angles, descriptors, pairs):
        """
        Сохраняет дескрипторы, ключевые точки, их ориентации и пары точек в файл.
        """
        # Преобразуем все данные в удобный для сохранения формат
        data = {
            "keypoints": keypoints,
            "angles": [float(a) for a in angles],
            "descriptors": np.array(descriptors).tolist(),
            "pairs": np.array(pairs).tolist(),
        }

        # Сохраняем как JSON для читаемости
        with open(file_path, "w") as f:
            json.dump(data, f, indent=4)
        print(f"Данные сохранены в {file_path}")