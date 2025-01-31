import numpy as np
import matplotlib.pyplot as plt
from sklearn.datasets import load_digits
from sklearn.cluster import KMeans
from sklearn.metrics import confusion_matrix

class ImageClustering():
    def __init__(self):
        self.digits = self.load_digits()
        if self.digits is not None:
            self.X = self.digits.data
            self.Y = self.digits.target
            self.images = self.digits.images

        self.datasets = None
        self.clustering_results = None
        self.evaluation_results = None

    def load_digits(self):
        return load_digits()

    def get_histogram(self, image, bins=16):
        # Диапазон яркости - от 0 до 16
        return np.histogram(image, bins=bins, range=(0, 16))[0]

    def get_magnitude(self, image):
        dx = np.gradient(image, axis=0)
        dy = np.gradient(image, axis=1)
        return np.sqrt(dx ** 2 + dy ** 2)

    def set_feature_vectors(self):
        return {
            # Векторы характеристик
            'x_vector': self.X,  # Вектор характеристик - сами изображение
            'hist_vector': np.array([self.get_histogram(img) for img in self.images]),  # гистограммы интенсивности
            'magnitude_vector': np.array([self.get_magnitude(img).flatten() for img in self.images]),  # магнитуды градиента
        }

    def apply_kmeans_method(self, data, n_clusters=10, random_state=42):
        data_normalized = (data - data.mean(axis=0)) / (data.std(axis=0) + 1e-8)

        kmeans = KMeans(n_clusters=n_clusters, random_state=random_state)
        labels = kmeans.fit_predict(data_normalized)

        return kmeans, labels

    def set_clasterization(self, datasets):

        clustering_results = {}

        for key, value in datasets.items():
            if not np.isnan(value).any():
                kmeans, labels = self.apply_kmeans_method(value)
                clustering_results[key] = (kmeans, labels)
            else:
                print(f"{key} is None!\n")

        return clustering_results

    def get_clasterization(self):
        self.datasets = self.set_feature_vectors()
        self.clustering_results = self.set_clasterization(self.datasets)

    def map_clusters_to_labels(self, cluster_labels, true_labels):
        """
        Каждому кластеру присваивается тот класс (цифра), которая встречается в нем чаще всего
        """
        # Уникальные метки кластеров
        n_clusters = len(np.unique(cluster_labels))
        # Уникальные метки классов (10)
        n_classes = len(np.unique(true_labels))
        mapping_matrix = np.zeros((n_clusters, n_classes))

        # Матрица частот встречаемости классов в кластерах
        for i in range(len(true_labels)):
            mapping_matrix[cluster_labels[i], true_labels[i]] += 1

        # Определение наилучшего соответствия кластер->класс
        cluster_to_class = {}
        for cluster in range(n_clusters):
            # Класс с максимальным количеством точек в кластере
            true_class = np.argmax(mapping_matrix[cluster])
            cluster_to_class[cluster] = true_class
        return np.array([cluster_to_class[label] for label in cluster_labels])

    def calculate_cluster_metrics(self, data, labels):
        n = len(data)
        F0_numerator = 0
        F0_denominator = 0
        F1_numerator = 0
        F1_denominator = 0

        for i in range(n):
            for j in range(n):
                # евклидово расстояние
                distance = np.linalg.norm(data[i] - data[j])

                # если объекты из одного кластера
                if labels[i] == labels[j]:
                    F0_numerator += distance
                    F0_denominator += 1
                else:
                    F1_numerator += distance
                    F1_denominator += 1

        # Среднеее внутрикластерное расстояние
        F0 = F0_numerator / F0_denominator if F0_denominator > 0 else 0
        # Среднее межкластерное расстояние
        F1 = F1_numerator / F1_denominator if F1_denominator > 0 else 0

        return F0, F1

    def get_evaluation_results(self):
        evaluation_results = {}

        for name, (kmeans, labels) in self.clustering_results.items():
            predicted_labels = self.map_clusters_to_labels(labels, self.Y)
            intra_cluster, inter_cluster = self.calculate_cluster_metrics(self.datasets[name], labels)
            conf_matrix = confusion_matrix(self.Y, predicted_labels)

            evaluation_results[name] = {
                'intra_cluster': intra_cluster,
                'inter_cluster': inter_cluster,
                'confusion_matrix': conf_matrix,
                'predicted_labels': predicted_labels
            }

        self.evaluation_results = evaluation_results

        # Вывод результатов
        for name, metrics in evaluation_results.items():
            print(f"\nРезультаты для {name}:")
            print(f"Среднее внутрикластерное расстояние (F0): {metrics['intra_cluster']:.2f}")
            print(f"Среднее межкластерное расстояние (F1): {metrics['inter_cluster']:.2f}")
            print(f"Отношение F1/F0: {metrics['inter_cluster'] / metrics['intra_cluster']:.2f}")
            print("\nМатрица ошибок:")
            print(metrics['confusion_matrix'])

    def calculate_metrics(self, y_true, y_pred):
        classes = np.unique(y_true)
        n_classes = len(classes)

        accuracy = np.zeros(n_classes)
        precision = np.zeros(n_classes)
        recall = np.zeros(n_classes)
        f1 = np.zeros(n_classes)
        alpha = np.zeros(n_classes)
        beta = np.zeros(n_classes)

        # Расчет метрик для каждого класса
        for i, class_label in enumerate(classes):
            # Бинаризация меток
            true_bin = (y_true == class_label)
            pred_bin = (y_pred == class_label)

            TP = np.sum((true_bin) & (pred_bin))
            FP = np.sum((y_true != class_label) & (pred_bin))
            TN = np.sum((y_true != class_label) & (y_pred != class_label))
            FN = np.sum((true_bin) & (y_pred != class_label))

            accuracy[i] = (TP + TN) / (TP + TN + FP + FN)
            precision[i] = TP / (TP + FP) if (TP + FP) > 0 else 0
            recall[i] = TP / (TP + FN) if (TP + FN) > 0 else 0
            f1[i] = 2 * (precision[i] * recall[i]) / (precision[i] + recall[i]) if (precision[i] + recall[i]) > 0 else 0
            alpha[i] = FP / (FP + TN) if (FP + TN) > 0 else 0
            beta[i] = FN / (TP + FN) if (TP + FN) > 0 else 0

        return {
            'accuracy': np.mean(accuracy),
            'precision': np.mean(precision),
            'recall': np.mean(recall),
            'f1': np.mean(f1),
            'alpha': np.mean(alpha),
            'beta': np.mean(beta)
        }

    def set_metrics(self):
        for name, metrics in self.evaluation_results.items():
            predicted_labels = metrics['predicted_labels']
            classification_metrics = self.calculate_metrics(self.Y, predicted_labels)

            yield {
                'name': name,
                'Accuracy': classification_metrics['accuracy'],
                'Precision': classification_metrics['precision'],
                'Recall': classification_metrics['recall'],
                'F1 Score': classification_metrics['f1'],
                'alpha': classification_metrics['alpha'],
                'beta': classification_metrics['beta'],
            }

    def get_metrics(self):
        for statistic in self.set_metrics():
            print(f"\nМетрики для {statistic['name']}:")
            print(f"Accuracy: {statistic['Accuracy']:.3f}")
            print(f"Precision: {statistic['Precision']:.3f}")
            print(f"Recall: {statistic['Recall']:.3f}")
            print(f"F1 Score: {statistic['F1 Score']:.3f}")
            print(f"Ошибка I рода (alpha): {statistic['alpha']:.3f}")
            print(f"Ошибка II рода (beta): {statistic['beta']:.3f}")



    def set_best_metrics(self):
        best_metrics = {
            'accuracy': {'value': 0, 'method': ''},
            'precision': {'value': 0, 'method': ''},
            'recall': {'value': 0, 'method': ''},
            'f1': {'value': 0, 'method': ''},
            'alpha': {'value': float('inf'), 'method': ''},
            'beta': {'value': float('inf'), 'method': ''}
        }

        for name, metrics in self.evaluation_results.items():
            predicted_labels = metrics['predicted_labels']
            current_metrics = self.calculate_metrics(self.Y, predicted_labels)

            for metric_name in best_metrics.keys():
                current_value = current_metrics[metric_name]

                if metric_name in ['alpha', 'beta']:
                    if current_value < best_metrics[metric_name]['value']:
                        best_metrics[metric_name]['value'] = current_value
                        best_metrics[metric_name]['method'] = name
                else:
                    if current_value > best_metrics[metric_name]['value']:
                        best_metrics[metric_name]['value'] = current_value
                        best_metrics[metric_name]['method'] = name

        return best_metrics

    def get_best_metrics(self):
        best_metrics = self.set_best_metrics()
        print("\nЛучшие метрики для каждого метода:")
        print("-" * 50)
        for metric_name, data in best_metrics.items():
            print(f"{metric_name.capitalize()}:")
            print(f"Значение: {data['value']:.3f}")
            print(f"Метод: {data['method']}")
            print("-" * 50)

    def plot_roc_curves(self, y_true, y_pred_scores, method_name):
        from sklearn.preprocessing import label_binarize
        from sklearn.metrics import roc_curve, auc
        # Бинаризация меток
        n_classes = 10
        y_test_bin = label_binarize(y_true, classes=range(n_classes))
        y_pred_bin = label_binarize(y_pred_scores, classes=range(n_classes))

        plt.figure(figsize=(10, 8))

        for i in range(n_classes):
            fpr, tpr, _ = roc_curve(y_test_bin[:, i], y_pred_bin[:, i])
            roc_auc = auc(fpr, tpr)

            plt.plot(fpr, tpr, label=f'ROC класс {i} (AUC = {roc_auc:.2f})')

        plt.plot([0, 1], [0, 1], 'k--')
        plt.xlim([0.0, 1.0])
        plt.ylim([0.0, 1.05])
        plt.xlabel('False Positive Rate')
        plt.ylabel('True Positive Rate')
        plt.title(f'ROC-кривые для набора данных {method_name}')
        plt.legend(loc="lower right", fontsize='small')
        plt.grid(True)
        plt.show()

    def get_roc_curves(self):
        for name, metrics in self.evaluation_results.items():
            predicted_labels = metrics['predicted_labels']
            self.plot_roc_curves(self.Y, predicted_labels, name)