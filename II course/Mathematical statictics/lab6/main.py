import csv
import math
import scipy

# Вариант Z11 (Z11: Построить доверительные границы для среднего значения нормального распределения)
# Q = 0.95
# Вид доверительной границы: Нижняя

# Интервальная оценка для среднего значения нормального распределения.
# Описание и теоретические аспекты выполнения см. в [1], задание 15.
# Отчёт должен содержать:
#   1. Объём выборки;
#   2. Выборочное среднее;
#   3. Стандартную ошибку среднего;
#   4. Вычисленный доверительный интервал.


x = []
with open('D:/failiki/university/2 курс/ТВИМС/5/r3z2.csv', 'r') as csvfile:
    reader = csv.reader(csvfile)
    next(reader)
    for row in reader:
        x.append(float(row[0]))

Q = 0.95
n = len(x)

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

def standard_deviation():  # стандартное отклонение
    return math.sqrt(biased_estimate())

def standard_error_of_the_mean():
    return standard_deviation() / math.sqrt(n)

# Вычисляем t-статистику для Q=0.95 и степеней свободы n-1
t = abs(scipy.stats.t.ppf((1 - Q), n - 1))

# Вычисляем доверительный интервал
def confidence_interval():
    return avg() - t * standard_error_of_the_mean()


print("x =", x)
print("Объем выборки = ", n)
print("Выборочное среднее = ", avg())
print("Стандартная ошибка среднего = ", standard_error_of_the_mean())
print("t = ", t)
print("Доверительный интервал ({:.2f}%): ({}, ∞)".format(Q * 100, confidence_interval()))
