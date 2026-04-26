class Evaluator:
    def accuracy(self, y_true, y_pred):
        correct = sum([1 for t, p in zip(y_true, y_pred) if t == p])
        return correct / len(y_true)