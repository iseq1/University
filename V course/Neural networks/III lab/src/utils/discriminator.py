# -----------------------------
# DISCRIMINATOR
# -----------------------------
import torch.nn as nn


class Discriminator(nn.Module):
    def __init__(self, image_channels=3, features_d=64):
        super().__init__()
        self.disc = nn.Sequential(
            nn.Conv2d(image_channels, features_d, 4, 2, 1),
            nn.LeakyReLU(0.2, inplace=True),

            nn.Conv2d(features_d, features_d * 2, 4, 2, 1),
            nn.BatchNorm2d(features_d * 2),
            nn.LeakyReLU(0.2, inplace=True),

            nn.Conv2d(features_d * 2, features_d * 4, 4, 2, 1),
            nn.BatchNorm2d(features_d * 4),
            nn.LeakyReLU(0.2, inplace=True),

            nn.Conv2d(features_d * 4, features_d * 8, 4, 2, 1),
            nn.BatchNorm2d(features_d * 8),
            nn.LeakyReLU(0.2, inplace=True),

            nn.Conv2d(features_d * 8, 1, 4, 1, 0),
        )

    def forward(self, x):
        return self.disc(x)
