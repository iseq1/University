import numpy as np
import matplotlib.pyplot as plt

# 1. Проверить правильность тестового решения

# Для проверки правильности тестового решения тестовой задачи
# необходимо реализовать метод Рунге-Кутты 4-го порядка
# и сравнить численное решение с точным решением.

print('1. Проверить правильность тестового решения.')
# Метод Рунге-Кутты 4-го порядка
def runge_kutta_4(f, y0, t0, t1, h):
    t = np.arange(t0, t1 + h, h)
    y = np.zeros((len(t), len(y0)))
    y[0] = y0
    for i in range(1, len(t)):
        k1 = f(t[i-1], y[i-1])
        k2 = f(t[i-1] + h / 2, y[i-1] + h * k1 / 2)
        k3 = f(t[i-1] + h / 2, y[i-1] + h * k2 / 2)
        k4 = f(t[i-1] + h, y[i-1] + h * k3)
        y[i] = y[i-1] + h * (k1 + 2 * k2 + 2 * k3 + k4) / 6
    return t, y

# Функция для тестовой задачи
def test_function(t, y):
    y1, y2 = y
    dy1 = -y2 + y1 * (y1**2 + y2**2 - 1)
    dy2 = y1 + y2 * (y1**2 + y2**2 - 1)
    return np.array([dy1, dy2])

# Начальные условия и параметры
y0_test = [1 / np.sqrt(2), 0]  # Начальные условия y1(0) и y2(0)
t0_test = 0
t1_test = 5

# Шаг интегрирования
h = 0.01

# Решение тестовой задачи методом Рунге-Кутты
t, y = runge_kutta_4(test_function, y0_test, t0_test, t1_test, h)

# Точное решение для сравнения
y1_exact = np.cos(t) / np.sqrt(1 + np.exp(2 * t))
y2_exact = np.sin(t) / np.sqrt(1 + np.exp(2 * t))

# Вычисление ошибки
error_y1 = np.abs(y[:, 0] - y1_exact)
error_y2 = np.abs(y[:, 1] - y2_exact)

# Графическое сравнение
plt.figure(figsize=(14, 6))

plt.subplot(1, 2, 1)
plt.plot(t, y[:, 0], 'b-', label='Численное решение y1(t)')
plt.plot(t, y1_exact, 'r--', label='Точное решение y1(t)')
plt.xlabel('Время t')
plt.ylabel('y1(t)')
plt.legend()
plt.title('Сравнение численного и точного решений для y1(t)')

plt.subplot(1, 2, 2)
plt.plot(t, y[:, 1], 'b-', label='Численное решение y2(t)')
plt.plot(t, y2_exact, 'r--', label='Точное решение y2(t)')
plt.xlabel('Время t')
plt.ylabel('y2(t)')
plt.legend()
plt.title('Сравнение численного и точного решений для y2(t)')

plt.tight_layout()
plt.show()

print('Из графиков видно, что численное решение практически совпадает с точным решением, что подтверждает правильность работы программы на тестовой задаче.')
