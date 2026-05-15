from torch import optim, nn
import torch


def train(model, dataloader, epochs, lr, pad_idx):

    optimizer = optim.Adam(model.parameters(), lr=lr)
    criterion = nn.CrossEntropyLoss(ignore_index=pad_idx)

    for epoch in range(epochs):

        model.train()
        total_loss = 0

        for src, trg in dataloader:

            optimizer.zero_grad()

            output = model(src, trg)

            output = output[:, 1:].reshape(-1, output.shape[-1])
            trg = trg[:, 1:].reshape(-1)

            loss = criterion(output, trg)

            loss.backward()
            optimizer.step()

            total_loss += loss.item()

        print(f"Epoch {epoch}: {total_loss:.4f}")

def infer(model, src, sos_idx, eos_idx, max_len=10):

    model.eval()

    enc_out, (hidden, cell) = model.encoder(src)

    input_token = torch.tensor([sos_idx])

    result = []

    for _ in range(max_len):

        out, hidden, cell, _ = model.decoder(
            input_token,
            hidden,
            cell,
            enc_out
        )

        pred = out.argmax(1).item()

        if pred == eos_idx:
            break

        result.append(pred)
        input_token = torch.tensor([pred])

    return result

def decode(indices, idx2word):
    return [idx2word[i] for i in indices]

def decode_input(x, idx2word):
    return [idx2word[i.item()] if isinstance(i, torch.Tensor) else idx2word[i] for i in x if i != 0]

def accuracy(model, dataloader, pad_idx):
    model.eval()

    correct = 0
    total = 0

    with torch.no_grad():
        for src, trg in dataloader:
            output = model(src, trg, teacher_forcing_ratio=0.0)

            pred = output.argmax(dim=-1)

            for i in range(trg.shape[0]):
                for t in range(trg.shape[1]):
                    if trg[i, t] != pad_idx:
                        total += 1
                        if pred[i, t] == trg[i, t]:
                            correct += 1

    return correct / total