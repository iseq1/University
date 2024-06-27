
from task3 import *

# Начальные условия
x0 = 2
y0 = 2

# Список значений параметра p
p_values = np.linspace(0.001, 0.2, 10)

plt.figure(figsize=(12, 10))

for p in p_values:
    # Функция правых частей системы уравнений
    def f(t, y):
        x1, x2 = y
        dx1_dt = x2 - p * x1 * (x1 ** 2 + x2 ** 2 - 1)
        dx2_dt = -x1 - p * x2 * (x1 ** 2 + x2 ** 2 - 1)
        return np.array([dx1_dt, dx2_dt])

    # Решение системы уравнений методом Рунге-Кутты
    t, y = runge_kutta_4_system(f, [x0, y0], 0, 20, 0.01)

    # Графики траекторий в фазовом пространстве
    plt.subplot(2, 1, 1)
    plt.plot(y[:, 0], y[:, 1], label=f'p={p}')
    plt.xlabel('$x_1$')
    plt.ylabel('$x_2$')
    plt.title('Траектории в фазовом пространстве')
    plt.legend()

    # Графики x1(t) и x2(t)
    plt.subplot(2, 1, 2)
    plt.plot(t, y[:, 0], label=f'$x_1$, p={p}')
    plt.plot(t, y[:, 1], label=f'$x_2$, p={p}')
    plt.xlabel('Время t')
    plt.ylabel('Значение')
    plt.title('Графики $x_1(t)$ и $x_2(t)$')
    plt.legend()

plt.tight_layout()
plt.show()
