"""
Главный контроллер
"""
from src.models.boolean_function import BooleanFunction
from src.models.linear_function import LinearFunction
from src.services.hamming_service import HammingService
from src.services.nonlinearity_service import NonlinearityService
from src.services.generator_service import GeneratorService
from src.services.sbox_generator import SBoxGenerator


class MainController:

    @staticmethod
    def first_stage():

        # пример из лекции: f = x1*x2 + x3; g = x1 + x3
        f = BooleanFunction(3, [0,1,0,1,0,1,1,0])
        g = LinearFunction(3, [0, 1, 0, 1])

        print(f"Булевая функция f = {f}\n"
              f"Линейная функция g = {g}")

        print("Расстояние Хэмминга:", HammingService.get_distance(f, g))
        print("Нелинейность f:", NonlinearityService.compute_nonlinearity(f))


    @staticmethod
    def second_stage():
        for n in (4, 6):
            bent = GeneratorService.generate_bent(n)
            nl = NonlinearityService.compute_nonlinearity(bent)
            print(f"n={n}, формула: {bent.description}")
            print(f"Вектор значений (кол-во={len(bent.values)}): {bent.values}")
            print("Нелинейность:", nl)
            print("-" * 40)


    @staticmethod
    def third_stage():
        print("Поиск s-box n=5")
        gen = SBoxGenerator(n=5, seed=42)
        sbox, nl = gen.search_best(attempts=5, steps_per_attempt=10, enforce_no_fixed_points=True)
        print("Найден s-box NL:", nl)
        print("Таблица (первые 20 значений):", sbox.table[:20])
        print("Перестановка?:", sbox.is_permutation())
        print("Есть фиксированные точки?:", sbox.has_fixed_points())

