import numpy as np
import matplotlib.pyplot as plt


def Regression(N, x, t):
    y = []
    M = [1, 8, 100]
    for item in M:
        F = np.ones((N, item+1))
        for i in range(N):
            for j in range(item+1):
                F[i][j] = x[i] ** j

        # w = np.linalg.inv(F.T @ F) @  F.T @ t
        w = np.linalg.pinv(F) @ t
        y.append(F @ w)
    return y

def Errors(N, x, t):
    errors=[]
    for M in range(1,101):
        F = np.ones((N,M+1))
        for i in range(N):
            for j in range(M+1):
                F[i][j] = x[i]**j
        F_plus = np.linalg.inv(F.T @ F) @ F.T
        w = F_plus @ t
        y = F @ w
        error = sum((t-y) **2 )/2
        errors.append(error)

    return errors

def PlotGraphics(x, t, y, errors):
    # Создание общего окна для всех графиков
    fig, axs = plt.subplots(2, 2, figsize=(12, 10))
    for idx, M in enumerate([1,8,100]):
        ax = axs[idx // 2, idx % 2]
        ax.plot(x, y[idx], label='y(x)', c='g', linewidth=2)
        ax.scatter(x, t, s=5, c='orange', label='t(x)', alpha=0.5)
        ax.set_title(f'M={M}')
        ax.legend()

    axs[1, 1].plot(range(1, 101), errors, c='g', linewidth=2)
    axs[1, 1].set_xlabel('Degree of polynomial M')
    axs[1, 1].set_ylabel('Error E(w)')
    axs[1, 1].set_title('Error vs Degree of Polynomial')

    plt.tight_layout()
    plt.show()

if __name__ == '__main__':
    N = 1000
    x = np.linspace(0, 1, N)
    z = 20 * np.sin(2 * np.pi * 3 * x) + 100 * np.exp(x)
    error = 10 * np.random.randn(N)
    t = z + error
    y = Regression(N,x,t)
    errors = Errors(N,x,t)
    PlotGraphics(x,t,y, errors)

