from rembg import remove
from PIL import Image
import numpy as np
import cv2
import os
from tqdm import tqdm

def process_img(img, size=200, padding=20):
    """
    - Recibe imagen BGR (OpenCV)
    - Remueve fondo con rembg
    - Recorta en bounding box
    - Pone fondo negro
    - Retorna imagen RGB 200x200
    """

    # Convertir BGR → RGB
    rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    pil_img = Image.fromarray(rgb)

    # Remover fondo
    no_bg = remove(pil_img)
    no_bg_np = np.array(no_bg)  # RGBA

    # Extraer canal alfa
    alpha = no_bg_np[:, :, 3]

    coords = cv2.findNonZero(alpha)
    if coords is None:
        return None

    x, y, w, h = cv2.boundingRect(coords)

    # Agregar padding
    x1 = max(x - padding, 0)
    y1 = max(y - padding, 0)
    x2 = min(x + w + padding, no_bg_np.shape[1])
    y2 = min(y + h + padding, no_bg_np.shape[0])

    cropped_rgba = no_bg_np[y1:y2, x1:x2]

    # Convertir RGBA → RGB con fondo negro
    black_bg = np.zeros((cropped_rgba.shape[0], cropped_rgba.shape[1], 3), dtype=np.uint8)
    alpha_crop = cropped_rgba[:, :, 3] / 255.0

    # Mezclar mano + fondo negro
    for c in range(3):
        black_bg[:, :, c] = cropped_rgba[:, :, c] * alpha_crop + 0 * (1 - alpha_crop)

    # Redimensionar a 200×200
    resized = cv2.resize(black_bg, (size, size), interpolation=cv2.INTER_AREA)

    return resized

def preprocess_all(raw, output):
    raw_root = raw
    out_root = output

    for root, dirs, files in os.walk(raw_root):
        print("Processing ", dirs)
        for fname in tqdm(files):
            if not fname.lower().endswith((".jpg", ".jpeg", ".png")):
                continue

            in_path = os.path.join(root, fname)

            rel_path = os.path.relpath(in_path, raw_root)
            out_path = os.path.join(out_root, rel_path)

            os.makedirs(os.path.dirname(out_path), exist_ok=True)

            img = cv2.imread(in_path)
            processed = process_img(img)

            if processed is None:
                continue

            cv2.imwrite(out_path, processed)

print("Starting Preprocessing")
preprocess_all("data/raw", "data/preprocessed")