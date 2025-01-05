from segmentation_class import *


class EdgeDetector(Segmentation):
    def __init__(self):
        super().__init__()
        self.grad_x = None
        self.grad_y = None
        self.gradient_magnitude = None
        self.gradient_direction = None
        self.gradient_direction_rounded = None
        self.suppressed_image = None
        self.edges = None

    def gaussian_kernel(self, sigma, size):
        ax = np.arange(-size // 2 + 1., size // 2 + 1.)
        xx, yy = np.meshgrid(ax, ax)
        kernel = np.exp(-(xx ** 2 + yy ** 2) / (2. * sigma ** 2))
        kernel = kernel / (2 * np.pi * sigma ** 2)
        kernel = kernel / np.sum(kernel)  # Нормализуем ядро
        return kernel

    def apply_gaussian_blur(self, image, kernel):
        image_height, image_width = image.shape
        kernel_height, kernel_width = kernel.shape
        padding_y, padding_x = kernel_height // 2, kernel_width // 2

        # Создаем пустой массив для результата
        blurred_image = np.zeros_like(image, dtype=np.float32)

        for i in range(image_height):
            for j in range(image_width):
                sum_value = 0.0

                for m in range(kernel_height):
                    for n in range(kernel_width):
                        # Индексы для области среза
                        x = i + m - padding_y
                        y = j + n - padding_x

                        if 0 <= x < image_height and 0 <= y < image_width:
                            sum_value += image[x, y] * kernel[m, n]

                blurred_image[i, j] = sum_value

        return np.clip(blurred_image, 0, 255).astype(np.uint8)

    def get_blured_image(self, file_path, image_to_work=None):
        sigma, size = 1, 5

        kernel = self.gaussian_kernel(sigma, size)
        blurred_image = self.apply_gaussian_blur(self.gray_image_array if image_to_work is None else image_to_work, kernel)
        self.blurred_image = blurred_image
        plt.figure(figsize=(4, 4))
        plt.imshow(blurred_image, cmap='gray')
        plt.title(f"σ={sigma}, размер={size}")
        plt.axis('off')
        plt.savefig(f'{file_path}', bbox_inches='tight')
        plt.tight_layout()
        plt.show()

    def apply_filter(self, image, kernel):
        image_height, image_width = image.shape
        kernel_height, kernel_width = kernel.shape
        padding_y, padding_x = kernel_height // 2, kernel_width // 2

        filtered_image = np.zeros_like(image, dtype=np.float32)

        for i in range(image_height):
            for j in range(image_width):
                sum_value = 0.0

                for m in range(kernel_height):
                    for n in range(kernel_width):
                        x = i + m - padding_y
                        y = j + n - padding_x

                        if 0 <= x < image_height and 0 <= y < image_width:
                            sum_value += image[x, y] * kernel[m, n]

                filtered_image[i, j] = sum_value

        return filtered_image

    def get_gradient_n_magnitude(self, file_path):
        # Фильтры Собеля 3x3
        sobel_x = np.array([[-1, 0, 1],
                            [-2, 0, 2],
                            [-1, 0, 1]])

        sobel_y = np.array([[1, 2, 1],
                            [0, 0, 0],
                            [-1, -2, -1]])

        grad_x = self.apply_filter(self.blurred_image, sobel_x)
        self.grad_x = grad_x
        grad_y = self.apply_filter(self.blurred_image, sobel_y)
        self.grad_y = grad_y

        # Магнитуда и направление градиента
        gradient_magnitude = np.abs(grad_x) + np.abs(grad_y)
        self.gradient_magnitude = gradient_magnitude
        gradient_direction = np.arctan2(grad_y, grad_x)
        self.gradient_direction = gradient_direction


        plt.figure(figsize=(6, 8))
        plt.imshow(grad_x, cmap='gray')
        plt.title('Градиент по X')
        plt.axis('off')
        plt.savefig(f'{file_path[0]}', bbox_inches='tight')
        plt.show()

        plt.figure(figsize=(6, 8))
        plt.imshow(grad_y, cmap='gray')
        plt.title('Градиент по Y')
        plt.axis('off')
        plt.savefig(f'{file_path[1]}', bbox_inches='tight')
        plt.show()

        plt.figure(figsize=(6, 8))
        plt.imshow(gradient_magnitude, cmap='gray')
        plt.title('Магнитуда градиента')
        plt.axis('off')
        plt.savefig(f'{file_path[2]}', bbox_inches='tight')
        plt.show()

        plt.figure(figsize=(6, 8))
        plt.imshow(gradient_direction, cmap='gray')
        plt.title('Направление градиента')
        plt.axis('off')
        plt.savefig(f'{file_path[2]}', bbox_inches='tight')
        plt.show()

    def set_gradient_direction_round(self):
        gradient_direction_degrees = np.degrees(self.gradient_direction)
        directions = np.array([0, 45, 90, 135, 180, 225, 270, 315])

        def round_to_nearest_direction(angle):
            return directions[np.argmin(np.abs(directions - angle))]

        self.gradient_direction_rounded = np.zeros_like(gradient_direction_degrees)

        for i in range(gradient_direction_degrees.shape[0]):
            for j in range(gradient_direction_degrees.shape[1]):
                self.gradient_direction_rounded[i, j] = round_to_nearest_direction(gradient_direction_degrees[i, j])

    def get_gradient_direction_round(self, file_path):
        self.set_gradient_direction_round()
        plt.figure(figsize=(6, 8))
        plt.imshow(self.gradient_direction_rounded, cmap='gray')
        plt.title('Округленное направление градиента')
        plt.axis('off')
        plt.savefig(f'{file_path}', bbox_inches='tight')
        plt.show()

    def set_non_maximum_suppression(self, gradient_magnitude, gradient_direction):
        image_height, image_width = gradient_magnitude.shape
        suppressed_image = np.zeros((image_height, image_width), dtype=np.float32)

        for i in range(1, image_height - 1):
            for j in range(1, image_width - 1):

                # Направление градиента для текущего пикселя
                direction = gradient_direction[i, j]

                if direction == 0 or direction == 180:
                    q = gradient_magnitude[i, j + 1]
                    r = gradient_magnitude[i, j - 1]

                elif direction == 45 or direction == 225:
                    q = gradient_magnitude[i + 1, j - 1]
                    r = gradient_magnitude[i - 1, j + 1]

                elif direction == 90 or direction == 270:
                    q = gradient_magnitude[i + 1, j]
                    r = gradient_magnitude[i - 1, j]

                elif direction == 135 or direction == 315:
                    q = gradient_magnitude[i - 1, j - 1]
                    r = gradient_magnitude[i + 1, j + 1]

                if (gradient_magnitude[i, j] >= q) and (gradient_magnitude[i, j] >= r):
                    suppressed_image[i, j] = gradient_magnitude[i, j]
                else:
                    suppressed_image[i, j] = 0

        return suppressed_image

    def get_non_maximum_suppression(self, file_path):
        suppressed_image = self.set_non_maximum_suppression(self.gradient_magnitude, self.gradient_direction_rounded)
        self.suppressed_image = suppressed_image
        plt.figure(figsize=(6, 8))
        plt.imshow(suppressed_image, cmap='gray')
        plt.title('Подавление немаксимумов')
        plt.axis('off')
        plt.savefig(f'{file_path}', bbox_inches='tight')
        plt.show()

    def set_hysteresis_thresholding(self, suppressed_image, low_threshold, high_threshold):
        image_height, image_width = suppressed_image.shape
        edges = np.zeros((image_height, image_width), dtype=np.uint8)

        # Значения для границ (strong) и пикселей между порогами (weak)
        strong = 255
        weak = 90

        # Границы
        strong_i, strong_j = np.where(suppressed_image > high_threshold)

        # Пиксели, которые находятся между порогами
        boundary_i, boundary_j = np.where((suppressed_image >= low_threshold) & (suppressed_image <= high_threshold))

        # Границы на изображении
        edges[strong_i, strong_j] = strong

        # Пиксели между порогами
        edges[boundary_i, boundary_j] = weak

        def grow_edges(x, y):
            stack = [(x, y)]

            while stack:
                cx, cy = stack.pop()

                for dx in range(-1, 2):
                    for dy in range(-1, 2):
                        nx, ny = cx + dx, cy + dy

                        if nx < 0 or nx >= image_height or ny < 0 or ny >= image_width:
                            continue

                        if suppressed_image[nx, ny] >= low_threshold and edges[nx, ny] != strong:
                            edges[nx, ny] = strong
                            stack.append((nx, ny))

        for i in range(image_height):
            for j in range(image_width):
                if edges[i, j] == strong:
                    grow_edges(i, j)

        # Обнуление пикселей, которые не являются границами (формирование фона)
        edges[edges != strong] = 0

        return edges

    def get_hysteresis_thresholding(self, file_path):
        # Применяем гистерезис (Уменьшение значений => четкость границ) # 80 160
        low_threshold = 100
        high_threshold = 200
        edges = self.set_hysteresis_thresholding(self.suppressed_image, low_threshold, high_threshold)
        self.edges = edges
        # Отображаем результат
        plt.figure(figsize=(8, 8))
        plt.imshow(edges, cmap='gray')
        plt.title('Гистерезис')
        plt.axis('off')
        plt.savefig(f'{file_path[0]}', bbox_inches='tight')
        plt.show()

        plt.figure(figsize=(8, 8))
        plt.imshow(self.image)
        plt.title("Оригинальное изображение")
        plt.axis('off')
        plt.savefig(f'{file_path[1]}', bbox_inches='tight')
        plt.show()
