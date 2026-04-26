import pandas as pd

def load_dataset(path):
    df = pd.read_csv(path)
    texts = df["text"].tolist()
    labels = df["label"].tolist()
    return texts, labels