import os
import torch
import numpy as np
from torch.utils.data import DataLoader
from dataset_pet import OxfordPetsDataset
from unet import UNet
from tqdm import tqdm
from PIL import Image, ImageOps, ImageFilter
import matplotlib.pyplot as plt
import csv

# Настройки
DATA_ROOT = "../dataset"        # путь к папке dataset (от src/)
MODEL_PATH = "unet_pets.pth"    # где сохранена модель после обучения
OUT_DIR = "deliverable/results"
NUM_SAVE = 20                   # сколько примеров сохранить (всего)
BATCH = 4
THRESH = 0.5

os.makedirs(OUT_DIR, exist_ok=True)
os.makedirs(os.path.join(OUT_DIR, "images"), exist_ok=True)

device = "cuda" if torch.cuda.is_available() else "cpu"
print("Device:", device)

# Dataset + loader (test split)
dataset = OxfordPetsDataset(root=DATA_ROOT, split="test", img_size=256)
loader = DataLoader(dataset, batch_size=BATCH, shuffle=False)

# Model
model = UNet().to(device)
model.load_state_dict(torch.load(MODEL_PATH, map_location=device))
model.eval()

# Utils
sigmoid = torch.nn.Sigmoid()

def to_pil(tensor):
    # tensor in [C,H,W], values 0..1
    arr = (tensor.cpu().numpy() * 255).astype(np.uint8)
    if arr.shape[0] == 1:
        arr = arr[0]
        return Image.fromarray(arr)
    else:
        arr = np.transpose(arr, (1,2,0))
        return Image.fromarray(arr)

def color_overlay(image_pil, mask_bin_pil, color=(255,0,0), alpha=0.5):
    # mask_bin_pil is single-channel 0/255
    mask = mask_bin_pil.convert("L").point(lambda p: 255 if p>128 else 0)
    color_layer = Image.new("RGBA", image_pil.size, color + (0,))
    mask_rgba = Image.new("RGBA", image_pil.size, color + (int(255*alpha),))
    # where mask==255, paste colored semi-transparent
    base = image_pil.convert("RGBA")
    result = Image.composite(mask_rgba, base, mask)
    # blend original and result to keep edges softer
    blended = Image.alpha_composite(base, result)
    return blended.convert("RGB")

# Iterate and save
saved = 0
metrics = []
with torch.no_grad():
    for images, masks in tqdm(loader, desc="Inference"):
        images = images.to(device)
        masks = masks.to(device)  # shape [B,1,H,W]
        outputs = model(images)   # logits
        probs = sigmoid(outputs)  # [B,1,H,W]

        for i in range(images.size(0)):
            if saved >= NUM_SAVE:
                break

            img_t = images[i]              # [3,H,W]
            true_mask_t = masks[i]         # [1,H,W] float 0/1
            prob_t = probs[i]              # [1,H,W]

            # to PIL
            orig = to_pil(img_t)  # RGB
            true_mask = to_pil(true_mask_t)  # grayscale 0/1 -> 0..255
            prob = to_pil(prob_t)             # grayscale probability
            # binary
            prob_arr = np.array(prob).astype(np.float32)/255.0
            bin_mask_arr = (prob_arr > THRESH).astype(np.uint8) * 255
            bin_mask = Image.fromarray(bin_mask_arr)

            idx = f"{saved:03d}"
            orig.save(os.path.join(OUT_DIR, "images", f"{idx}_orig.png"))
            true_mask.save(os.path.join(OUT_DIR, "images", f"{idx}_true_mask.png"))
            prob.save(os.path.join(OUT_DIR, "images", f"{idx}_pred_prob.png"))
            bin_mask.save(os.path.join(OUT_DIR, "images", f"{idx}_pred_bin.png"))

            # overlay (red)
            overlay = color_overlay(orig, bin_mask, color=(255,0,0), alpha=0.5)
            overlay.save(os.path.join(OUT_DIR, "images", f"{idx}_overlay.png"))

            # compute IoU and Dice on this image
            gt = (np.array(true_mask).astype(np.uint8) > 128).astype(np.uint8)
            pred = (bin_mask_arr > 0).astype(np.uint8)
            intersection = (gt & pred).sum()
            union = (gt | pred).sum()
            iou = float(intersection) / (union + 1e-8)
            dice = 2.0 * float(intersection) / (gt.sum() + pred.sum() + 1e-8)

            metrics.append({
                "idx": idx,
                "iou": iou,
                "dice": dice,
                "gt_sum": int(gt.sum()),
                "pred_sum": int(pred.sum())
            })

            saved += 1

        if saved >= NUM_SAVE:
            break

# save metrics csv
csv_path = os.path.join(OUT_DIR, "metrics.csv")
with open(csv_path, "w", newline="") as csvfile:
    fieldnames = ["idx", "iou", "dice", "gt_sum", "pred_sum"]
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()
    for r in metrics:
        writer.writerow(r)

# Save aggregated numbers
ious = [r["iou"] for r in metrics]
dices = [r["dice"] for r in metrics]
with open(os.path.join(OUT_DIR, "summary.txt"), "w") as f:
    f.write(f"num_examples: {len(metrics)}\n")
    f.write(f"mean_iou: {float(np.mean(ious)):.4f}\n")
    f.write(f"mean_dice: {float(np.mean(dices)):.4f}\n")

print("Saved images to", os.path.join(OUT_DIR, "images"))
print("Saved metrics to", csv_path)
