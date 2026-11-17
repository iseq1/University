"""Описание базового класса для скриптов"""
import sys

from argparse import ArgumentParser
from abc import ABC, abstractmethod
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

OUTPUT_DIR = ROOT / "backend" /"data" / "generated"


class BaseScript(ABC):
    """Базовый класс, описывающий скрипты"""

    def __init__(self):
        self.parser = ArgumentParser(description=__doc__)


    @abstractmethod
    def main(self) -> None:
        """Основной метод класса"""
        pass


    @staticmethod
    def _get_output_dir() -> Path:
        """Получение рабочей директории"""
        return OUTPUT_DIR