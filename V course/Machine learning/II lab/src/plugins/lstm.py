import torch.nn as nn
import torch


class LSTMCell(nn.Module):
    def __init__(self, input_dim, hidden_dim):
        super().__init__()

        self.input_dim = input_dim
        self.hidden_dim = hidden_dim

        # объединяем x_t и h_{t-1}
        self.W_f = nn.Linear(input_dim + hidden_dim, hidden_dim)
        self.W_i = nn.Linear(input_dim + hidden_dim, hidden_dim)
        self.W_g = nn.Linear(input_dim + hidden_dim, hidden_dim)
        self.W_o = nn.Linear(input_dim + hidden_dim, hidden_dim)

    def forward(self, x_t, h_prev, c_prev):
        """
        x_t:     [batch, input_dim]
        h_prev:  [batch, hidden_dim]
        c_prev:  [batch, hidden_dim]
        """

        # 1. склеиваем вход и hidden
        combined = torch.cat([x_t, h_prev], dim=1)

        # 2. гейты
        f_t = torch.sigmoid(self.W_f(combined))   # forget
        i_t = torch.sigmoid(self.W_i(combined))   # input
        g_t = torch.tanh(self.W_g(combined))      # candidate
        o_t = torch.sigmoid(self.W_o(combined))   # output

        # 3. обновление памяти
        c_t = f_t * c_prev + i_t * g_t

        # 4. скрытое состояние
        h_t = o_t * torch.tanh(c_t)

        return h_t, c_t


class LSTM(nn.Module):
    def __init__(self, input_dim, hidden_dim: int):
        super().__init__()

        self.hidden_dim = hidden_dim
        self.cell = LSTMCell(input_dim, hidden_dim)

    def forward(self, x):
        """
        x: [batch, seq_len, input_dim]
        """

        batch_size, seq_len, _ = x.size()

        # начальные состояния
        h = torch.zeros(batch_size, self.hidden_dim)
        c = torch.zeros(batch_size, self.hidden_dim)

        outputs = []

        # проход по времени
        for t in range(seq_len):
            x_t = x[:, t, :]          # [batch, input_dim]
            h, c = self.cell(x_t, h, c)

            outputs.append(h.unsqueeze(1))

        # склеиваем по времени
        outputs = torch.cat(outputs, dim=1)

        return outputs, (h, c)