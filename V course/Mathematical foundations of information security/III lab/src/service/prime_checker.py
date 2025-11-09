from src.service.elliptic_сurve import EllipticCurveTest
from src.service.miller_rabin import MillerRabinTest
from src.service.pierre_de_fermat import FermatTest
from datetime import datetime
import time


class PrimeChecker:
    """Обработчик для проверки числа на простоту разными методами"""

    @staticmethod
    def fermat_test(x):
        """Проверка простоты тестом Ферма"""
        return FermatTest().apply(x)

    @staticmethod
    def miller_rabin_test(x):
        """Проверка простоты тестом Миллера-Рабина"""
        return MillerRabinTest().apply(x)

    @staticmethod
    def elliptic_curve_test(x):
        """Проверка простоты тестом эллиптических кривых"""
        return EllipticCurveTest().apply(x)


class PrimeCounter:
    """Обработчик для подсчета простых чисел"""

    @staticmethod
    def count_primes(limit: int, save_to_file: bool = True, filename: str = None):
        """Подсчитывает количество простых чисел n ≡ 5 (mod 6) до limit"""

        methods = {
            "Ферма": PrimeChecker.fermat_test,
            "Миллер–Рабин": PrimeChecker.miller_rabin_test,
            "Эллиптический": PrimeChecker.elliptic_curve_test,
        }

        results = {}

        # Подготовим буфер для вывода
        output_lines = []
        output_lines.append(f"\nРезультаты проверки до {limit:,} ({datetime.now().strftime('%Y-%m-%d %H:%M:%S')}):")
        output_lines.append("-" * 60)

        for name, test_func in methods.items():
            start = time.time()
            primes = [
                n for n in range(5, limit + 1, 6)
                if test_func(n)
            ]
            duration = time.time() - start
            results[name] = {
                "count": len(primes),
                "values": primes,
                "time": duration
            }

            values_preview = ', '.join(map(str, primes[:10]))
            if len(primes) > 10:
                values_preview += ", ..."

            output_lines.append(f"{name:<20} — найдено {len(primes):<6} простых за {duration:.4f} c")
            output_lines.append(f"Примеры: [{values_preview}]")
            output_lines.append("-" * 60)

        # Сравнение результатов
        all_counts = [data["count"] for data in results.values()]
        consistent = all(c == all_counts[0] for c in all_counts)
        result_text = "✅ Результаты совпадают" if consistent else "⚠️ Результаты различаются!"
        output_lines.append(result_text)

        # Собираем всё в один текст
        full_output = "\n".join(output_lines)

        # Печатаем в консоль
        print(full_output)

        # Записываем в файл
        if save_to_file:
            if filename is None:
                filename = f"logs\prime_results_{limit}.log"
            with open(filename, "w", encoding="utf-8") as f:
                f.write(full_output)
            print(f"\n💾 Результаты сохранены в файл: {filename}")
