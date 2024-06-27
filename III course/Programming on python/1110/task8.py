def align(matrix, alignment):
    if not matrix:
        print("Матрица пуста.")
        return

    # Получаем количество столбцов в матрице
    num_columns = len(matrix[0])

    # Инициализируем список для хранения длин столбцов
    column_widths = [0] * num_columns

    # Находим максимальную длину для каждого столбца
    for col in range(num_columns):
        column_data = [str(row[col]) for row in matrix]
        column_widths[col] = max(len(data) for data in column_data)

    # Выводим матрицу с выравниванием
    for row in matrix:
        for col in range(num_columns):
            data = str(row[col])
            align = alignment[col]

            if align == 'l':
                print(data.ljust(column_widths[col]), end=' ')
            elif align == 'c':
                print(data.center(column_widths[col]), end=' ')
            elif align == 'r':
                print(data.rjust(column_widths[col]), end=' ')
            else:
                print("Неверный тип выравнивания. Используйте 'l', 'c' или 'r'.")
                return

        print()  # Переход на новую строку после каждой строки матрицы

# Пример использования
matrix = [
    [1234, 5, 678],
[1, 234, 5]
]

align(matrix, 'lcr')
