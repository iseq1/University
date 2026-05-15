from src.plugins.attantion import Attention
from src.plugins.lstm import LSTM
import torch.nn as nn
import torch


class Decoder(nn.Module):
    def __init__(self, vocab_size, emb_dim, hidden_dim):
        super().__init__()

        self.embedding = nn.Embedding(vocab_size, emb_dim)

        # вход: [embedding + context]
        self.lstm = LSTM(emb_dim + hidden_dim, hidden_dim)

        self.attention = Attention(hidden_dim)

        self.fc = nn.Linear(hidden_dim * 2, vocab_size)

        self.hidden_dim = hidden_dim

    def forward(self, input_token, hidden, cell, encoder_outputs):
        """
        input_token: [batch]
        hidden: [batch, hidden_dim]
        cell: [batch, hidden_dim]
        encoder_outputs: [batch, seq_len, hidden_dim]
        """

        # 1. embedding
        input_token = input_token.unsqueeze(1)  # [batch, 1]
        embedded = self.embedding(input_token)
        embedded = embedded.squeeze(1)  # [batch, emb_dim]

        # 2. attention context
        context, attn_weights = self.attention(hidden, encoder_outputs)
        # context: [batch, hidden_dim]

        # 3. объединяем embedding + context
        lstm_input = torch.cat([embedded, context], dim=1)
        # [batch, emb_dim + hidden_dim]

        lstm_input = lstm_input.unsqueeze(1)  # [batch, 1, emb_dim+hidden]

        # 4. LSTM step
        output, (hidden, cell) = self.lstm(lstm_input)

        # output: [batch, 1, hidden_dim]
        output = output.squeeze(1)

        # 5. concat output + context
        combined = torch.cat([output, context], dim=1)

        # 6. prediction
        prediction = self.fc(combined)
        # [batch, vocab_size]

        return prediction, hidden, cell, attn_weights


