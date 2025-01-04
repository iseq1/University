from computer_vision_class import *
import random


class Segmentation(Computer_Vision):
    def __init__(self):
        super().__init__()
        self.binary_image = None
        self.without_noise_image = None
        self.segments = None
        self.colored_image = None
        self.minima_indices = None
        self.segments_new = None
        self.colored_image_new = None

    def set_binary_image(self, image):
        # Делаю по поиску порога методом Оцу
        # Вычисляем гистограмму
        histogram, _ = np.histogram(image, bins=256, range=(0, 255))
        print(histogram)
        # Максимальное значение интенсивности пикселя
        G_max = 255
        # Минимальное значение внутриклассовой дисперсии
        S_min = float('inf')
        # S_min = 255
        # Оптимальный порог
        T = 0
        # Общее количество пикселей
        total_pixels = image.size
        # Шаг для перебора порогов
        t = 1

        # Нахождение оптимального порога по минимизации внутриклассовой дисперсии
        # Внутриклассовая дисперсия - это значение разброса интенсивностей пикселей внутри классов (фон <==> объект)
        # Меньшее значение дисперсии => лучше разделение на классы
        for u in range(1, G_max + 1, t):
            if np.sum(histogram[:u]) == 0 or np.sum(histogram[u:]) == 0:
                continue

            # Веса определяются как нормализованная сумма всех пикселей (доля пикселей в каждом классе)
            # Вес класса фона (нормализованный) от 0 до u - 1
            weight_background = np.sum(histogram[:u]) / total_pixels
            # Вес класса объекта (нормализованный) от u до G_max
            weight_foreground = np.sum(histogram[u:]) / total_pixels

            # Средние значения интенсивности пикселей для фона и объекта
            # Вычисляем и суммируем взвешенные значения интенсивности (Интенсивность пикселя * на количество пикселей с данной интенсивностью) для класса =>
            # => Общая интенсивность класса => Среднее значение интенсивности
            mean_background = np.sum(np.arange(u) * histogram[:u]) / np.sum(histogram[:u])
            mean_foreground = np.sum(np.arange(u, G_max + 1) * histogram[u:]) / np.sum(histogram[u:])

            # Дисперсии интенсивности для классов фона и объекта
            # Вычисляем дисперсию (среднее значение квадратов отклонений) => Скалярное произведение вектора квадратов отклонений на гистограмму =>
            # Взвешенная сумма квадратов отклонений / вес класса => Дисперсия интенсивности для класса
            variance_background = np.dot((np.arange(u) - mean_background) ** 2, histogram[:u]) / weight_background
            variance_foreground = np.dot((np.arange(u, G_max + 1) - mean_foreground) ** 2,
                                         histogram[u:]) / weight_foreground

            # Значение внутриклассовой дисперсии (взвешенная сумма дисперсий интенсивности для классов)
            sigma_w_squared = weight_background * variance_background + weight_foreground * variance_foreground

            # Используем внутриклассовую дисперсию как оценку качества разделения на классы
            if sigma_w_squared < S_min:
                S_min = sigma_w_squared
                T = u

        # Применяем порог T к изображению (создаем бинарную маску)
        binary_image = (image >= T).astype(np.uint8) * 255
        return binary_image

    def get_binary_image(self, file_path):
        self.binary_image = self.set_binary_image(self.gray_image_array)

        plt.figure(figsize=(10, 5))
        plt.title("Изображение после бинаризации")
        plt.axis('off')
        plt.imshow(self.binary_image, cmap='gray')
        plt.savefig(f'{file_path}')
        plt.show()

    def set_salt_and_pepper_noise_remover(self, image):
        denoised_image = image.copy()

        height, width = image.shape

        for i in range(1, height - 1):
            for j in range(1, width - 1):
                pixel = image[i, j]
                neighbors = [
                    image[i - 1, j - 1], image[i - 1, j], image[i - 1, j + 1],
                    image[i, j - 1], image[i, j + 1],
                    image[i + 1, j - 1], image[i + 1, j], image[i + 1, j + 1]
                ]

                if pixel == 255 and all(n == 0 for n in neighbors):
                    denoised_image[i, j] = 0
                elif pixel == 0 and all(n == 255 for n in neighbors):
                    denoised_image[i, j] = 255

        return denoised_image

    def get_salt_and_pepper_noise_remover(self, file_path):
        self.without_noise_image = self.set_salt_and_pepper_noise_remover(self.binary_image)

        plt.figure(figsize=(10, 5))
        plt.title("Изображение после удаления специй")
        plt.axis('off')
        plt.imshow(self.without_noise_image, cmap='gray')
        plt.savefig(f'{file_path}')
        plt.show()

    def set_seed_growth_segmentation(self, image):
        height, width = image.shape

        segments = np.zeros((height, width), dtype=np.int32)

        # Инициализация номера сегмента
        current_segment = 1

        def grow_segment(x, y, segment_number):
            stack = [(x, y)]

            while stack:
                cx, cy = stack.pop()

                # Учет границ
                if cx < 0 or cx >= height or cy < 0 or cy >= width:
                    continue

                # Проверка на принадлежность к сегменту и критерию похожести
                if segments[cx, cy] != 0 or image[cx, cy] != image[x, y]:
                    continue

                segments[cx, cy] = segment_number

                # Соседи
                stack.append((cx - 1, cy))
                stack.append((cx + 1, cy))
                stack.append((cx, cy - 1))
                stack.append((cx, cy + 1))

        for i in range(height):
            for j in range(width):
                if segments[i, j] == 0:
                    grow_segment(i, j, current_segment)
                    current_segment += 1

        return segments

    def get_seed_growth_segmentation(self, file_path):
        self.segments = self.set_seed_growth_segmentation(self.without_noise_image)

        plt.figure(figsize=(10, 5))
        plt.title("Сегментированное изображение")
        plt.axis('off')
        plt.imshow(self.segments, cmap='nipy_spectral')
        plt.savefig(f'{file_path}')

        plt.show()

    def generate_random_color(self, used_colors):
        while True:
            color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
            if color not in used_colors:
                used_colors.add(color)
                return color

    def set_color_segments(self, segments):

        height, width = segments.shape

        colored_image = np.zeros((height, width, 3), dtype=np.uint8)

        used_colors = set()

        unique_segments = np.unique(segments)
        for segment in unique_segments:
            color = self.generate_random_color(used_colors)
            colored_image[segments == segment] = color

        return colored_image

    def get_color_segments(self, file_path):
        self.colored_image = self.set_color_segments(self.segments)

        plt.figure(figsize=(10, 5))
        plt.title("Сегментированное изображение с уникальными цветами")
        plt.axis('off')
        plt.imshow(self.colored_image)
        plt.savefig(f'{file_path}')
        plt.show()

    def set_local_minimum_with_neighborhood(self, histogram, neighborhood_size):
        minima_indices = []
        for i in range(0, len(histogram), neighborhood_size):
            # Начальная точка
            start = i

            # Конечная точка с проверкой на выход за границы
            end = min(i + neighborhood_size, len(histogram))

            # Находим локальный минимум в текущей области
            local_min_index = start + np.argmin(histogram[start:end])
            minima_indices.append(local_min_index)

        return minima_indices

    def get_local_minimum_with_neighborhood(self, file_path):
        histogram, bins = self.set_histogram(self.gray_image_array)
        neighborhood_size = 50
        minima_indices = self.set_local_minimum_with_neighborhood(histogram, neighborhood_size)
        self.minima_indices = minima_indices
        plt.figure(figsize=(10, 5))
        plt.plot(bins[:-1], histogram, color='pink')
        plt.plot(minima_indices, histogram[minima_indices], "rx")
        plt.title("Гистограмма полутонового изображения с локальными минимумами")
        plt.xlabel("Значение пикселя")
        plt.ylabel("Частота")
        plt.grid(True)
        plt.savefig(f'{file_path}')
        plt.show()

    def apply_histogram_clustering(self, image, minima_indices):
        clustered_image = np.zeros_like(image)
        cluster_id = 1

        minima_indices = np.concatenate(([0], minima_indices, [256]))

        # Проход по парам соседних минимумов
        for i in range(len(minima_indices) - 1):
            lower_bound = minima_indices[i]
            upper_bound = minima_indices[i + 1]
            mask = (image >= lower_bound) & (image < upper_bound)
            clustered_image[mask] = cluster_id
            cluster_id += 1

        return clustered_image

    def set_seed_growth_segmentation_with_init(self, image, clustered_image):

        height, width = np.array(image).shape

        segments_new = np.zeros((height, width), dtype=np.int32)
        current_segment = 1

        def grow_segment(x, y, cluster_id):
            stack = [(x, y)]

            while stack:
                cx, cy = stack.pop()

                # Проверка границ
                if cx < 0 or cx >= height or cy < 0 or cy >= width:
                    continue

                # Проверка, что пиксель уже помечен или не принадлежит текущему кластеру
                if segments_new[cx, cy] != 0 or clustered_image[cx, cy] != cluster_id:
                    continue

                segments_new[cx, cy] = current_segment

                # Соседи
                stack.append((cx - 1, cy))
                stack.append((cx + 1, cy))
                stack.append((cx, cy - 1))
                stack.append((cx, cy + 1))

                # Проход по кластерам

        unique_clusters = np.unique(clustered_image)
        for cluster_id in unique_clusters:
            for i in range(height):
                for j in range(width):
                    if segments_new[i, j] == 0 and clustered_image[i, j] == cluster_id:
                        grow_segment(i, j, cluster_id)
                        current_segment += 1

        return segments_new

    def get_seed_growth_segmentation_with_init(self, file_path):
        # Кластеризация(histogram, neighborhood_size)
        clustered_image = self.apply_histogram_clustering(self.gray_image, self.minima_indices)
        # Применение алгоритма выращивания семян
        self.segments_new = self.set_seed_growth_segmentation_with_init(self.gray_image, clustered_image)

        plt.figure(figsize=(10, 5))
        plt.title("Сегментированное изображение")
        plt.axis('off')
        plt.imshow(self.segments_new, cmap='nipy_spectral')
        plt.savefig(f'{file_path}')
        plt.show()

    def get_colored_image_new(self, file_path):
        self.colored_image_new = self.set_color_segments(self.segments_new)
        plt.figure(figsize=(10, 5))
        plt.title("Сегментированное изображение с уникальными цветами")
        plt.axis('off')
        plt.imshow(self.colored_image_new)
        plt.savefig(f'{file_path}')
        plt.show()