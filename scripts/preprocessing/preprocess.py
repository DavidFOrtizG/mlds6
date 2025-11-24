from rembg import remove, new_session
from PIL import Image
import numpy as np
import cv2
import os
from concurrent.futures import ProcessPoolExecutor, as_completed
from tqdm import tqdm
import tarfile

def compress_preprocessed(pre_path="/content/mlds6/data/preprocessed",
                          compressed_dir="/content/mlds6/data_compressed",
                          tar_name="data_preprocessed.tar"):
    """
    Comprime la carpeta 'data/preprocessed/' en un archivo .tar
    dentro de la carpeta 'data_compressed/'.
    """
    os.makedirs(compressed_dir, exist_ok=True)

    tar_path = os.path.join(compressed_dir, tar_name)

    # Si existe un tar previo, borrarlo
    if os.path.exists(tar_path):
        os.remove(tar_path)

    print(f"\nCreando archivo comprimido: {tar_path}")

    with tarfile.open(tar_path, "w") as tar:
        tar.add(pre_path, arcname=os.path.basename(pre_path))

    print(f"TAR creado correctamente en: {tar_path}\n")


def init_gpu_session():

    return new_session("u2net", providers=["CUDAExecutionProvider", "CPUExecutionProvider"])


# Cada proceso tendrá su propia sesión
GLOBAL_SESSION = None


def process_img(img, size=200, padding=20):
    global GLOBAL_SESSION
    if GLOBAL_SESSION is None:
        GLOBAL_SESSION = init_gpu_session()

    rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    pil_img = Image.fromarray(rgb)

    # Remove background using GPU session
    no_bg = remove(pil_img, session=GLOBAL_SESSION)
    no_bg_np = np.array(no_bg)

    alpha = no_bg_np[:, :, 3]
    coords = cv2.findNonZero(alpha)
    if coords is None:
        return None

    x, y, w, h = cv2.boundingRect(coords)

    x1 = max(x - padding, 0)
    y1 = max(y - padding, 0)
    x2 = min(x + w + padding, no_bg_np.shape[1])
    y2 = min(y + h + padding, no_bg_np.shape[0])

    cropped_rgba = no_bg_np[y1:y2, x1:x2]
    alpha_crop = cropped_rgba[:, :, 3] / 255.0
    black_bg = (cropped_rgba[:, :, :3] * alpha_crop[..., None]).astype(np.uint8)

    resized = cv2.resize(black_bg, (size, size), interpolation=cv2.INTER_AREA)
    return resized


def process_single_file(args):
    in_path, out_path = args

    img = cv2.imread(in_path)
    if img is None:
        return False

    result = process_img(img)
    if result is None:
        return False

    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    cv2.imwrite(out_path, result)
    return True


def preprocess_all(raw, output, workers=4):
    tasks = []

    # Listar carpetas antes del procesamiento
    for root, dirs, files in os.walk(raw):
        relative_folder = os.path.relpath(root, raw)
        print(f"📁 Preparando carpeta: {relative_folder}")

        for fname in files:
            if fname.lower().endswith((".jpg", ".jpeg", ".png")):
                in_path = os.path.join(root, fname)
                rel_path = os.path.relpath(in_path, raw)
                out_path = os.path.join(output, rel_path)
                tasks.append((in_path, out_path))

    print(f"\nTotal imágenes encontradas: {len(tasks)}\n")

    # Paralelizar
    with ProcessPoolExecutor(max_workers=workers) as executor:
        futures = [executor.submit(process_single_file, t) for t in tasks]

        for _ in tqdm(as_completed(futures), total=len(futures), desc="Procesando"):
            pass

    print("\n✔ Preprocesamiento completado con GPU.")


if __name__ == "__main__":
    print("Starting Preprocessing with GPU")
    preprocess_all("/content/mlds6/data/raw", "/content/mlds6/data/preprocessed", workers=4)

    compress_preprocessed(
        pre_path="/content/mlds6/data/preprocessed",
        compressed_dir="/content/mlds6/data_compressed",
        tar_name="data_preprocessed.tar"
    )