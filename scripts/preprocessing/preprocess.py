from rembg import remove, new_session
from PIL import Image
import numpy as np
import cv2
import os
from concurrent.futures import ThreadPoolExecutor, as_completed
from tqdm import tqdm
import warnings
import tarfile
import h5py
from sklearn.preprocessing import OneHotEncoder
from sklearn.model_selection import train_test_split
import pandas as pd
import json

warnings.filterwarnings("ignore", category=UserWarning, message="Specified provider 'CUDAExecutionProvider' is not in available provider names")

GLOBAL_SESSION = None

def compress_data(raw_path, compressed_dir, tar_name):
    os.makedirs(compressed_dir, exist_ok=True)
    tar_path = os.path.join(compressed_dir, tar_name)
    if os.path.exists(tar_path):
        os.remove(tar_path)
    print(f"Creando archivo comprimido: {tar_path}")
    with tarfile.open(tar_path, "w") as tar:
        tar.add(raw_path, arcname=os.path.basename(raw_path))
    print(f"TAR creado correctamente en: {tar_path}")

def init_gpu_session():
    return new_session("u2net", providers=["CUDAExecutionProvider", "CPUExecutionProvider"])

def process_img(img, size=200, padding=20):
    global GLOBAL_SESSION
    if GLOBAL_SESSION is None:
        raise RuntimeError("El modelo GLOBAL_SESSION debe inicializarse antes de ThreadPoolExecutor.")

    rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    pil_img = Image.fromarray(rgb)
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
    try:
        img = cv2.imread(in_path)
        if img is None:
            return False
        result = process_img(img)
        if result is None:
            return False
        os.makedirs(os.path.dirname(out_path), exist_ok=True)
        cv2.imwrite(out_path, result)
        return True
    except Exception as e:
        print(f"Error procesando {in_path}: {e}")
        return False

def preprocess_all(raw, output, workers=8):
    global GLOBAL_SESSION
    print("Cargando modelo de remoción de fondo")
    GLOBAL_SESSION = init_gpu_session()
    print("Modelo cargado correctamente.")

    tasks = []
    print("Listando archivos...")
    for root, dirs, files in os.walk(raw):
        for fname in files:
            if fname.lower().endswith((".jpg", ".jpeg", ".png")):
                in_path = os.path.join(root, fname)
                rel_path = os.path.relpath(in_path, raw)
                out_path = os.path.join(output, rel_path)
                tasks.append((in_path, out_path))

    print(f"\nTotal imágenes encontradas: {len(tasks)}\n")
    print(f"Iniciando procesamiento con {workers} hilos (GPU/CUDA)...")

    with ThreadPoolExecutor(max_workers=workers) as executor:
        futures = [executor.submit(process_single_file, t) for t in tasks]
        for _ in tqdm(as_completed(futures), total=len(futures), desc="Procesando"):
            pass

    print("\nPreprocesamiento completado con GPU.")

def create_h5_file(df, h5_file_path, image_size, one_hot_encoder):
    n_images = df.shape[0]
    categories = [str(x) for x in one_hot_encoder.categories_[0]]
    one_hot_vector_index = range(len(categories))

    with h5py.File(h5_file_path, "w") as f:
        dset_img = f.create_dataset("images", shape=(n_images, ) + image_size, dtype=np.uint8)
        dset_class = f.create_dataset("classes", shape=(n_images, len(categories)) , dtype=np.uint8)
        
        class_map_dict = dict(zip(one_hot_vector_index, categories))
        class_map_json = json.dumps(class_map_dict)
        dset_class.attrs['index_to_class'] = class_map_json

        for index, row in tqdm(df.iterrows(), total=df.shape[0]):
            image = Image.open(row["file_path"])
            np_image = np.array(image)
            dset_img[index] = np_image
            dset_class[index] = one_hot_encoder.transform([[row["class"]]])

def h5_files_train_val_test(origin_path, destination_path):
    categories = []
    for folder in os.listdir(origin_path):
        categories.append(folder)
    categories.sort()
    ohe = OneHotEncoder(handle_unknown='ignore', sparse_output=False)
    ohe.fit(np.array(categories).reshape(-1, 1))

    file_paths = []
    classes = []
    for root, dirs, files in os.walk(origin_path):
        for fname in files: 
            file_paths.append(root+"/"+fname)
            classes.append(root.split("/")[-1])
    
    df = pd.DataFrame(list(zip(file_paths, classes)), columns =["file_path", "class"])

    X = df[["file_path"]]
    y = df[["class"]]

    X_train, X_aux, y_train, y_aux = train_test_split(X, y, test_size=0.3, random_state=42, stratify=y)
    X_val, X_test, y_val, y_test = train_test_split(X_aux, y_aux, test_size=0.5, random_state=42, stratify=y_aux)
    
    train_df = pd.concat([X_train, y_train], axis=1).reset_index(drop=True)
    val_df = pd.concat([X_val, y_val], axis=1).reset_index(drop=True)
    test_df = pd.concat([X_test, y_test], axis=1).reset_index(drop=True)

    print("\nCreating training data .hdf5 files")
    create_h5_file(
        train_df, 
        h5_file_path=destination_path+"train.hdf5", 
        image_size=(200,200,3), 
        one_hot_encoder = ohe
    )
    print("Train data saved in ", destination_path+"train.hdf5")

    print("\nCreating validation data .hdf5 files")
    create_h5_file(
        val_df, 
        h5_file_path=destination_path+"/val.hdf5", 
        image_size=(200,200,3), 
        one_hot_encoder = ohe
    )
    print("Validation data saved in ", destination_path+"val.hdf5")

    print("\nCreating test data .hdf5 files")
    create_h5_file(
        test_df, 
        h5_file_path=destination_path+"test.hdf5", 
        image_size=(200,200,3), 
        one_hot_encoder = ohe
    )
    print("Test data saved in ", destination_path+"test.hdf5")

if __name__ == "__main__":
    print("Starting Preprocessing with GPU")
    preprocess_all("/content/mlds6/data/raw", "/content/mlds6/data/preprocessed", workers=8)

    print("Compressing output into .tar files")

    images_path = "/content/mlds6/data/preprocessed/asl-alphabet/asl_alphabet_train/asl_alphabet_train/"
    destination_path = "/content/mlds6/data/hdf5/"
    os.makedirs(destination_path, exist_ok=True)
    h5_files_train_val_test(images_path, destination_path)

    compress_data(
        raw_path='/content/mlds6/data/preprocessed',
        compressed_dir='/content/mlds6/data_compressed',
        tar_name='data_compressed.tar'
    )

    compress_data(
        raw_path='/content/mlds6/data/hdf5',
        compressed_dir='/content/mlds6/data_compressed',
        tar_name='hdf5.tar'
    )