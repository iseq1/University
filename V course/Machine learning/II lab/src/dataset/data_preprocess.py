from collections import Counter
import pandas as pd
import torch


class DataPreprocess:

    SPECIAL_TOKENS = ["<PAD>", "<SOS>", "<EOS>", "<UNK>"]

    def __init__(self):
        self.input_i2w = None
        self.input_w2i = None
        self.target_i2w = None
        self.target_w2i = None
        self.Y = None
        self.X = None

    @staticmethod
    def get_data(path: str = "dataset/steam_dataset_clean.csv"):
        df = pd.read_csv(path)
        inputs = df["description"].tolist()
        targets = df["genre"].tolist()
        return inputs, targets

    @staticmethod
    def tokenize(text: str) -> list:
        return text.lower().split()

    def build_vocab(self, texts, min_freq=1):
        counter = Counter()

        for text in texts:
            tokens = self.tokenize(text)
            counter.update(tokens)

        vocab = self.SPECIAL_TOKENS.copy()

        for word, freq in counter.items():
            if freq >= min_freq:
                vocab.append(word)

        word2idx = {word: i for i, word in enumerate(vocab)}
        idx2word = {i: word for word, i in word2idx.items()}

        return word2idx, idx2word

    def encode(self, text, word2idx, add_sos=False, add_eos=False):
        tokens = self.tokenize(text)

        ids = []

        if add_sos:
            ids.append(word2idx["<SOS>"])

        for token in tokens:
            ids.append(word2idx.get(token, word2idx["<UNK>"]))

        if add_eos:
            ids.append(word2idx["<EOS>"])

        return ids

    @staticmethod
    def pad_sequences(sequences, pad_idx):
        max_len = max(len(seq) for seq in sequences)

        padded = []
        for seq in sequences:
            seq = seq + [pad_idx] * (max_len - len(seq))
            padded.append(seq)

        return padded

    def handle(self):

        inputs, targets = self.get_data()

        print(f'Input example: {inputs[:3]}')
        print(f'Target example: {targets[:3]}')

        self.input_w2i, self.input_i2w = self.build_vocab(inputs)
        self.target_w2i, self.target_i2w = self.build_vocab(targets)

        print("Input vocab size:", len(self.input_w2i))
        print("Target vocab size:", len(self.target_w2i))

        encoded_inputs = [
            self.encode(text, self.input_w2i)
            for text in inputs
        ]
        print(f'Input encoded: {encoded_inputs[:3]}')

        encoded_targets = [
            self.encode(text, self.target_w2i, add_sos=True, add_eos=True)
            for text in targets
        ]
        print(f'Target encoded: {encoded_targets[:3]}')

        input_pad_idx = self.input_w2i["<PAD>"]
        target_pad_idx = self.target_w2i["<PAD>"]

        padded_inputs = self.pad_sequences(encoded_inputs, input_pad_idx)
        print(f'Inputs encoded with <PAD>: {padded_inputs[:3]}')
        padded_targets = self.pad_sequences(encoded_targets, target_pad_idx)
        print(f'Target encoded with <PAD>: {padded_targets[:3]}')

        self.X = torch.tensor(padded_inputs)
        self.Y = torch.tensor(padded_targets)

        print(self.X.shape)
        print(self.Y.shape)

    def get_preprocessed_data(self):
        return [self.X, self.Y]

    def get_input_vocab(self):
        return [self.input_w2i, self.input_i2w]

    def get_target_vocab(self):
        return [self.target_w2i, self.target_i2w]