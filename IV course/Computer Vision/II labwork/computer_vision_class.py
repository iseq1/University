import matplotlib.pyplot as plt
from PIL import Image
import numpy as np

class Computer_Vision:
    def __init__(self):
        self.image = None
        self.image_array = None
        self.inverted_image = None
        self.inverted_image_array = None
        self.gray_image = None
        self.gray_image_array = None
        self.noisy_gray_image = None
        self.noisy_gray_image_array = None
        self.blurred_image = None
        self.blurred_image_array = None
        self.equalized_image = None
        self.equalized_image_picture = None

    def set_image(self, image_path):
        '''
        Считываю цветное изображение в numpy-массив.

        :param image_path:
        :return:
        '''
        image = Image.open(image_path)
        self.image = image
        self.image_array = np.array(image)
        plt.figure(figsize=(10, 5))
        plt.subplot(1, 1, 1)
        plt.title("Оригинальное изображение")

        print(f"Размер изображения: {image.size}\n"
              f"Форма numpy-массива: {self.image_array.shape}\n")

    def get_image(self, file_path):
        '''
        Показываю оригинальную картинку
        :return:
        '''
        plt.imshow(self.image)  # Отображение изображения
        plt.savefig(f'{file_path}', bbox_inches='tight')
        plt.show()  # Показываем графики

    def set_inverted_image(self):
        '''
        Провожу инвертирование изображения.
        :return:
        '''
        self.inverted_image_array = 255 - self.image_array
        self.inverted_image = Image.fromarray(self.inverted_image_array)

    def get_inverted_image(self, file_path):
        '''
        Показываю инвертированное изображение.
        :return:
        '''
        self.set_inverted_image()
        plt.figure(figsize=(10, 5))
        plt.subplot(1, 2, 1)
        plt.title("Оригинал")
        plt.imshow(self.image)

        plt.subplot(1, 2, 2)
        plt.title("Инвертированный оригинал")
        plt.imshow(self.inverted_image)
        plt.savefig(f'{file_path}', bbox_inches='tight')
        plt.show()

    def set_gray_image(self):
        '''
        Перевожу изображение в полутоновое, используя усреднение по каналам.
        :return:
        '''
        image_to_work = self.inverted_image_array if self.inverted_image_array is not None else self.image_array
        height, width, _ = image_to_work.shape
        gray_image_array = np.zeros((height, width), dtype=np.uint8)

        for i in range(height):
            for j in range(width):
                r, g, b = image_to_work[i, j].astype(np.int16)
                gray_image_array[i, j] = (r + g + b) // 3

        self.gray_image_array = np.clip(gray_image_array, 0, 255).astype(np.uint8)
        self.gray_image = Image.fromarray(self.gray_image_array, mode='L')

    def get_gray_image(self, file_path):
        '''
        Показываю полутоновое изображение.
        :return:
        '''
        self.set_gray_image()
        plt.figure(figsize=(10, 5))
        plt.subplot(1, 2, 1)
        plt.title("Оригинал")
        plt.imshow(self.image)

        plt.subplot(1, 2, 2)
        plt.title("Полутоновый оригинал")
        plt.imshow(self.gray_image, cmap='gray')
        plt.savefig(f'{file_path}', bbox_inches='tight')
        plt.show()

    def set_noisy_image(self):
        '''
        Добавляю случайный шум (нормальное распределение).
        :return:
        '''
        mean = 0
        std_dev = 25
        noise = np.random.normal(mean, std_dev, self.gray_image_array.shape).astype(np.int16)
        mask = np.random.choice([0, 1], size=self.gray_image_array.shape, p=[0.5, 0.5])
        noisy_gray_image_array = self.gray_image_array.astype(np.int16) + noise * mask
        noisy_gray_image_array = np.clip(noisy_gray_image_array, 0, 255).astype(np.uint8)
        noisy_gray_image = Image.fromarray(noisy_gray_image_array, mode='L')
        self.noisy_gray_image_array = noisy_gray_image_array
        self.noisy_gray_image = noisy_gray_image

    def get_noisy_image(self, file_path):
        '''
        Показываю шумное изображение.
        :return:
        '''
        self.set_noisy_image()
        plt.figure(figsize=(10, 5))
        plt.subplot(1, 2, 1)
        plt.title("Полутоновый оригинал")
        plt.imshow(self.gray_image, cmap='gray')

        plt.subplot(1, 2, 2)
        plt.title("Зашумленный полутоновый оригинал")
        plt.imshow(self.noisy_gray_image, cmap='gray')
        plt.savefig(f'{file_path}', bbox_inches='tight')
        plt.show()

    def set_histogram(self, array=None):
        '''
        Строю гистограмму полученного изображения.
        :return:
        '''
        return np.histogram(
            self.noisy_gray_image_array if array is None else array, bins=256, range=(0, 255))

    def get_histogram(self, file_path, array=None):
        '''
        Показываю гистограмму.
        :return:
        '''
        histogram, bins = self.set_histogram(array)

        plt.figure(figsize=(10, 5))
        plt.bar(bins[:-1], histogram, width=1, color='pink')
        plt.title("Гистограмма полутонового зашумленного оригинала")
        plt.xlabel("Яркость")
        plt.ylabel("Частота")
        plt.savefig(f'{file_path}', bbox_inches='tight')
        plt.show()

    def gaussian_kernel(self, sigma, size):
        '''
        Считаю значение по формуле функции Гаусса в двух измерениях.
        :param sigma:
        :param size:
        :return:
        '''
        ax = np.arange(-size // 2 + 1., size // 2 + 1.)
        xx, yy = np.meshgrid(ax, ax)
        kernel = np.exp(-(xx ** 2 + yy ** 2) / (2. * sigma ** 2))
        kernel = kernel / (2 * np.pi * sigma ** 2)
        kernel = kernel / np.sum(kernel)
        return kernel

    def apply_gaussian_blur(self, image, kernel):
        '''
        Считаю значение функции Гаусса для матрицы
        :param image:
        :param kernel:
        :return:
        '''
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

    def set_blured_image(self):
        '''
        Произвожу размытие изображения с помощью ядра Гаусса с разными значениями дисперсии и размера фильтра.
        :return:
        '''
        cores = [
            (1, 3),
            (2, 5),
            (5, 9),
        ]

        results = {}

        for sigma, size in cores:
            kernel = self.gaussian_kernel(sigma, size)

            blurred_image = self.apply_gaussian_blur(self.noisy_gray_image_array, kernel)

            results[f"σ={sigma}, размер={size}"] = blurred_image

        return results

    def get_blured_image(self, file_path):
        '''
        Показываю размытые изображения
        :return:
        '''
        results = self.set_blured_image()
        plt.figure(figsize=(12, 8))

        for idx, (key, blurred_image) in enumerate(results.items()):
            # (строки - для дисперсий, столбцы - для размеров)
            plt.subplot(1, len(results), idx + 1)
            plt.imshow(blurred_image, cmap='grey')
            self.blurred_image = blurred_image
            plt.title(key)
            plt.axis('off')

        plt.tight_layout()
        plt.savefig(f'{file_path}', bbox_inches='tight')
        plt.show()

    def manual_histogram_equalization(self, image):
        '''
        Эквализирую гистограммы изображения по яркости.
        :param image:
        :return:
        '''
        # Кол-во пикселей в конкретном интервале яркости
        histogram, _ = np.histogram(image.flatten(), bins=256, range=(0, 255))

        pixels = image.size

        cdf = histogram.cumsum()

        cdf_min = cdf[cdf > 0].min()

        equalized_image = np.zeros_like(image, dtype=np.uint8)

        for x in range(256):
            equalized_image[image == x] = round((cdf[x] - cdf_min) / (pixels - 1) * 255)

        return equalized_image

    def set_equalized_image(self):
        '''
        Провожу эквализацию гистограммы изображения.
        :return:
        '''
        equalized_image = self.manual_histogram_equalization(self.blurred_image)
        # тут надо перевести в L канал, чтобы было чб, а у меня сине-желтое (причем equalized_image - уже image)
        self.equalized_image_array = equalized_image
        self.equalized_image = Image.fromarray(equalized_image, mode='L')



        histogram, bins = np.histogram(self.blurred_image.flatten(), bins=256, range=(0, 255))
        return equalized_image, histogram, bins

    def get_equalized_histogram(self, file_path):
        '''
        Показываю гистограммы.
        :return:
        '''
        equalized_image, histogram, bins = self.set_equalized_image()
        plt.figure(figsize=(12, 6))

        plt.subplot(1, 2, 1)
        plt.bar(bins[:-1], histogram, width=1, color='cyan')
        plt.title("Гистограмма размытого оригинала")
        plt.xlabel("Яркость")
        plt.ylabel("Частота")

        hist_equalized, bins_equalized = np.histogram(equalized_image.flatten(), bins=256, range=(0, 255))
        plt.subplot(1, 2, 2)
        plt.bar(bins_equalized[:-1], hist_equalized, width=1, color='pink')
        plt.title("Гистограмма эквализованного изображения")
        plt.xlabel("Яркость")
        plt.ylabel("Частота")

        plt.tight_layout()
        plt.savefig(f'{file_path}', bbox_inches='tight')
        plt.show()



    def get_equalized_image(self, file_path):
        '''
        показываю эквализированное изображение
        :param file_path:
        :return:
        '''
        plt.title("Эквализованное изображение")
        plt.imshow(self.equalized_image, cmap='gray')  # Отображение изображения
        plt.savefig(f'{file_path}', bbox_inches='tight')
        plt.show()
