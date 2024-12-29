def make_solution(self, pre_sol):
    """
    Обрабатывает массив pre_sol, заменяя уникальные числа на 0/1 и вычисляя значения строк.
    Сначала обрабатываем числа, затем строки (от наименьшей строки к наибольшей).
    Строки вида '3+5+6' обрабатываются как индексы и XOR-ятся.
    """
    # Находим количество уникальных целых чисел (не равных 0)
    unique_ints = list(set([item for item in pre_sol if isinstance(item, int) and item != 0]))
    how_much = len(unique_ints) * 2
    print(f"Количество уникальных целых чисел: {len(unique_ints)}, Итераций: {how_much}")

    # Разделяем элементы на числа и строки
    nums = [item for item in pre_sol if isinstance(item, int) and item != 0]
    strs = [item for item in pre_sol if isinstance(item, str)]

    # Сортируем строки по количеству элементов в выражении (по количеству индексов)
    strs.sort(key=lambda x: len(x.split('+')))  # Сортируем по количеству индексов в выражении

    # Создаем список для хранения всех возможных решений
    solutions = []

    # Генерация 0 и 1 для уникальных целых чисел
    for i in range(how_much):
        # Генерируем набор значений для уникальных чисел
        values = [int(x) for x in bin(i)[2:].zfill(len(unique_ints))]  # Бинарное представление
        mapping = dict(zip(unique_ints, values))  # Сопоставляем число с 0 или 1

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
                                result ^= current_solution[int(val)-1]

                            current_solution[j] = result
                            resolved = True
                        except Exception as e:
                            print(f"Ошибка вычисления выражения '{item}': {e}")
                            current_solution[j] = None  # Если ошибка, ставим None
        solutions.append(current_solution)

    return solutions


pre_sol = [0, '5+3+6', '1+6', 6, 5, 6]

# Вызов метода
solutions = make_solution(None, pre_sol)

# Вывод всех решений
for sol in solutions:
    print(sol)
