"""
Класс-обработчик для измерения и уменьшения аддитивного белого шума
"""
from abc import ABC, abstractmethod
import numpy as np
import pywt


class IImageDenoiseHandler(ABC):
    """Интерфейс обработчика"""

    @staticmethod
    @abstractmethod
    def apply(image: np.ndarray) -> dict:
        pass


class ImageDenoiseHandler(IImageDenoiseHandler):

    @staticmethod
    def apply(image: np.ndarray) -> dict:
        try:
            if image is None:
                return {'code': 'denoise', 'data': None, 'msg': 'Нет изображения'}

            sigma_before = ImageDenoiseHandler.estimate_noise_sigma(image)
            denoised, sigma_used = ImageDenoiseHandler.wavelet_denoise(image, sigma_before)

            # на случай, если denoised == None (все равно делаем обработку)
            if denoised is None:
                denoised = image.copy()

            sigma_after = ImageDenoiseHandler.estimate_noise_sigma(denoised)

            quality = 0.0
            if sigma_before > 0:
                quality = (sigma_before - sigma_after) / sigma_before * 100.0
                quality = float(np.clip(quality, 0.0, 100.0))

            return {
                'code': 'denoise',
                'data': denoised,
                'params': {
                    'sigma_before': float(sigma_before),
                    'sigma_after': float(sigma_after),
                    'quality': quality
                },
                'msg': f'Шум уменьшен с σ={sigma_before:.2f} до σ={sigma_after:.2f} ({quality:.1f}% улучшение)'
            }
        except Exception as e:
            print(f"apply error: {e}")
            return {'code': 'denoise', 'data': None, 'msg': f'Ошибка при уменьшении шума: {e}'}


    @staticmethod
    def estimate_noise_sigma(image) -> float:
        """Оценка уровня шума σ через вейвлеты. Возвращает float (всегда)."""
        try:
            if image is None:
                return 0.0

            # приводим к grayscale float
            if image.ndim == 3:
                img = np.mean(image, axis=2).astype(np.float32)
            else:
                img = image.astype(np.float32)

            # маленький чек — если все пиксели равны -> шум 0
            if img.size == 0:
                return 0.0
            if np.all(img == img.flat[0]):
                return 0.0

            # однократное DWT
            coeffs = pywt.dwt2(img, 'db1')
            # coeffs = (cA, (cH, cV, cD))
            try:
                _, (cH, cV, cD) = coeffs
            except Exception:
                # если структура неожиданна — fallback к wavedec2
                coeffs_all = pywt.wavedec2(img, wavelet='db1', level=1)
                # в wavedec2 coeffs_all[1] = (cH, cV, cD)
                _, (cH, cV, cD) = coeffs_all[0], coeffs_all[1]

            # робастная оценка медиа
            med = np.median(np.abs(cD))
            if med == 0:
                return 0.0
            sigma_est = float(med / 0.6745)
            return sigma_est
        except Exception as e:
            print(f"estimate_noise_sigma error: {e}")
            return 0.0

    @staticmethod
    def wavelet_denoise(image, sigma_est=None, wavelet='db1', level=2):
        """Подавление шума по вейвлетам, возвращает RGB-массив"""
        try:
            # Преобразуем к серому для денойза
            if image.ndim == 3:
                image_gray = np.mean(image, axis=2)
            else:
                image_gray = image.copy()

            # Получаем объект вейвлета
            if isinstance(wavelet, str):
                wave = pywt.Wavelet(wavelet)
            elif isinstance(wavelet, pywt.Wavelet):
                wave = wavelet
            else:
                raise ValueError("wavelet must be a str or pywt.Wavelet object")

            # Определяем безопасный уровень декомпозиции
            try:
                max_level = pywt.dwtn_max_level(image_gray.shape, wave.dec_len)
                level = min(level, max_level) if max_level >= 1 else 1
            except Exception:
                level = 1

            # Декомпозиция по вейвлетам
            coeffs = pywt.wavedec2(image_gray, wavelet=wave, level=level)
            cA, cD = coeffs[0], coeffs[1:]

            if sigma_est is None:
                sigma_est = ImageDenoiseHandler.estimate_noise_sigma(image_gray)

            # Универсальный порог Донхо
            threshold = sigma_est * np.sqrt(2 * np.log(image_gray.size))

            # Применяем мягкий порог
            new_coeffs = [cA]
            for (cH, cV, cD_) in cD:
                cH = pywt.threshold(cH, threshold, mode='soft')
                cV = pywt.threshold(cV, threshold, mode='soft')
                cD_ = pywt.threshold(cD_, threshold, mode='soft')
                new_coeffs.append((cH, cV, cD_))

            # Обратное преобразование
            denoised = pywt.waverec2(new_coeffs, wavelet=wave)
            denoised = np.clip(denoised, 0, 255).astype(np.uint8)

            # Преобразуем в RGB
            denoised_rgb = np.stack([denoised] * 3, axis=-1)

            return denoised_rgb, sigma_est

        except Exception as e:
            print(f"wavelet_denoise error: {e}")
            return None, None
