import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import time
# from scipy.stats import norm


start_time = time.time()

file_path = 'Bd_Titanik.xlsx'

data = pd.read_excel(file_path, skiprows=3)
data = data.iloc[3:, :]
normalized_data = (data - data.mean()) / data.std()
# print(normalized_data)

tetta = [0, 0, 0, 0, 0, 0, 0]
l = [0, 0, 0, 0, 0, 0, 0]
n = 0.01
print("Размер шага:", n)

y = [0] * data.shape[0]
for i in range(0, data.shape[0]):
    y[i] = data.iloc[i, 0]


def L(j):
    global n, l
    tetta[j] = tetta[j - 1] + n * l[j - 1]
    return tetta[j]

for j in range(0, 7):
    if j == 0:
        normalized_data.iloc[:, j] = 1
    if j != 0:
        tetta[j] = L(j)
    sum_result = 0
    for i in range(0, normalized_data.shape[0] - 1):
        sum_result += (y[i] - 1 / (1 + np.exp(-tetta[j] * normalized_data.iloc[i, j]))) * normalized_data.iloc[i, j]
    l[j] = sum_result


print("Значение параметра Тетта:",tetta)
sum_result = 0

for i in range(0, 7):
    if i == 0:
        normalized_data.iloc[:, i] = 1

    for j in range(0, normalized_data.shape[0] - 1):
        result_vector = np.dot(tetta, normalized_data.iloc[j,])
        sum_result += np.log(
            ((1 / (1 + np.exp(-result_vector))) ** y[j]) * ((1 / (1 + np.exp(result_vector))) ** (1 - y[j])))


print("Значение l(tetta):", sum_result)
theta_hat = np.array(tetta)
mu_approx = np.mean(theta_hat)
sigma_approx = np.std(theta_hat, ddof=1)

normal_distribution = np.random.normal(loc=mu_approx, scale=sigma_approx, size=10000)
end_time = time.time()
duration = end_time - start_time
plt.figure(figsize=(10, 6))
sns.histplot(theta_hat, bins=20, kde=True, color='blue')
sns.histplot(normal_distribution, bins=20, kde=True, color='green')

plt.legend()
plt.show()


print("Время, затраченное на выполнение программы:", duration, "мс")

live = int(input())
passclass = int(input())
gender = int(input())
age = int(input())
count_family = int(input())
count_parents_children = int(input())
price = int(input())
vector = [live, passclass, gender, age, count_family, count_parents_children, price]

tetta = np.array(tetta)
p_1 = 0
for i in range(0, 7):
    p_1 += 1 / (1 + np.exp(- tetta[i] * vector[i]))
print("Live probabiliry:", (round(p_1 / 7, 2) * 100) , '%')

tetta_star = 0
for i in range(0, len(tetta)):
    tetta_star += tetta[i]
tetta_star /= len(tetta)

tetta_2 = [0] * len(tetta)
for i in range(0, len(tetta)):
    tetta_2[i] = tetta_star

num_rows = normalized_data.shape[0]
num_cols = 7
I = np.zeros((num_rows, num_cols))

for j in range(num_rows):
    for i in range(num_cols):
        if i == 0:
            normalized_data.iloc[:, i] = 1

        result_vector = np.dot(tetta_2, normalized_data.iloc[j, :])
        I[j, :] = np.dot(
            np.dot(np.exp(-result_vector) / ((1 + np.exp(-result_vector)) * (1 + np.exp(-result_vector))),
                   normalized_data.iloc[j, :]),
            np.transpose(normalized_data.iloc[j, :])
        )

alpha = 0.05
I = np.array(I)

mean_value = np.dot(np.dot(I, vector), normalized_data)
z_score = (mean_value - 0) / (1 - alpha/2)  # z-оценка
r = 1 - np.abs(np.around(0.5 - 0.5 * np.sign(z_score) * (1 - np.exp(-2 * z_score**2)), 10))  # значение функции распределения
mean_r = np.mean(r)
print(mean_r)

w = np.dot(normalized_data, np.transpose(tetta))
mean_w = np.mean(w)
print(mean_w)

print("Доверительный Интервал:", mean_w - mean_r, mean_w + mean_r)