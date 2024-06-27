import numpy as np
import pandas as pd
import matplotlib as mpl
import matplotlib.pyplot as plt
import math
import csv
mpl.use('TkAgg')

data = []

with open('D:/failiki/university/2 курс/ТВИМС/5/r4z2.csv', 'r') as csvfile:
    reader = csv.reader(csvfile)
    next(reader)
    for row in reader:
        data.append([float(row[0]), float(row[1])])

print(data)

x = [i[0] for i in data]
print("x = ", x)

y = [i[1] for i in data]
print("y = ", y)

def Average(x): #Среднее
    avg = 0
    for i in x:
        avg+=i
    return avg/len(x)
print("average(x) = ", Average(x))
print("average(y) = ", Average(y))

def Shifted_dispersion(x): #Смещённая дисперсия
    disp = 0
    for i in range(0, len(x)):
        disp+= (x[i]-Average(x))**2
    return disp/len(x)
print("Disoersia(x) = ", Shifted_dispersion(x))
print("Dispersia(y) = ", Shifted_dispersion(y))

def Standard_deviation(x): #Стандартное отклонение
    return math.sqrt(Shifted_dispersion(x))
print("otklon(x) = ", Standard_deviation(x))
print("otklon(y) = ", Standard_deviation(y))

def cor(x, y):
    cov = 0
    n = min(len(x), len(y))
    for i in range(n):
        cov+=((x[i] - Average(x))*(y[i]-Average(y)))
    cov = cov/len(x)
    return cov/(Standard_deviation(x)*Standard_deviation(y))

r = cor(x,y)
print("cor(x,y) = ", r)

# x(y) = a*y + b
# x(y) = X + b_(x/y) * (y -Y) -> x(y) = b_(x/y) * y + ( X - Y * b_(x/y) ) -> a=b_(x/y), b= X - Y*b_(x/y)

a = r*(Standard_deviation(x)/Standard_deviation(y))
b = Average(x) - r*(Standard_deviation(x)/Standard_deviation(y))*Average(y)

print("\n a = ", a,
      "\n b = ", b)
print("\n X(76) = ", 76*a+b)

plt.scatter([i[0] for i in data],[i[1] for i in data])
plt.plot([i*a+b for i in y], y, color='red')
plt.show()
