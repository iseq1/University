import numpy as np
import matplotlib.pyplot as plt
from sklearn.datasets import load_digits
from sklearn.model_selection import train_test_split
from sklearn.metrics import confusion_matrix

class DecisionTreeNode:
    def __init__(self, feature=None, threshold=None, left=None, right=None, value=None):
        self.feature = feature  # Индекс признака для разбиения
        self.threshold = threshold  # Пороговое значение для разбиения
        self.left = left  # Левое поддерево
        self.right = right  # Правое поддерево
        self.value = value  # Класс, если узел является листом

class DecisionTree:
    def __init__(self, max_depth=8, min_samples_split=2, min_entropy=0.01):
        self.max_depth = max_depth  # Максимальная глубина дерева
        self.min_samples_split = min_samples_split  # Минимальное количество образцов для разделения узла
        self.min_entropy = min_entropy  # Минимальная энтропия для разделения узла
        self.tree = None  # Дерево решений

    def fill_tree(self, x, y):
        self.tree = self.build_tree(x, y, depth=0)

    def build_tree(self, x, y, depth):
        # Условие остановка построения дерева
        if depth == self.max_depth or len(x) < self.min_samples_split or self.calculate_entropy(y) < self.min_entropy:
            # возвращает индекс класса с наибольшим количеством вхождений в списке y
            return DecisionTreeNode(value=np.bincount(y).argmax())


        # Находим лучшее разбиение
        best_split = None
        best_gain = -1
        for feature in range(x.shape[1]):
            for threshold in np.unique(x[:, feature]):
                left_indices = x[:, feature] <= threshold
                right_indices = x[:, feature] > threshold
                gain = self.information_gain(y, y[left_indices], y[right_indices])
                if gain > best_gain:
                    best_gain = gain
                    best_split = (feature, threshold)

        # Если не удалось найти разбиение, создаем листовой узел
        if best_gain == 0:
            # возвращает индекс класса с наибольшим количеством вхождений в списке y
            return DecisionTreeNode(value=np.bincount(y).argmax())

        # Создаем узел и рекурсивно строим левое и правое поддерево
        # лучшее разделение на признак и порог
        feature, threshold = best_split
        left_indices = x[:, feature] <= threshold
        right_indices = x[:, feature] > threshold

        left_subtree = self.build_tree(x[left_indices], y[left_indices], depth + 1)
        right_subtree = self.build_tree(x[right_indices], y[right_indices], depth + 1)

        return DecisionTreeNode(feature=feature, threshold=threshold, left=left_subtree, right=right_subtree)

    def calculate_entropy(self, y):
        _, counts = np.unique(y, return_counts=True)
        probabilities = counts / len(y)
        entropy = -np.sum(probabilities * np.log2(probabilities))
        return entropy

    def information_gain(self, parent, left_child, right_child):
        parent_entropy = self.calculate_entropy(parent)
        left_weight = len(left_child) / len(parent)
        right_weight = len(right_child) / len(parent)
        # берём средневзвешенную энтропию для двух дочерних узлов, учитывая их веса
        children_entropy = (left_weight * self.calculate_entropy(left_child) +
                            right_weight * self.calculate_entropy(right_child))
        information_gain = parent_entropy - children_entropy
        return information_gain

    def predict(self, x):
        # получается массив предсказанных меток классов для каждого элемента входных данных
        return np.array([self.predict_instance(instance, self.tree) for instance in x])

    def predict_instance(self, x, node):
        # Если узел является листом, возвращаем его значение (класс)
        if node.value is not None:
            return node.value

        # Рекурсивно спускаемся по дереву до листовых узлов
        if x[node.feature] <= node.threshold:
            return self.predict_instance(x, node.left)
        else:
            return self.predict_instance(x, node.right)

def plot_error_histogram(confusion_matrix, title):
    errors = np.sum(confusion_matrix, axis=1) - np.diag(confusion_matrix)
    classes = range(len(confusion_matrix))

    plt.bar(classes, errors)
    plt.xlabel('Классы')
    plt.ylabel('Количество ошибок')
    plt.title(title)
    plt.xticks(classes)
    plt.show()

if __name__ == '__main__':
    ld = load_digits()
    x_train, x_test, y_train, y_test = train_test_split(ld.data, ld.target, test_size=0.2, random_state=50)

    classifier = DecisionTree(max_depth=10, min_samples_split=10, min_entropy=0.01)
    classifier.fill_tree(x_train, y_train)

    y_train_pred = classifier.predict(x_train)
    y_test_pred = classifier.predict(x_test)
    train_accuracy = np.mean(y_train == y_train_pred)
    print("Точность тренеровочных данных:", train_accuracy)

    test_accuracy = np.mean(y_test == y_test_pred)
    print("Точность тестовых данных:", test_accuracy, end='\n\n')

    train_confusion_matrix = confusion_matrix(y_train, y_train_pred)
    print("Тренеровочная матрица (confusion) ошибок:\n", train_confusion_matrix, end='\n\n')
    plot_error_histogram(train_confusion_matrix, title='Гистограмма уверенности тренеровочных данных по матрице ошибок (confusion)')

    test_confusion_matrix = confusion_matrix(y_test, y_test_pred)
    print("Тестовая матрица (confusion) ошибок:\n", test_confusion_matrix)
    plot_error_histogram(test_confusion_matrix, title='Гистограмма уверенности тестовых данных по матрице ошибок (confusion)')

    plt.imshow(ld.images[100])
    plt.show()

    print(classifier.predict([ld.data[100]]))
