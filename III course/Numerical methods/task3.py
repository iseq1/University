def calculate_error(y_numerical, y_exact):
    return np.max(np.abs(y_numerical - y_exact))


from task1 import *
from task2 import *

# Список значений шага h
h_values = [0.0001, 0.005, 0.01, 0.05, 0.1, 0.5]

# Список для сохранения максимальной погрешности e и e/h
errors = []
errors_over_h = []
a_test = 0
b_test = 5
for h in h_values:
    # Решение тестовой задачи методом Рунге-Кутты
    t, y_numerical = runge_kutta_4_system(test_function, y0_test, a_test, b_test, h)

    # Точное решение
    y1_exact = np.cos(t) / np.sqrt(1 + np.exp(2 * t))
    y2_exact = np.sin(t) / np.sqrt(1 + np.exp(2 * t))
    y_exact = np.array([y1_exact, y2_exact]).T

    # Расчет погрешности
    error = calculate_error(y_numerical, y_exact)
    errors.append(error)

    # Расчет погрешности, нормированной на шаг h
    error_over_h = error / h
    errors_over_h.append(error_over_h)

# Построение графиков
plt.figure(figsize=(12, 6))
plt.subplot(1, 2, 1)
plt.gca().invert_xaxis()
plt.plot(h_values, errors)
plt.title('Зависимость максимальной погрешности $e$ от шага $h$')
plt.xlabel('Шаг $h$')
plt.ylabel('Максимальная погрешность $e$')

plt.subplot(1, 2, 2)
plt.gca().invert_xaxis()
plt.plot(h_values, errors_over_h)
plt.title('Зависимость $e/h$ от шага $h$')
plt.xlabel('Шаг $h$')
plt.ylabel('$e/h$')

plt.tight_layout()
plt.show()
