from src.plugins.lstm import LSTM
import torch.nn as nn


class Encoder(nn.Module):
    def __init__(self, vocab_size, emb_dim, hidden_dim):
        super().__init__()

        # 1. Embedding (готовый слой)
        self.embedding = nn.Embedding(vocab_size, emb_dim)

        # 2. Custom LSTM (твой ручной)
        self.lstm = LSTM(emb_dim, hidden_dim)

    def forward(self, src):
        """
        src: [batch, seq_len]
        """

        # 1. переводим слова → векторы
        embedded = self.embedding(src)
        # [batch, seq_len, emb_dim]

        # 2. прогоняем через LSTM
        outputs, (h, c) = self.lstm(embedded)

        """
        outputs → hidden states всех шагов (ВАЖНО для attention)
        h → последний hidden state
        c → memory state
        """

        return outputs, (h, c)