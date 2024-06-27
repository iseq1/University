import numpy as np
import matplotlib.pyplot as plt
from sklearn.datasets import fetch_california_housing

def gradient(X, z, w, learning_rate, num_iterations, alpha ):
    '''Функция для подсчёта весов градиентного спуска'''
    error_history = []
    for i in range(num_iterations):
        grad = (1 / len(z)) * (np.dot(X.T, np.dot(X, w) - z)) + alpha * w
        w -= learning_rate * grad

        error = calc_error(X,z,w)
        error_history.append(error)

        if i > 0 and abs(error_history[-1] - error_history[-2]) < alpha:
            print("достигнут критерий остановки по изменению ошибки - ГС закончен")
            break

        if np.linalg.norm(grad) < alpha:
            print("достигнут критерий остановки по норме градиента - ГС закончен")
            break
    return w, error_history


def calc_error(X, z, w):
    '''Вычисление ошибки'''
    error = np.sum((np.dot(X, w) - z) ** 2) / len(z)
    return error


def create_basis_matrix(x):
    '''Функция для создания матрицы базисных функций'''
    basis_matrix = np.hstack((np.ones((len(x), 1)), x, np.cos(x), np.sin(x))) #
    return basis_matrix



if __name__ == '__main__':
    alpha = 0.0000001
    boston = fetch_california_housing()
    x, z = boston.data, boston.target
    x = create_basis_matrix(x) # матрица базисныe функциb

    #  Шафлим 1 к 4 трен и тест
    count_desyatok = len(x) // 10
    train_indices = np.arange(0, 8 * count_desyatok)
    text_indices = np.arange(8 * count_desyatok, 10 * count_desyatok)

    # Стандартизация тренеровочных данных
    train_std = np.std(x[train_indices])
    train_mean = np.mean(x[train_indices])
    X_train = (x[train_indices] - train_mean) / train_std

    # стандартизация тестовых данных
    std_test = np.std(x[text_indices])
    mean_test = np.mean(x[text_indices])
    X_test = (x[text_indices] - mean_test) / std_test

    # условие
    iterations_count = 1000
    learning_rate = 0.01
    std0 = 0.1

    # начальное приближение в град.с.
    w = np.random.normal(0, std0, size=len(X_train[0]))
    w_train, error_history_train = gradient(X_train, z[train_indices], w, learning_rate, iterations_count, alpha)

    error_train = calc_error(X_train, z[train_indices], w_train)
    error_test = calc_error(X_test, z[text_indices], w_train)
    print("Ошибка на обучающей выборке:", error_train)
    print("Ошибка на тестовой выборке:", error_test)

    plt.plot(range(len(error_history_train)), error_history_train)
    plt.xlabel('Итерация')
    plt.ylabel('Ошибка')
    plt.title('Ошибка обучения в зависимости от итерации')
    plt.show()
