import os
from PIL import Image
from torch.utils.data import Dataset
import numpy as np
import torchvision.transforms as T


class OxfordPetsDataset(Dataset):
    def __init__(self, root, split="train", img_size=256):
        self.root = root
        self.img_size = img_size

        # Пути
        self.images_dir = os.path.join(root, "images")
        self.masks_dir = os.path.join(root, "annotations", "trimaps")

        # Списки файлов
        if split == "train":
            list_file = os.path.join(root, "annotations", "trainval.txt")
        else:
            list_file = os.path.join(root, "annotations", "test.txt")

        with open(list_file, "r") as f:
            self.files = [line.strip().split(" ")[0] for line in f]

        # Трансформации
        self.img_transform = T.Compose([
            T.Resize((img_size, img_size)),
            T.ToTensor(),
        ])

        self.mask_transform = T.Compose([
            T.Resize((img_size, img_size), interpolation=Image.NEAREST),
        ])

    def __len__(self):
        return len(self.files)

    def __getitem__(self, idx):
        img_name = self.files[idx]

        # Пути к файлам
        img_path = os.path.join(self.images_dir, img_name + ".jpg")
        mask_path = os.path.join(self.masks_dir, img_name + ".png")

        # Загрузка изображения
        image = Image.open(img_path).convert("RGB")

        # Загрузка маски
        mask = Image.open(mask_path)

        # Преобразование маски: trimaps {1,2,3}
        mask = np.array(self.mask_transform(mask))
        mask = (mask == 3).astype(np.float32)  # 1 — объект, 0 — фон

        image = self.img_transform(image)

        # Превращаем маску в тензор 1×H×W
        mask = np.expand_dims(mask, axis=0)

        return image, mask
