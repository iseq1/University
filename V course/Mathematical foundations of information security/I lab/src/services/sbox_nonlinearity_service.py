"""
Сервис вычисления степени нелинейности S-box.
"""
from itertools import product
from src.models.sbox import SBox
from src.models.boolean_function import BooleanFunction
from src.services.nonlinearity_service import NonlinearityService


class SBoxNonlinearityService:
    """
    Вычисление нелинейности S-box
    """

    @staticmethod
    def compute_sbox_nonlinearity(sbox: SBox) -> int:
        """
        Вычисляет степень нелинейности объекта

        :param sbox: объект SBox
        :return: степень нелинейности s-box
        """
        m = sbox.m
        min_nl = None

        # перебираем все ненулевые вектора A длины m
        for bits in product([0, 1], repeat=m):
            if all(b == 0 for b in bits):
                continue

            # строим линейную комбинацию компонентных функций
            combined = [0] * (2 ** sbox.n)
            for i_bit, b in enumerate(bits):
                if b:
                    fi_vals = sbox.basis[i_bit].values
                    # побитовый XOR по элементам
                    combined = [cv ^ fv for cv, fv in zip(combined, fi_vals)]

            bf = BooleanFunction(sbox.n, combined)
            nl = NonlinearityService.compute_nonlinearity(bf)

            if min_nl is None or nl < min_nl:
                min_nl = nl
                if min_nl == 0:  # оптимизация
                    return 0

        return int(min_nl if min_nl is not None else 0)
