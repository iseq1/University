def sort_parallel_diagonals(matrix):
    rows = len(matrix)
    cols = len(matrix[0])

    # Собираем элементы с каждой диагонали в список
    diagonals = []
    for i in range(cols):
        diagonal = []
        for j in range(min(i, rows), max(0, i - cols), -1):
            diagonal.append(matrix[j][i - j])
        diagonals.append(sorted(diagonal))

    for i in range(1, rows):
        diagonal = []
        for j in range(min(cols - 1, rows - i), max(0, cols - i - 1), -1):
            diagonal.append(matrix[j + i][j])
        diagonals.append(sorted(diagonal))

    # Обновляем матрицу с отсортированными элементами на диагоналях
    for i in range(cols):
        for j in range(min(i, rows), max(0, i - cols), -1):
            matrix[j][i - j] = diagonals[i].pop(0)

    for i in range(1, rows):
        for j in range(min(cols - 1, rows - i), max(0, cols - i - 1), -1):
            matrix[j + i][j] = diagonals[i + cols - 1].pop(0)

    return matrix

# Пример использования
matrix = [
    [3, 8, 4],
    [1, 5, 9],
    [6, 7, 2]
]

sorted_matrix = sort_parallel_diagonals(matrix)
for row in sorted_matrix:
    print(row)
