import pandas as pd
import json
import re

class TextPreprocessor:

    DS_PATH = '../dataset/dataset.csv'

    def __init__(self, stopwords=None):

        if stopwords is None:
            self.stopwords = {"the", "is", "a", "an", "and", "to", "of", "in", "it", "this", "that"}
        else:
            self.stopwords = stopwords

    @staticmethod
    def clean_text(text: str) -> str:
        """
        Приводит текст к нижнему регистру, убирает знаки кроме букв и пробелов
        :param text:
        :return:
        """
        text = str(text).lower()
        text = re.sub(r"[^a-z\s]", "", text)
        text = re.sub(r"\s+", " ", text).strip()
        return text

    @staticmethod
    def tokenize(text: str) -> list:
        """
        Разбивает текст на токены
        :param text:
        :return:
        """
        return text.split()

    @staticmethod
    def remove_stopwords(tokens, stopwords):
        """
        Убирает стоп-слова
        :param tokens:
        :param stopwords:
        :return:
        """
        return [token for token in tokens if token not in stopwords]

    def preprocess_text(self, text):
        """
        Полная обработка одного текста
        :param text:
        :return:
        """
        cleaned = self.clean_text(text)
        tokens = self.tokenize(cleaned)
        tokens = self.remove_stopwords(tokens, self.stopwords)
        return tokens

    def preprocess_corpus(self, texts):
        """
        Обрабатывает список текстов
        :param texts:
        :return:
        """
        return [self.preprocess_text(t) for t in texts]

    @staticmethod
    def save_tokenized(tokenized_texts, filename="tokenized_texts.json"):
        """
        Сохраняет токенизированный корпус в JSON
        """
        with open(filename, "w", encoding="utf-8") as f:
            json.dump(tokenized_texts, f, ensure_ascii=False)
        print(f"Saved tokenized texts to {filename}")

    @staticmethod
    def load_tokenized(filename="tokenized_texts.json"):
        """
        Загружает токенизированный корпус из JSON
        """
        with open(filename, "r", encoding="utf-8") as f:
            tokenized_texts = json.load(f)
        print(f"Loaded tokenized texts from {filename}")
        return tokenized_texts

    @staticmethod
    def get_dataset(dataset_path=None):
        ds_path = dataset_path if dataset_path else TextPreprocessor.DS_PATH
        df = pd.read_csv(ds_path)
        return df