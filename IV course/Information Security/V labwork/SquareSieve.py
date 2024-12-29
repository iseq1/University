import math
from decimal import Decimal
import numpy as np


class SquareSieve:
    def __init__(self, smoothness_parameter=None, M=None):
        self.b_smooth = 100 if smoothness_parameter is None else smoothness_parameter
        self.b_smooth_list = self.get_b_smooth_list(self.b_smooth)
        self.M = 100 if M is None else M

    def get_b_smooth_list(self, b_smooth: int) -> list:
        '''
        Вычисление простых чисел до предела заданного B-гладкости

        :param b_smooth: Предел B-гладкости
        :return: Список простых чисел, чьи значения меньше предела B-гладкости
        '''
        # Создаем список, где индекс - это число, а значение - True (если оно простое) или False (если оно составное)
        sieve = [True] * (b_smooth + 1)
        sieve[0], sieve[1] = False, False  # 0 и 1 не простые числа

        for i in range(2, int(b_smooth ** 0.5) + 1):  # Перебираем числа до квадратного корня из limit
            if sieve[i]:  # Если i простое
                for j in range(i * i, b_smooth + 1, i):  # Отметить все кратные i как составные
                    sieve[j] = False

        return [i for i, is_prime in enumerate(sieve) if is_prime]

    def get_consider_value_list(self, n):
        ''''''
        x_range = np.arange(start=math.floor(math.sqrt(n)) + 1, stop=round(math.sqrt(n)) + 1 + self.M, step=1)
        consider_values = []
        for i in range(len(x_range)):
            # print(Decimal(int(x_range[i])**2), Decimal(int(n)))
            consider_values.append(Decimal(int(x_range[i])**2) - Decimal(int(n)))
            # consider_values.append((x_range[i] ** 2) - (n))
        consider_values = np.array(consider_values)

        return x_range, consider_values

    def check_square(self, lst):
        for index, item in enumerate(lst):
            if item>0:
                if math.sqrt(item) == math.floor(math.sqrt(item)):
                    return True, index, item
        return False

    def sifting(self, lst):
        sifting_list = []
        for item in lst:
            for prime_number in self.b_smooth_list:
                if item % prime_number == 0:
                    while item % prime_number == 0:
                        item = int(item)//int(prime_number)
            sifting_list.append(item)
        return np.array(sifting_list)

    def get_target_list(self, cv_lst, s_lst):
        return [int(cv_lst[i]) for i in np.where(s_lst == 1)[0]]

    def factorization_by_b_smooth(self, lst):
        factor_dict = {}
        for item in lst:
            factor_dict[item] = []
            cur_item = item
            for prime_number in self.b_smooth_list:
                if cur_item == 1:
                    continue
                if cur_item % prime_number == 0:
                    count = 0
                    while cur_item % prime_number == 0:
                        cur_item = int(cur_item)//int(prime_number)
                        count += 1
                    factor_dict[item].append((prime_number, count%2))
                else:
                    factor_dict[item].append((prime_number, 0))
        return factor_dict

    def make_matrix(self, target_dict):
        # Собираем все простые числа, которые встречаются в разложениях
        all_primes = set()
        for factors in target_dict.values():
            for prime, _ in factors:
                all_primes.add(prime)

        # Сортируем простые числа, чтобы они шли в определенном порядке
        all_primes = sorted(all_primes)

        # Создаем пустую матрицу с нужными размерами
        A_matrix = np.zeros((len(target_dict), len(all_primes)), dtype=int)

        # Заполняем матрицу
        for i, (num, factors) in enumerate(target_dict.items()):
            for prime, count in factors:
                if count % 2 != 0:  # Если степень нечетная (значит это простое число присутствует)
                    prime_index = all_primes.index(prime)  # Находим индекс простого числа
                    A_matrix[i, prime_index] = 1  # Ставим 1 в соответствующую ячейку матрицы

        return A_matrix.T

    def gaussian_elimination(self, A):
        m, n = A.shape
        row_used = np.zeros(m, dtype=int)  # Массив для отметки использованных строк

        for col in range(n):
            # Находим первую строку с единицей в текущем столбце
            pivot_row = -1
            for row in range(m):
                if A[row, col] == 1 and row_used[row] == 0:
                    pivot_row = row
                    break

            if pivot_row == -1:
                continue  # Если не нашли, переходим к следующему столбцу

            # Помечаем строку как использованную
            row_used[pivot_row] = 1

            # Применяем XOR для всех строк ниже, чтобы обнулить элементы в столбце
            for row in range(m):
                if row != pivot_row and A[row, col] == 1:
                    A[row] ^= A[pivot_row]  # XOR-им строку с ведущей единицей

        return A

    def find_basic_and_free_variables(self, A):
        """
        Находит базисные и свободные переменные после приведения матрицы A
        к ступенчатому виду. Базисные переменные имеют ведущие единицы.
        """
        m, n = A.shape
        basic_vars = []
        free_vars = []

        # Определяем базисные и свободные переменные
        for col in range(n):
            print(basic_vars, free_vars)
            found = False
            for row in range(m):
                if A[row, col] == 1 and row == col:
                    if row not in basic_vars:
                        basic_vars.append(row)
                        found = True
                        break
            if not found:
                free_vars.append(col)

        return basic_vars, free_vars

    def back_substitution(self, A, free_vars):
        """
        Выполняет подстановку для нахождения значений базисных переменных через
        свободные переменные.
        """
        m, n = A.shape
        solution = np.zeros(n, dtype=int)

        # Для каждой строки с ведущей единицей (базисной переменной)
        for row in range(m):
            # Если строка не нулевая
            if np.any(A[row] == 1):
                leading_one_pos = np.argmax(A[row])  # Позиция ведущей единицы
                if leading_one_pos not in free_vars:
                    # Строка с ведущей единицей выражает базисную переменную через свободные
                    # Применяем XOR с соответствующими переменными
                    sum_free_vars = 0
                    for col in range(n):
                        if col != leading_one_pos and A[row, col] == 1:
                            sum_free_vars ^= solution[col]  # XOR свободных переменных
                    solution[leading_one_pos] = sum_free_vars
        return solution

    # def generate_solutions(self, A, free_vars, basic_vars):
    #     """
    #     Генерирует все возможные решения системы, принимая свободные переменные
    #     как 0 или 1.
    #     """
    #     m, n = A.shape
    #     num_solutions = 2 ** len(free_vars)
    #     solutions = []
    #
    #     # Генерация всех комбинаций значений для свободных переменных
    #     for i in range(num_solutions):
    #         # Создаем маску для свободных переменных
    #         free_values = [int(x) for x in bin(i)[2:].zfill(len(free_vars))]
    #
    #         # Заполняем решение с учетом значений свободных переменных
    #         solution = np.zeros(n, dtype=int)
    #
    #         # Присваиваем значения для свободных переменных
    #         for j, free_var in enumerate(free_vars):
    #             solution[free_var] = free_values[j]
    #
    #         # Теперь подставим свободные переменные в уравнения для базисных переменных
    #         for row in basic_vars:
    #             leading_one_pos = np.argmax(A[row])  # Позиция ведущей единицы
    #             if leading_one_pos not in free_vars:
    #                 # Если ведущая единица не в свободных переменных, то это базисная переменная
    #                 sum_free_vars = 0
    #                 for col in range(n):
    #                     if col != leading_one_pos and A[row, col] == 1:
    #                         sum_free_vars ^= solution[col]  # XOR с соответствующими значениями
    #                 solution[leading_one_pos] = sum_free_vars
    #
    #         solutions.append(solution)
    #
    #     return solutions

    def generate_expressions(self, matrix, basis_vars, free_vars):
        """
        Генерирует выражения для переменных из базисных и свободных переменных.

        :param matrix: numpy-матрица (2D-массив), содержащая коэффициенты.
        :param basis_vars: список индексов базисных переменных.
        :param free_vars: список индексов свободных переменных.
        :return: словарь с выражениями для каждой переменной.
        """
        n_rows, n_cols = matrix.shape

        # Проверка, чтобы сумма количества базисных и свободных переменных равнялась числу столбцов
        if len(basis_vars) + len(free_vars) != n_cols:
            raise ValueError(
                "Сумма количества базисных и свободных переменных должна быть равна числу столбцов в матрице")

        expressions = {}
        pre_solution = {}

        for i, row in enumerate(matrix):
            # Проверить наличие базисной переменной в строке
            basis_indices_in_row = [j for j in basis_vars if row[j] == 1]
            if not basis_indices_in_row:
                continue  # Пропустить строки без базисной переменной

            # Предположим, что в строке только одна базисная переменная
            basis_index = basis_indices_in_row[0]

            # Найти все свободные переменные, которые есть в текущей строке
            free_indices = [j for j in range(n_cols) if j != basis_index and row[j] == 1]

            # Сформировать выражение
            if not free_indices:  # Если свободных переменных нет, значение переменной = 0
                expressions[f"x{basis_index + 1}"] = "0"
                pre_solution[basis_index] = 0
            else:  # Иначе переменная выражается через свободные
                free_terms = " ⊕ ".join([f"x{j + 1}" for j in free_indices])
                expressions[f"x{basis_index + 1}"] = free_terms
                pre_solution[basis_index] = [j for j in free_indices]

        pos = list(i + 1 for i in range(len(basis_vars) + len(free_vars)))
        for key in pre_solution.keys():
            if pre_solution[key] == 0:
                pos[key] = 0
            elif isinstance(pre_solution[key], list) and len(pre_solution[key]) == 1:
                pos[key] = pos[pre_solution[key][0]] = key + 1
            elif isinstance(pre_solution[key], list) and len(pre_solution[key]) > 1:
                pos[key] = "+".join([str(i + 1) for i in pre_solution[key]])

        return expressions, pos

    def make_solution(self, pre_sol):
        """
        Обрабатывает массив pre_sol, заменяя уникальные числа на 0/1 и вычисляя значения строк.
        Сначала обрабатываем числа, затем строки (от наименьшей строки к наибольшей).
        Строки вида '3+5+6' обрабатываются как индексы и XOR-ятся.
        """
        # Находим количество уникальных целых чисел (не равных 0)
        unique_ints = list(set([item for item in pre_sol if isinstance(item, int) and item != 0]))
        how_much = 2**len(unique_ints)
        print(f"Количество уникальных целых чисел: {len(unique_ints)}, Итераций: {how_much}")

        # Разделяем элементы на числа и строки
        # nums = [item for item in pre_sol if isinstance(item, int) and item != 0]
        # strs = [item for item in pre_sol if isinstance(item, str)]

        # Сортируем строки по количеству элементов в выражении (по количеству индексов)
        # strs.sort(key=lambda x: len(x.split('+')))  # Сортируем по количеству индексов в выражении

        # Создаем список для хранения всех возможных решений
        solutions = []

        # Генерация 0 и 1 для уникальных целых чисел
        for i in range(how_much):
            # Генерируем набор значений для уникальных чисел
            values = [int(x) for x in bin(i)[2:].zfill(len(unique_ints))]  # Бинарное представление
            mapping = dict(zip(unique_ints, values))  # Сопоставляем число с 0 или 1
            print(mapping)
            # Создаем копию массива и заменяем значения
            current_solution = pre_sol[:]

            # Обрабатываем числа сначала
            for j, item in enumerate(current_solution):
                if isinstance(item, int) and item != 0:
                    if item in mapping:
                        current_solution[j] = mapping[item]  # Заменяем числа на 0/1

            resolved = True
            while resolved:
                resolved = False  # Флаг, что были обработаны строки
                for j, item in enumerate(current_solution):
                    if isinstance(item, str):
                        # Проверяем, можем ли мы обработать строку (все элементы должны быть числами)
                        elements = item.split('+')
                        if all(isinstance(current_solution[int(el) - 1], int) for el in elements):
                            try:
                                elements = item.split('+')
                                result = 0
                                for val in elements:
                                    result ^= current_solution[int(val) - 1]

                                current_solution[j] = result
                                resolved = True
                            except Exception as e:
                                print(f"Ошибка вычисления выражения '{item}': {e}")
                                current_solution[j] = None  # Если ошибка, ставим None
            solutions.append(current_solution)

        return solutions

    def find_y(self, solution, target, n, x_list, consider_l):
        print(solution, target)
        print(len(solution))
        for item in solution:
            if sum(item)!=0:
                # тут получаем y, считаем Х, находим НОД(X − y, n), елси он чето то чето дургое кароче посмотри теорию
                y = math.sqrt(math.prod([j for i, j in zip(item,target) if i == 1]))
                if y == round(y):
                    solve = [j for i, j in zip(item,target) if i == 1]
                    if isinstance(consider_l, np.ndarray):
                        consider_l = consider_l.tolist()
                    indices = [consider_l.index(sol) for sol in solve]
                    X = math.prod([x_list[item] for item in indices])
                    print(X, y)
                    # НОД(X +− y, n)
                    nod_1 = math.gcd(X-int(y), n)
                    nod_2 = math.gcd(X+int(y), n)
                    if n not in [nod_1, nod_2] and 1 not in [nod_1, nod_2]:
                        return nod_1, nod_2
                else:
                    continue
            else:
                continue
        return None, None


    def factorization(self, n):
        # 1.
        x_list, consider_values_list = self.get_consider_value_list(n)
        print(x_list, consider_values_list)
        if not self.check_square(consider_values_list):
            print("Полных квадратов не нашлось")
            # 2. Решето Эратосфена
            sifted_list = self.sifting(consider_values_list)
            print(sifted_list)
            yield sifted_list
            target_list = self.get_target_list(consider_values_list, sifted_list)
            print(target_list)
            # target_list = [10, 24, 35, 52, 54, 78]
            factorization_target_dict = self.factorization_by_b_smooth(target_list)
            print(factorization_target_dict)
            A = self.make_matrix(factorization_target_dict)
            yield A
            print(A)
            A_reduced = self.gaussian_elimination(A)
            print(A_reduced)
            basic_vars, free_vars = self.find_basic_and_free_variables(A_reduced)
            print("Базисные переменные:", basic_vars)
            print("Свободные переменные:", free_vars)
            expressions, pre_solution = self.generate_expressions(A, basic_vars, free_vars)

            # Печать результатов
            for var, expr in expressions.items():
                print(f"{var} = {expr}")

            # Печать результатов
            print(pre_solution)
            solution = self.make_solution(pre_solution)
            yield solution
            print(solution)
            yield self.find_y(solution, target_list, n, x_list, consider_values_list)

        else:
            _, index, y_square = self.check_square(consider_values_list)
            x = x_list[index]
            print(f"Нашёлся полный квадрат: {y_square}")
            if x ** 2 - y_square == n:
                return int(x + math.sqrt(y_square)), int(x - math.sqrt(y_square))
            else:
                print("чёта ошибка тут какаято!")



ss = SquareSieve(29, 40)
# # ss.factorization(112093)
# # 875078015194165779807004996891
# 2945551046056896373232621994521
# p, q = ss.factorization(112093)
# print(p, q)
