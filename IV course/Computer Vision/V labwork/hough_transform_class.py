from edge_detector_class import *


class HoughTransform(EdgeDetector):
    def __init__(self):
        super().__init__()
        self.accumulator, self.thetas, self.rhos = None, None, None
        self.smoothed_accumulator = None
        self.suppressed_accumulator = None
        self.image_with_lines = None

    def set_hough_transform(self, edges):

        height, width = edges.shape

        # Диапазон значений theta
        theta_min = -np.pi / 2
        theta_max = np.pi
        theta_step = np.pi / 180
        thetas = np.arange(theta_min, theta_max, theta_step)

        # Диапазон значений ro
        diag_len = int(np.sqrt(height ** 2 + width ** 2))
        rhos = np.arange(0, diag_len, 1)

        accumulator = np.zeros((len(rhos), len(thetas)), dtype=int)

        for y in range(height):
            for x in range(width):
                if edges[y, x] == 255:
                    for theta_index, theta in enumerate(thetas):
                        ro = int(x * np.cos(theta) + y * np.sin(theta))
                        if 0 <= ro < diag_len:
                            ro_index = ro
                            accumulator[ro_index, theta_index] += 1

        return accumulator, thetas, rhos

    def get_hough_transform(self, file_path):
        accumulator, thetas, rhos = self.set_hough_transform(self.edges)
        self.accumulator, self.thetas, self.rhos = accumulator, thetas, rhos
        print(accumulator)
        plt.imshow(accumulator, cmap='hot', extent=[np.rad2deg(thetas[0]), np.rad2deg(thetas[-1]), rhos[0], rhos[-1]])
        plt.title('Преобразование Хафа')
        plt.xlabel('Тета (градусы)')
        plt.ylabel('Ро')
        plt.savefig(f'{file_path}', bbox_inches='tight')
        plt.show()

    def set_hough_transform_smoothed(self):
        sigma, size = 1, 3
        kernel = self.gaussian_kernel(sigma, size)
        smoothed_accumulator = self.apply_gaussian_blur(self.accumulator, kernel)
        return smoothed_accumulator

    def get_hough_transform_smoothed(self, file_path):
        self.smoothed_accumulator = self.set_hough_transform_smoothed()
        print(self.smoothed_accumulator)
        plt.imshow(self.smoothed_accumulator, cmap='hot',
                   extent=[np.rad2deg(self.thetas[0]), np.rad2deg(self.thetas[-1]), self.rhos[0], self.rhos[-1]])
        plt.title('Преобразование Хафа (сглаженное)')
        plt.xlabel('Тета (градусы)')
        plt.ylabel('Ро')
        plt.savefig(f'{file_path}', bbox_inches='tight')
        plt.show()

    def set_non_maximum_suppression_haff(self, accumulator):
        image_height, image_width = accumulator.shape
        suppressed_image = np.zeros((image_height, image_width), dtype=np.float32)

        for i in range(1, image_height - 1):
            for j in range(1, image_width - 1):

                current_value = accumulator[i, j]

                neighbors = [
                    accumulator[i - 1, j - 1], accumulator[i - 1, j], accumulator[i - 1, j + 1],
                    accumulator[i, j - 1], accumulator[i, j + 1],
                    accumulator[i + 1, j - 1], accumulator[i + 1, j], accumulator[i + 1, j + 1]
                ]

                if current_value >= max(neighbors):
                    suppressed_image[i, j] = current_value
                else:
                    suppressed_image[i, j] = 0

        return suppressed_image

    def get_non_maximum_suppression_haff(self, file_path):
        suppressed_accumulator = self.set_non_maximum_suppression_haff(self.smoothed_accumulator)
        print(suppressed_accumulator)
        self.suppressed_accumulator = suppressed_accumulator
        plt.imshow(suppressed_accumulator, cmap='hot', extent=[np.rad2deg(self.thetas[0]), np.rad2deg(self.thetas[-1]), self.rhos[0], self.rhos[-1]])
        plt.title('Преобразование Хафа (сглаженное и подавленное)')
        plt.xlabel('Тета (градусы)')
        plt.ylabel('Ро')
        plt.savefig(f'{file_path}', bbox_inches='tight')
        plt.show()

    def set_draw_lines_on_image(self, original_image, suppressed_hough, theta_range, rho_range, edge_image):

        line_image = np.copy(original_image)
        height, width = line_image.shape[:2]

        tresh = 0.5 * np.max(suppressed_hough)
        indices = np.argwhere(suppressed_hough > 0)
        # используя такой трешхолд, на моей картинке не особо линии рисует(
        # indices = np.argwhere(suppressed_hough > tresh)

        for rho_idx, theta_idx in indices:
            rho = rho_range[rho_idx]
            theta = theta_range[theta_idx]

            x = np.arange(0, width)
            y = ((rho - x * np.cos(theta)) / np.sin(theta)).astype(int)

            for px, py in zip(x, y):
                if 0 <= px < width and 0 <= py < height:
                    try:
                        if edge_image[py, px] == 255:
                            line_image[py, px] = [0, 0, 255]
                    except IndexError:
                        print(f"Индекс [px={px}, py={py}] вне границ [width={width}, height={height}]")
                        continue

        return line_image

    def get_draw_lines_on_image(self, file_path):
        image_with_lines = self.set_draw_lines_on_image(self.image_array, self.accumulator, self.thetas, self.rhos, self.edges)
        self.image_with_lines = image_with_lines
        plt.figure(figsize=(10, 10))
        plt.imshow(image_with_lines)
        plt.axis('off')
        plt.savefig(f'{file_path}', bbox_inches='tight')
        plt.show()
