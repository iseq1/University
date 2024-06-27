import csv
import math
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
import pylab


mpl.use('TkAgg')

y = []

with open('D:/failiki/university/2 курс/ТВИМС/5/r4z2.csv', 'r') as csvfile:
    reader = csv.reader(csvfile)
    next(reader)
    for row in reader:
        y.append(float(row[0]))

x = [-2.6, 5.41, 0.73, -0.12, 3.21]
x = sorted(x)
n = len(x)
razmax = x[n - 1] - x[0]
print(x)


def avg():
    avg = 0
    for i in x:
        avg += i
    return avg / n


def biased_estimate():  # смещенная оценка - дисперсия
    s = 0
    for i in x:
        s += (i - avg()) ** 2
    return s / n


def unbiased_estimate():  # несмещенная оценка - дисперсия
    return biased_estimate() * n / (n - 1)


def standard_deviation():  # стандартное отклонение
    return math.sqrt(biased_estimate())


def coef_asym():  # коэф асимметрии
    k = 0
    for i in x:
        k += (i - avg()) ** 3
    return k / (n * (standard_deviation()) ** 3)


def med():  # медиана
    if n % 2 == 0:
        return (x[int(n / 2)] + x[int(n / 2 - 1)]) / 2
    return x[int(n / 2)]


def inter_lat():  # интерквартильная широта
    if n % 4 == 0:
        nkvart = (x[n // 4] + x[n // 4 - 1]) / 2
        vkvart = (x[3 * n // 4] + x[3 * n // 4 - 1]) / 2
    else:
        nkvart = x[n // 4]
        vkvart = x[3 * n // 4]
    return vkvart - nkvart


def koef_ecc():  # коэф эксцесса
    koef = 0
    for i in x:
        koef += (i - avg()) ** 4
    return (koef / (n * (standard_deviation() ** 4))) - 3


print("=========")
print("Объем выборки = ", n)
print("Минимум = ", x[0])
print("Максимум = ", x[n - 1])
print("Размах = ", razmax)
print("Среднее = ", avg())
print("Смещенная оценка = ", biased_estimate())
print("Несмещенная оценка = ", unbiased_estimate())
print("Стандартное отклонение = ", standard_deviation())
print("Коэффицент асимметрии = ", coef_asym())
print("Коэффицент эксцесса = ", koef_ecc())
print("Медиана = ", med())
print("Интерквартильная широта = ", inter_lat())
print("=========")

k = int(1 + 3.222 * np.log10(n))  # кол-во интервалов по формуле стерджесса
dl_intervala = razmax / k  # длина одного интервала

otrezki = [x[0]]  # контейнер с точками начала отрезков
for i in range(1, k):
    otrezki.append(otrezki[i - 1] + dl_intervala)

h = []  # контейнер с высотами гистограммы
for j in range(k):
    count = 0
    for i in x:
        if i >= otrezki[j] and i < otrezki[j] + dl_intervala:
            count += 1
    h.append(count / (n * dl_intervala))

y = []  # y функции нормального распределения
for i in range(len(x)):
    y.append((1 / (standard_deviation() * np.sqrt(2 * np.pi))) * np.exp(
        -((x[i] - avg()) ** 2) / (2 * (standard_deviation() ** 2))))

j = 0
for i in range(len(h)):
    if h[i] == max(h):
        j = i
print("Середина отрезка самого высокого столба гистограммы примерно равна моде = ", otrezki[j] + dl_intervala / 2)

pylab.subplot(1, 2, 1)
pylab.title("Гистограмма")
pylab.plot(x, y, 'k', lw=2)  # нормальное распределение
pylab.bar(otrezki, h, width=dl_intervala, align="edge")  # вероятностная гистограмма
pylab.grid()

print("=========")
counter = []  # контейнер [число, сколько раз встречается]
for i in sorted(set(x)):
    count = 0
    for j in x:
        if i == j:
            count += 1
    counter.append([i, count])
sorted(counter)
counter.insert(0, [counter[0][0] - 1, 0])  # добавляем первый элемент для первого отрезка

p = []  # контенйер для частот
for i in range(len(counter)):
    p.append(counter[i][1] / n)
for i in range(1, len(p)):
    p[i] = p[i] + p[i - 1]
counter.append([counter[len(counter) - 1][0] + 1, 0])  # добавляем последний элемент для последнего отрезка

pylab.subplot(1, 2, 2)
pylab.title("ЭФР")
for i in range(len(p)):
    pylab.plot([counter[i][0], counter[i + 1][0]], [p[i], p[i]], color='green')
pylab.grid()

pylab.show()