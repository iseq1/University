import torch.nn.functional as F
import torch.nn as nn
import torch


class Attention(nn.Module):
    def __init__(self, hidden_dim):
        super().__init__()
        self.hidden_dim = hidden_dim

    def forward(self, decoder_hidden, encoder_outputs):
        """
        decoder_hidden: [batch, hidden_dim]
        encoder_outputs: [batch, seq_len, hidden_dim]
        """

        # 1. расширяем decoder hidden
        # [batch, 1, hidden_dim]
        decoder_hidden = decoder_hidden.unsqueeze(1)

        # 2. считаем score (dot product)
        scores = torch.sum(encoder_outputs * decoder_hidden, dim=2)
        # [batch, seq_len]

        # 3. attention weights
        attn_weights = F.softmax(scores, dim=1)
        # [batch, seq_len]

        # 4. добавляем размерность
        attn_weights = attn_weights.unsqueeze(2)
        # [batch, seq_len, 1]

        # 5. context vector (взвешенная сумма)
        context = torch.sum(attn_weights * encoder_outputs, dim=1)
        # [batch, hidden_dim]

        return context, attn_weights

