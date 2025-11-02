from src.models.boolean_function import BooleanFunction
from src.services.generator_service import GeneratorService
from src.services.nonlinearity_service import NonlinearityService
from src.services.hamming_service import HammingService
from src.models.linear_function import LinearFunction

class MainController:

    @staticmethod
    def demo():
        # Пример: f(x1,x2,x3) = x1*x2 + x3
        f = BooleanFunction(3, [0,1,0,1,0,1,1,0])
        print(f'Булевая функция f = {f}')

        # Линейная функция для проверки
        g = LinearFunction(3, [0, 1, 0, 1])  # f = x1 + x3
        print(f'Линейная булевая функция g = {g}')

        print(f"Расстояние Хэмминга между f и g: {HammingService.get_distance(f,g)}")

        nl = NonlinearityService.compute_nonlinearity(f)
        print(f"Степень нелинейности функции f: {nl}")

    @staticmethod
    def demo_bent():
        print("=== Генерация bent-функций ===")

        for n in [4, 6]:
            bent = GeneratorService.generate_bent(n)
            nl = NonlinearityService.compute_nonlinearity(bent)
            print(f"n = {n}")
            print(f"f(x) = {bent.description}")
            print(f"Вектор значений: {bent.values}")
            print(f"Нелинейность: {nl}")
            print("-" * 40)