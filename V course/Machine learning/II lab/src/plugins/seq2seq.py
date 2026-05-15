import torch.nn as nn
import torch


class Seq2Seq(nn.Module):
    def __init__(self, encoder, decoder):
        super().__init__()

        self.encoder = encoder
        self.decoder = decoder

    def forward(self, src, trg, teacher_forcing_ratio=0.5):
        """
        src: [batch, src_len]
        trg: [batch, trg_len]
        """

        batch_size = src.shape[0]
        trg_len = trg.shape[1]
        vocab_size = self.decoder.fc.out_features

        outputs = torch.zeros(batch_size, trg_len, vocab_size)

        # 1. encoder
        encoder_outputs, (hidden, cell) = self.encoder(src)

        # 2. первый вход decoder = <SOS>
        input_token = trg[:, 0]

        for t in range(1, trg_len):

            output, hidden, cell, _ = self.decoder(
                input_token,
                hidden,
                cell,
                encoder_outputs
            )

            outputs[:, t] = output

            # teacher forcing
            use_teacher = torch.rand(1).item() < teacher_forcing_ratio

            top1 = output.argmax(1)

            input_token = trg[:, t] if use_teacher else top1

        return outputs
