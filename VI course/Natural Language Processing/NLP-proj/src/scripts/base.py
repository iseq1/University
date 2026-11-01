"""Описание базового класса для скриптов"""
from argparse import ArgumentParser
from abc import ABC, abstractmethod


class BaseScript(ABC):
    """Базовый класс, описывающий скрипты"""

    def __init__(self):
        self.parser = ArgumentParser(description=__doc__)


    @abstractmethod
    def main(self) -> None:
        """Основной метод класса"""
        pass
