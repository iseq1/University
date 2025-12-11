from src.utils.discriminator import Discriminator
from src.utils.generator import Generator

from torchvision import datasets, transforms
from torchvision.utils import save_image
from torch.utils.data import DataLoader
from tqdm import tqdm
import torch.optim as optim
import torch.nn as nn

import numpy as np
import torch
import csv
import os
import time

# --- CUDA ускорение ---
torch.backends.cudnn.benchmark = True
torch.backends.cudnn.enabled = True

print(torch.__version__)
print(torch.version.cuda)
print("CUDA available:", torch.cuda.is_available())
print("GPU name:", torch.cuda.get_device_name(0) if torch.cuda.is_available() else "—")


def save_checkpoint(gen, disc, opt_gen, opt_disc, epoch, path="checkpoint.pt"):
    torch.save({
        "epoch": epoch,
        "gen_state": gen.state_dict(),
        "disc_state": disc.state_dict(),
        "opt_gen_state": opt_gen.state_dict(),
        "opt_disc_state": opt_disc.state_dict(),
    }, path)
    print(f"✔ Checkpoint saved: {path}")


def load_checkpoint(path, gen, disc, opt_gen=None, opt_disc=None, device="cpu"):
    checkpoint = torch.load(path, map_location=device)

    gen.load_state_dict(checkpoint["gen_state"])
    disc.load_state_dict(checkpoint["disc_state"])

    if opt_gen and opt_disc:
        opt_gen.load_state_dict(checkpoint["opt_gen_state"])
        opt_disc.load_state_dict(checkpoint["opt_disc_state"])

    print(f"✔ Checkpoint loaded, epoch = {checkpoint['epoch']}")
    return checkpoint["epoch"]


# -----------------------------
# ДАТАЛОАДЕР
# -----------------------------
def get_fruits360_dataloader(path, image_size=64, batch_size=64):
    transform = transforms.Compose([
        transforms.Resize(image_size),
        transforms.CenterCrop(image_size),
        transforms.ToTensor(),
        transforms.Normalize([0.5]*3, [0.5]*3)
    ])

    dataset = datasets.ImageFolder(root=path, transform=transform)

    dataloader = DataLoader(
        dataset,
        batch_size=batch_size,
        shuffle=True,
        num_workers=0,       # главный источник ускорения
        pin_memory=True,
        # persistent_workers=True
    )

    return dataloader

# -----------------------------
# ТРЕНИРОВКА
# -----------------------------
def train_gan(
        gen,
        disc,
        dataloader,
        z_dim=100,
        lr=2e-4,
        epochs=10,
        device="cpu",
        save_dir="generated",
        resume=False,
        checkpoint_path="checkpoint.pt"
):

    os.makedirs(save_dir, exist_ok=True)

    # CSV лог
    csv_path = os.path.join(save_dir, "loss_log.csv")
    new_log = not os.path.exists(csv_path)

    # Loss function
    criterion = nn.BCEWithLogitsLoss()

    # Optimizers
    opt_gen = optim.Adam(gen.parameters(), lr=lr, betas=(0.5, 0.999))
    opt_disc = optim.Adam(disc.parameters(), lr=lr, betas=(0.5, 0.999))

    start_epoch = 0

    # ---- RESUME TRAINING ----
    if resume and os.path.exists(checkpoint_path):
        start_epoch = load_checkpoint(checkpoint_path, gen, disc, opt_gen, opt_disc, device)
        print(f"▶ Resuming from epoch {start_epoch+1}")

    # Fixed noise for samples
    fixed_noise = torch.randn(64, z_dim, 1, 1).to(device)

    gen.train()
    disc.train()

    # Open CSV
    with open(csv_path, "a", newline="") as f:
        writer = csv.writer(f)
        if new_log:
            writer.writerow(["epoch", "D_loss", "G_loss"])

        # ----------- EPOCH LOOP -----------
        for epoch in range(start_epoch, epochs):

            progress = tqdm(dataloader, desc=f"Epoch {epoch+1}/{epochs}", leave=True)
            batch_times = []

            losses_D = []
            losses_G = []

            for batch_idx, (real, _) in enumerate(progress):

                start_time = time.time()

                real = real.to(device)
                batch_size = real.size(0)

                # ----- TRAIN DISC -----
                noise = torch.randn(batch_size, z_dim, 1, 1, device=device)
                fake = gen(noise)

                disc_real = disc(real).reshape(-1)
                disc_fake = disc(fake.detach()).reshape(-1)

                loss_real = criterion(disc_real, torch.full_like(disc_real, 0.9))
                loss_fake = criterion(disc_fake, torch.zeros_like(disc_fake))
                loss_disc = (loss_real + loss_fake) / 2

                opt_disc.zero_grad()
                loss_disc.backward()
                opt_disc.step()

                # ----- TRAIN GEN -----
                output = disc(fake).reshape(-1)
                loss_gen = criterion(output, torch.ones_like(output))

                opt_gen.zero_grad()
                loss_gen.backward()
                opt_gen.step()

                batch_times.append(time.time() - start_time)

                losses_D.append(loss_disc.item())
                losses_G.append(loss_gen.item())

                if batch_idx % 50 == 0:
                    progress.set_postfix({
                        "D_loss": f"{loss_disc.item():.4f}",
                        "G_loss": f"{loss_gen.item():.4f}",
                        "batch_time": f"{batch_times[-1]:.3f}s"
                    })

            print(f"Среднее время батча: {np.mean(batch_times):.4f} сек")

            # Save CSV epoch avg losses
            writer.writerow([epoch+1, np.mean(losses_D), np.mean(losses_G)])

            # save samples
            with torch.no_grad():
                samples = gen(fixed_noise)
                samples = samples * 0.5 + 0.5
                save_image(samples, f"{save_dir}/epoch_{epoch+1}.png", nrow=8)

            # Save checkpoint each epoch
            save_checkpoint(gen, disc, opt_gen, opt_disc, epoch, checkpoint_path)

    print("Обучение завершено!")




if __name__ == '__main__':
    device = "cuda" if torch.cuda.is_available() else "cpu"

    batch_size = 64

    dataloader = get_fruits360_dataloader("D:\\projects\\University\\V course\\Neural networks\\III lab\\dataset\\Training", image_size=64, batch_size=batch_size)

    z_dim = 128
    gen = Generator(z_dim=z_dim).to(device)
    disc = Discriminator().to(device)

    train_gan(
        gen,
        disc,
        dataloader,
        z_dim=z_dim,
        lr=2e-4,
        epochs=25,
        device=device,
        save_dir="generated"
    )


