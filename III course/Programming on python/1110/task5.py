# for row in m:
#     for number in row:
#         print(number, end=' ')
#     print()
#
# for row in m:
#     s = [str(n) for n in row]
#     print(' '.join(s))
#
# for row in m:
#     print(' '.join([str(n) for n in row]))


m = [
[1, 2, 3, 4],
[56789, 78, 9, 0]
]



def str_row(row):
    return ' '.join([str(row[i]).ljust(len(str(max([x[i] for x in m])))) for i in range(len(row))])

print('\n'.join([str_row(row) for row in m]))
