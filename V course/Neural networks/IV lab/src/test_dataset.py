import torch
from torch.utils.data import DataLoader
from dataset_pet import OxfordPetsDataset
from unet import UNet

device = "cuda" if torch.cuda.is_available() else "cpu"
print("Using device:", device)

# Загружаем датасет
dataset = OxfordPetsDataset(root="../dataset", split="train")
loader = DataLoader(dataset, batch_size=2, shuffle=True)

# Берем один батч
images, masks = next(iter(loader))

print("Images:", images.shape)
print("Masks:", masks.shape)

# Загружаем модель
model = UNet().to(device)
images = images.to(device)

# Прогоняем через модель
with torch.no_grad():
    outputs = model(images)

print("Outputs:", outputs.shape)
print("Min/max outputs:", outputs.min().item(), outputs.max().item())
