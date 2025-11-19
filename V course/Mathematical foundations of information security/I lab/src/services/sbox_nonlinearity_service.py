# src/services/sbox_nonlinearity_service.py
from itertools import product
from src.models.sbox import SBox
from src.models.boolean_function import BooleanFunction
from src.services.nonlinearity_service import NonlinearityService

class SBoxNonlinearityService:
    """
    Степень нелинейности s-box как в лекции:
    NL(S) = min_{A != 0 in F2^m} NL( f_A ), где f_A = ⊕ ai * fi
    """
    @staticmethod
    def compute_sbox_nonlinearity(sbox: SBox) -> int:
        m = sbox.m
        min_nl = None
        # перебираем все ненулевые вектора A
        for bits in product([0,1], repeat=m):
            if all(b == 0 for b in bits):
                continue
            # комбинируем значения базовых функций
            combined = [0] * (2 ** sbox.n)
            for i_bit, b in enumerate(bits):
                if b:
                    fi_vals = sbox.basis[i_bit].values
                    # XOR поэлементно
                    combined = [ (cv ^ int(fv)) for cv, fv in zip(combined, fi_vals) ]
            bf = BooleanFunction(sbox.n, combined)
            nl = NonlinearityService.compute_nonlinearity(bf)
            if min_nl is None or nl < min_nl:
                min_nl = nl
                if min_nl == 0:
                    return 0
        return int(min_nl if min_nl is not None else 0)
