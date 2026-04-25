from src.plugins.text_preprocessor import TextPreprocessor
import numpy as np


class DatasetPreprocessor:

    @staticmethod
    def get_labels(dataset, size):

        scores  = dataset["review_score"].tolist()
        review_votes  = dataset["review_votes"].tolist()

        labels = []

        for score, vote in zip(scores, review_votes):
            if score == 1 and vote == 1:
                labels.append("positive_useful")
            elif score == 1 and vote == 0:
                labels.append("positive_not_useful")
            elif score == -1 and vote == 1:
                labels.append("negative_useful")
            else:
                labels.append("negative_not_useful")

        label2id = {
            "negative_not_useful": 0,
            "negative_useful": 1,
            "positive_not_useful": 2,
            "positive_useful": 3
        }

        y = np.array([label2id[label] for label in labels[:size]])

        return y

    @staticmethod
    def get_tokens(dataset, corpus_len=50000):

        texts = dataset["review_text"].astype(str).tolist()
        preprocessor = TextPreprocessor()
        tokenized_texts = None

        try:
            # Загружаем заготовку
            tokenized_texts = preprocessor.load_tokenized("steam_tokenized.json")
        except Exception as e:
            print(e)
            # Если нечего загружать - создаем заготовку
            tokenized_texts = preprocessor.preprocess_corpus(texts[:corpus_len])
            preprocessor.save_tokenized(tokenized_texts, "steam_tokenized.json")
        finally:
            return tokenized_texts