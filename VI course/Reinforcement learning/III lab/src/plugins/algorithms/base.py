from abc import ABC, abstractmethod


class Base(ABC):
    """Базовый класс реализуемых алгоритмов"""


    @abstractmethod
    def action(self, *args, **kwargs): pass


    @abstractmethod
    def generate_episode(self, *args, **kwargs): pass


    @abstractmethod
    def train(self, *args, **kwargs): pass


    @abstractmethod
    def evaluate(self, *args, **kwargs): pass