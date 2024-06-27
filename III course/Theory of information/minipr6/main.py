import pandas as pd
import numpy as np
import math
import seaborn as sns
import matplotlib.pyplot as plt
import time
from sklearn.preprocessing import StandardScaler
from scipy.stats import norm

start_time = time.time()

file_path = 'Bd_Titanik.xlsx'

data = pd.read_excel(file_path, skiprows=3)
data = data.iloc[3:, :]
# data['Survived_Feature'] = np.where(data.iloc[0, 0] == 1, 1, 0)
# data.columns = data.columns.astype(str)
# scaler = StandardScaler()
# df_normalized = pd.DataFrame(scaler.fit_transform(data), columns=data.columns)

normalized_data = (data - data.mean()) / data.std()
print(normalized_data)

# print(data.head())
tetta = [0, 0, 0, 0, 0, 0, 0]
l = [0, 0, 0, 0, 0, 0, 0]
n = 0.0001
y = [0] * data.shape[0]
for i in range(0, data.shape[0]):
    y[i] = data.iloc[i, 0]

for i in range(0, data.shape[0]):
    data.iloc[i, 0] = 1


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

print(l)
print(tetta)
sum_result = 0

for i in range(0, 7):
    if i == 0:
        normalized_data.iloc[:, i] = 1

    for j in range(0, normalized_data.shape[0] - 1):
        result_vector = np.dot(tetta, normalized_data.iloc[j,])
        sum_result += np.log(
            ((1 / (1 + np.exp(-result_vector))) ** y[j]) * ((1 / (1 + np.exp(result_vector))) ** (1 - y[j])))
    # print(np.log(((1 / (1 + np.exp(-tetta[i] * data.iloc[j, i]))) ** data.iloc[j, 0]) * ((1 / (1 + np.exp(tetta[i] * data.iloc[j, i]))) ** (1 - data.iloc[j, 0]))))

print(sum_result)
print(tetta)

end_time = time.time()
duration = end_time - start_time
print("Duration: ", duration)

theta_hat = np.array(tetta)

mu_approx = np.mean(theta_hat)
sigma_approx = np.std(theta_hat, ddof=1)

normal_distribution = np.random.normal(loc=mu_approx, scale=sigma_approx, size=10000)

plt.figure(figsize=(10, 6))
sns.histplot(theta_hat, bins=20, kde=True, color='blue')
sns.histplot(normal_distribution, bins=20, kde=True, color='red')

plt.legend()
plt.show()

end_time = time.time()
duration = end_time - start_time
print("Duration: ", duration)

vector = [1, 1, 20, 1, 2, 0, 50]

tetta = np.array(tetta)
p_1 = 0
for i in range(0, 7):
    p_1 += 1 / (1 + np.exp(- tetta[i] * vector[i]))
print(p_1 / 7)

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

r = norm.sf(np.dot(np.dot(I, vector), normalized_data), 0, 1 - alpha / 2)
mean_r = np.mean(r)
print(mean_r)

w = np.dot(normalized_data, np.transpose(tetta))
mean_w = np.mean(w)
print(mean_w)

print(mean_w - mean_r, mean_w + mean_r)