import csv
import math
import matplotlib.pyplot
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
import pylab
import scipy
from scipy import stats
from scipy.stats import expon, kstest
mpl.use('TkAgg')

#Вариант Z5 (Критерий согласия Колмогорова)
#α = 0.05
#H0: X ∼ E(λ = 1.5)

x = []
with open('D:/failiki/university/2 курс/ТВИМС/5/r2z2.csv', 'r') as csvfile:
    reader = csv.reader(csvfile)
    next(reader)
    for row in reader:
        x.append(float(row[0]))
print("x =", x)

def avg(x):  # среднее
    avg = 0
    for i in x:
        avg += i
    return avg / len(x)

def avg2(x):  # среднее
    avg = 0
    for i in x:
        avg += i**2
    return avg / len(x)

def biased_estimate(x):  # дисперсия
    s = 0
    for i in x:
        s += (i - avg(x)) ** 2
    return s / len(x)

def standard_deviation(x):
    return math.sqrt(biased_estimate(x))

# Исходные данные
alpha = 0.05
lambda_ = 1.5
H0 = 'X ~ E(lambda=1.5)'
y = sorted(x)
x_min = y[0]
x_max = y[len(x)-1]

# Определяем размер выборки
n = len(x)

# Определяем критическую константу
temp = np.sqrt(-0.5 * np.log(alpha / 2))
t_critical = 1.36 / np.sqrt(n)
print(f'Критическая константа: {t_critical}')
print("Вид критической области: t >", t_critical)

# Вычисляем значение статистики и p-значение
kstest_result = kstest(x, expon(loc=0, scale=1/lambda_).cdf)
stat_val = kstest_result.statistic
p_val = kstest_result.pvalue
print(f'Значение статистики Колмогорова: {stat_val}')
print(f'p-значение: {p_val}')

# выводим результаты
if stat_val > t_critical:
    print(f'Гипотеза H0 отклоняется на уровне значимости {alpha}, статистика Колмогорова-Смирнова = {stat_val:.4f}, p-значение = {p_val:.20f}')
else:
    print(f'Гипотеза H0 принимается на уровне значимости {alpha}, статистика Колмогорова-Смирнова = {stat_val:.4f}, p-значение = {p_val:.20f}')

expras = []
for i in range(len(x)):
    F = 1 - math.exp(x[i]*(-lambda_))
    expras.append(F)

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

# Строим график ЭФР
p = []  # контенйер для частот
for i in range(len(counter)):
    p.append(counter[i][1] / n)
for i in range(1, len(p)):
    p[i] = p[i] + p[i - 1]
counter.append([counter[len(counter) - 1][0] + 1, 0])  # добавляем последний элемент для последнего отрезка
for i in range(len(p)):
    pylab.plot([counter[i][0], counter[i + 1][0]], [p[i], p[i]], color='green')
pylab.plot(0, 0, color='green', label = "edf")
pylab.grid()

# Строим график функции распределения предполагаемого распределения
x_range = np.linspace(x_min, x_max, 1000)
y_cdf = expon.cdf(x_range, loc=0, scale=1/1.5)
plt.plot(x_range, y_cdf, 'r-', lw=2, alpha=0.6, label='exponential cdf')

# Строим график ЭФР
#y_ecdf = np.arange(1, len(x) + 1) / len(x)
#plt.step(np.sort(x), y_ecdf, where='post', label='empirical cdf')

plt.legend(loc='best')
plt.show()


print(avg(x)**2, "\n",  avg2(x))
