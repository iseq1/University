from abc import ABC, abstractmethod

class BaseClassifier(ABC):
    @abstractmethod
    def classify(self, text):
        pass