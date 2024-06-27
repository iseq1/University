import csv
import math

x = []
with open('D:/failiki/university/2 курс/ТВИМС/5/r3z1.csv', 'r') as csvfile:
    reader = csv.reader(csvfile)
    next(reader)
    for row in reader:
        x.append(float(row[0]))

print("x =", x, "\n")

def m1(x):  # среднее
    avg = 0
    for i in x:
        avg += i
    return avg / len(x)

def m2(x):  # среднее^2
    avg = 0
    for i in x:
        avg += i**2
    return avg / len(x)

def tet(x):
    return 1 + math.sqrt(1 + ((m1(x) * m1(x)) / (m2(x) - (m1(x) * m1(x)))))

def x0(x):
    return m1(x) * (tet(x) - 1)/tet(x)

print("Оценка параметра x0 = ", x0(x))
print("Оценка параметра θ = ", tet(x))