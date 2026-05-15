from torch.utils.data import DataLoader, TensorDataset
from sklearn.model_selection import train_test_split

from src.dataset.data_preprocess import DataPreprocess
from src.plugins.encoder import Encoder
from src.plugins.decoder import Decoder
from src.plugins.seq2seq import Seq2Seq
from src.utils.utils import *

if __name__ == "__main__":
    # 1.
    dp = DataPreprocess()
    dp.handle()
    X, Y = dp.get_preprocessed_data()
    input_w2i, input_i2w = dp.get_input_vocab()
    target_w2i, target_i2w = dp.get_target_vocab()

    X_train, X_test, Y_train, Y_test = train_test_split(
        X, Y,
        test_size=0.2,
        random_state=42
    )

    train_dataset = TensorDataset(
        torch.tensor(X_train),
        torch.tensor(Y_train)
    )

    test_dataset = TensorDataset(
        torch.tensor(X_test),
        torch.tensor(Y_test)
    )

    train_loader = DataLoader(train_dataset, batch_size=32, shuffle=True)
    test_loader = DataLoader(test_dataset, batch_size=32, shuffle=False)

    input_vocab_size = len(input_w2i)
    target_vocab_size = len(target_w2i)

    emb_dim = 64
    hidden_dim = 128

    encoder = Encoder(input_vocab_size, emb_dim, hidden_dim)
    decoder = Decoder(target_vocab_size, emb_dim, hidden_dim)

    model = Seq2Seq(encoder, decoder)

    pad_idx = target_w2i["<PAD>"]

    train(
        model=model,
        dataloader=train_loader,
        epochs=10,
        lr=0.001,
        pad_idx=pad_idx
    )

    train_acc = accuracy(model, train_loader, pad_idx)
    test_acc = accuracy(model, test_loader, pad_idx)

    print("\n=== RESULTS ===")
    print("Train accuracy:", train_acc)
    print("Test accuracy:", test_acc)

    for i in range(10):
        sample = X_test[i].unsqueeze(0)
        decoded_in = decode_input(X_test[i], input_i2w)

        result = infer(
            model,
            sample,
            sos_idx=target_w2i["<SOS>"],
            eos_idx=target_w2i["<EOS>"]
        )
        decoded_res = decode(result, target_i2w)

        print(f'Input: {decoded_in}\nResult: {decoded_res}\n\n')