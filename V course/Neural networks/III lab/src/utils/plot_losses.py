import pandas as pd
import matplotlib.pyplot as plt

def plot_losses(csv_path):
    data = pd.read_csv(csv_path)

    plt.figure(figsize=(10, 5))
    plt.plot(data["epoch"], data["D_loss"], label="Discriminator Loss")
    plt.plot(data["epoch"], data["G_loss"], label="Generator Loss")
    plt.legend()
    plt.xlabel("Epoch")
    plt.ylabel("Loss")
    plt.title("GAN Loss Curves")
    plt.grid(True)
    plt.show()


plot_losses("/src/generated\\loss_log.csv")