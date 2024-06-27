import numpy as np
import matplotlib.pyplot as plt


def metrics(sample1, sample2, threshhold):
    '''Вычисляет метрики для двух выборок с указанным порогом'''
    N = len(sample1)

    TP = len([height for height in sample2 if height >= threshhold])
    TN = len([height for height in sample1 if height < threshhold])
    FP = len([height for height in sample1 if height >= threshhold])
    FN = len([height for height in sample2 if height < threshhold])

    alpha = FP / (TN + FP)
    beta = FN / (TP + FN)
    accuracy = (TP + TN) / N
    precision = TP / (TP + FP)
    recall = TP / (TP + FN)

    if precision + recall != 0:
        F1 = 2 * (precision * recall) / (precision + recall)
    else:
        F1 = None  # Неопределено, если precision + recall равны 0

    if (FP + TN) != 0:
        # Если знаменатель равен нулю, FPR устанавливается в 0
        FPR = FP / (FP + TN)
    else:
        FPR = 0

    if (TP + FN) != 0:
        # Если знаменатель равен нулю, TPR устанавливается в 1
        TPR = TP / (TP + FN)
    else:
        TPR = 1

    return {
        'threshhold': threshhold,
        'TP': TP,
        'TN': TN,
        'FP': FP,
        'FN': FN,
        'alpha': alpha,
        'beta': beta,
        'accuracy': accuracy,
        'precision': precision,
        'recall': recall,
        'F1': F1,
        'FPR': FPR,
        'TPR': TPR
    }


def plot_roc_curve(sample1, sample2):
    '''Строит ROC-кривую на основе двух выборок и вычисляет AUC'''

    all_scores = np.concatenate([sample1, sample2])
    all_labels = np.concatenate([np.zeros(len(sample1)), np.ones(len(sample2))])

    # Сортируем все значения по убыванию и соответствующие метки
    sorted_indices = np.argsort(-all_scores)
    sorted_scores = all_scores[sorted_indices]
    sorted_labels = all_labels[sorted_indices]

    # Инициализируем переменные
    tp = 0
    fp = 0
    tn = len(sample1)
    fn = len(sample2)
    tpr_values = [0]
    fpr_values = [0]
    auc = 0

    # Перебираем значения и считаем метрики
    for i in range(len(sorted_scores)):
        # для каждого следующего значения
        # считаем, что он предсказан как класс 1, смотрим «желаемый класс» и если он
        # 0, то увеличиваем FPR на 1/(FP + TN), а если он 1, то TPR на 1/(TP + FN)
        if sorted_labels[i] == 1:
            tp += 1
            fn -= 1
        else:
            fp += 1
            tn -= 1

        # Вычисляем TPR и FPR
        tpr = tp / (tp + fn) if (tp + fn) > 0 else 0
        fpr = fp / (fp + tn) if (fp + tn) > 0 else 0
        tpr_values.append(tpr)
        fpr_values.append(fpr)

        # Увеличение AUC на основе площади прямоугольника
        if i > 0:
            # площадь текущего прямоугольника
            auc += (fpr_values[-1] - fpr_values[-2]) * tpr_values[-1]

    print(f'\nAUC = {auc}')

    # Построение ROC-кривой
    plt.plot(fpr_values, tpr_values, color='red')
    plt.plot([0, 1], [0, 1], color='pink', linestyle=':')
    plt.xlabel('FP Rate')
    plt.ylabel('TP Rate')
    plt.title('ROC Curve')
    plt.show()


def find_optimal_threshold(sample1, sample2):
    '''Находит оптимальный порог для двух выборок'''
    # массив из 100 пороговых значений, равномерно распределенных между минимальным значением среди обеих выборок и максимальным значением среди обеих выборок.
    thresholds = np.linspace(min(min(sample1), min(sample2)), max(max(sample1), max(sample2)), num=100)

    # макс точность и оптимальный порог
    max_accuracy = 0
    optimal_threshold = None


    for threshold in thresholds:
        # Вычисляем метрики для текущего порога
        metrics_result = metrics(sample1, sample2, threshold)
        accuracy = metrics_result['accuracy']
        if accuracy > max_accuracy:
            max_accuracy = accuracy
            optimal_threshold = threshold
    return optimal_threshold


if __name__ == '__main__':
    # Устанавливаем количество элементов в каждой выборке
    N = 1000
    # Задаем среднее значение и стандартное отклонение для выборки футболистов
    football_mean, football_std = (190, 10)
    # Задаем среднее значение и стандартное отклонение для выборки баскетболистов
    basketball_mean, basketball_std = (150, 10)

    # Создаем выборки ростов ф-в и б-в, используя нормальное распределение с заданными средним и стандартным отклонением
    football_sample = np.random.normal(football_mean, football_std, size=N)
    basketball_sample = np.random.normal(basketball_mean, basketball_std, size=N)

    # Находим оптимальный порог, который максимизирует точность классификации
    optimal_threshold = find_optimal_threshold(football_sample, basketball_sample)

    # Вычисляем метрики для найденного оптимального порога
    optimal_metrics = metrics(football_sample, basketball_sample, optimal_threshold)

    # Вывод метрики для оптимального порога
    print("\nМетрики для оптимального порога:")
    for key, value in optimal_metrics.items():
        print(f"{key}: {value}")

    # ROC-кривая
    plot_roc_curve(football_sample, basketball_sample)