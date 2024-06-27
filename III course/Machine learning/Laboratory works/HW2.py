import numpy as np
import matplotlib.pyplot as plt
import random


def Polynom(x):
    #  Возвращаем матрицу, в которой каждый столбец содержит значения степеней от 1 до 100 для каждого элемента массива
    polinom = [x ** i for i in range(1, 101)]
    global pol_grad
    pol_grad = random.randint(0,99)
    pol = polinom[pol_grad]
    return pol

def create_basis_matrix(x, functions):
    basis_matrix = np.ones((len(x), len(functions)))
    for i, func in enumerate(functions):
        if func == 'sin':
            basis_matrix[:, i] = np.sin(x)
        elif func == 'cos':
            basis_matrix[:, i] = np.cos(x)
        elif func == 'sin2':
            basis_matrix[:, i] = np.sin(x*2)
        elif func == 'cos2':
            basis_matrix[:, i] = np.cos(x*2)
        elif func == 'sinsin':
            basis_matrix[:, i] = np.sin(x**2)
        elif func == 'coscos':
            basis_matrix[:, i] = np.cos(x**2)
        elif func == 'exp':
            basis_matrix[:, i] = np.exp(x)
        elif func == 'sqrt':
            basis_matrix[:, i] = np.sqrt(x)
        elif func == 'cosh':
            basis_matrix[:, i] = np.cosh(x)
        elif func == 'sinh':
            basis_matrix[:, i] = np.sinh(x)
        elif func == 'tanh':
            basis_matrix[:, i] = np.tanh(x)
        elif func == 'tan':
            basis_matrix[:, i] = np.tan(x)
        elif func == 'polinom':
            basis_matrix[:, i] = Polynom(x)
        else:
            raise ValueError("Unknown basis function")
    return basis_matrix




def Lambda():
    # Создаем список, который содержит различные значения коэффициента регуляризации(alpha) для использования в регрессии с регуляризацией
    lambda_list = [np.power(0.1, 10), np.power(0.1, 9), np.power(0.1, 8),
                   np.power(0.1, 7), np.power(0.1, 6), np.power(0.1, 5),
                   np.power(0.1, 4), np.power(0.1, 3), np.power(0.1, 2),
                   np.power(0.1, 1), 0.5, 1, 10, 50, 500, 1000]
    return lambda_list


def ShuffleAndDistribution(N, x, t):
    # Создаем индексы и перемешиваем их
    indices = np.arange(N)
    np.random.shuffle(indices)

    # Применяем перемешанные индексы к массивам x и t
    x_shuffled = x[indices]
    t_shuffled = t[indices]

    size = len(x_shuffled)

    # Индексы для каждой части
    train_indices = np.arange(0, int(0.7 * size))
    validation_indices = np.arange(int(0.7 * size), int(0.7 * size) + int(0.15 * size))
    test_indices = np.arange(int(0.7 * size) + int(0.15 * size), size)

    # Разбиение данных
    x_train, t_train = x_shuffled[train_indices], t_shuffled[train_indices]
    x_validation, t_validation = x_shuffled[validation_indices], t_shuffled[validation_indices]
    x_test, t_test = x_shuffled[test_indices], t_shuffled[test_indices]
    return x_train, t_train, x_validation, t_validation, x_test, t_test




def SelectionBestParameters(x_train, t_train, x_validation, t_validation, N, MinError):
    function_list = ['sin', 'cos', 'exp', 'sqrt', 'cosh', 'sinh', 'tanh', 'tan', 'cos2', 'sin2', 'polinom']
    lambda_list = Lambda()

    w_best, best_basis, alpha_best = None, None, None

    for i in range(0, 20):
        # Случайный выбор числа базисных функций
        num_functions = np.random.randint(3, 9)
        # Случайный выбор базисных функций без повторений
        selected_functions = np.random.choice(function_list, size=num_functions, replace=False)
        # Формирование базисных функций
        bases = [1] + list(selected_functions)
        # Построение матриц базисных функций
        # Строим матрицы базисных функций для тренировочной и валидационной выборок
        F_train = np.column_stack([np.ones(len(x_train))] + [create_basis_matrix(x_train, selected_functions)])
        F_validation = np.column_stack([np.ones(len(x_validation))] + [create_basis_matrix(x_validation, selected_functions)])
        I = np.eye(np.shape(np.transpose(F_train) @ F_train)[0])

        # Подбор параметров модели
        for alpha in lambda_list:
            # Параметр модели
            w = np.linalg.inv(np.transpose(F_train) @ F_train + alpha * I) @ np.transpose(F_train) @ t_train
            # Ошибка на валидационной выборке
            Error_validation = 1 / N * np.sum((t_validation - F_validation @ np.transpose(w)) ** 2)
            if Error_validation < MinError:
                w_best = w
                best_basis = bases
                alpha_best = alpha
                MinError = Error_validation

    return function_list, w_best, best_basis, alpha_best, MinError

def CalcError(x_test, t_test, w_best, best_basis, N):
    # Вычисление ошибки на тестовой выборке

    # Строим матрицу базисных функций для тестовой выборки
    F_test = np.column_stack([np.ones(len(x_test))] + [create_basis_matrix(x_test, best_basis[1:])])
    # Вычисляем ошибку на тестовой выборке с использованием найденных параметров модели
    E_test = 1 / N * np.sum((t_test - F_test @ np.transpose(w_best)) ** 2)
    return E_test

def PredictingValues(x, b_best, w_best):
    # Предсказываем значеня целевой переменной для новых данных

    # Строим матрицу базисных функций для новых данных
    F_new = np.column_stack([np.ones(len(x))] + [create_basis_matrix(x, b_best[1:])])
    # Вычисляем предсказанные значения целевой переменной y для новых данных с использованием найденных параметров модели
    y = F_new @ w_best
    return y

def BestFunctions(best_basis, function_list):
    if '1' in best_basis:
        if 'polinom' in best_basis:
            index_to_replace = best_basis.index('polinom')
            best_basis[index_to_replace] = f'x^{pol_grad}'
        print("Набор лучших базисных функций: ", '1', best_basis[1:])
    else:
        if 'polinom' in best_basis:
            index_to_replace = best_basis.index('polinom')
            best_basis[index_to_replace] = f'x^{pol_grad}'
        print("Набор лучших базисных функций: ", best_basis)


def GraphPlot(x,z,t,y):
    plt.plot(x, z, color='indigo',  label='True Function', linewidth=2)
    plt.scatter(x, t, color='olive', alpha=0.5, label='Data Points')
    plt.plot(x, y, color='firebrick', label='Regression', linewidth=2)
    plt.legend()
    plt.show()


if __name__ == '__main__':
    # Условие
    N = 1000
    x = np.linspace(0, 1, N)
    z = 20 * np.sin(2 * np.pi * 3 * x) + 100 * np.exp(x)
    error = 10 * np.random.randn(N)
    t = z + error

    # lambda_list = Lambda()
    x_train, t_train, x_validation, t_validation, x_test, t_test = ShuffleAndDistribution(N, x, t)
    MinError = float('inf')
    function_list, w_best, best_basis, alpha_best, MinError = SelectionBestParameters(x_train, t_train, x_validation, t_validation, N, MinError)
    E_test = CalcError(x_test, t_test, w_best, best_basis, N)
    y = PredictingValues(x, best_basis, w_best)
    print("||======================||======================||======================||======================||")
    print("Значение ошибки на test части: ", E_test)
    print("||======================||======================||======================||======================||")
    print("Лучший коэффицент регуляризации: ", f'{alpha_best:.10f}')
    print("||======================||======================||======================||======================||")
    BestFunctions(best_basis, function_list)
    print("||======================||======================||======================||======================||")

    GraphPlot(x,z,t,y)