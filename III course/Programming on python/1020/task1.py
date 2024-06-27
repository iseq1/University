# m, n =3,4
# a = [[0]*3 for _ in range(m)]
# o=1
#
# # for i in range(len(a)):
# #     for j in range(len(a[i])):
# #         a[i][j]=o
# #         o+=1
# # for row in a:
# #     for item in row:
# #         item
# k=-1
#
# a = [list(range(i*n+1,i*n+n+1, (-1)**(i%2))) for i in range(m)]
#
# print(a)

def fill_spiral_matrix(n):
    matrix = [[None] * n for _ in range(n)]
    directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]
    direction = 0
    i, j = 0, 0

    for num in range(1, n ** 2 + 1):
        matrix[i][j] = num
        next_i, next_j = i + directions[direction][0], j + directions[direction][1]

        if 0 <= next_i < n and 0 <= next_j < n and matrix[next_i][next_j] is None:
            i, j = next_i, next_j
        else:
            direction = (direction + 1) % 4
            i, j = i + directions[direction][0], j + directions[direction][1]

    return matrix


size = 5
matrix = fill_spiral_matrix(size)
for row in matrix:
    print(row)