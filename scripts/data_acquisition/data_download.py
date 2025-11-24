import os
import tarfile
from kaggle.api.kaggle_api_extended import KaggleApi


def compress_raw_data(raw_path="../../data/raw", compressed_dir="../../data_compressed", tar_name="data_raw.tar"):
    """
    Comprime la carpeta 'data/raw/' en un archivo .tar dentro de 'data_compressed/'.
    """
    os.makedirs(compressed_dir, exist_ok=True)

    tar_path = os.path.join(compressed_dir, tar_name)

    if os.path.exists(tar_path):
        os.remove(tar_path)

    print(f"Creando archivo comprimido: {tar_path}")

    with tarfile.open(tar_path, "w") as tar:
        tar.add(raw_path, arcname=os.path.basename(raw_path))

    print(f"TAR creado correctamente en: {tar_path}")


if __name__ == "__main__":
    try:
        api = KaggleApi()
        api.authenticate()
        print("Kaggle authenticated")

    except Exception as e:
        print("Kaggle authentication failed")
        print("\nError:", e)
        print("\nMake sure your kaggle.json file is in the correct location.\n")

        print("On Windows:")
        print(r"    C:\Users\<YOUR_USERNAME>\.kaggle\kaggle.json")

        print("\nOn Linux / macOS:")
        print("    ~/.kaggle/kaggle.json")

        print("\nIf the folder '.kaggle' does not exist, create it manually and place kaggle.json inside.")
        print("Also ensure that the file is named exactly 'kaggle.json'.")


    api.dataset_download_files(
        'grassknoted/asl-alphabet',
        path='../../data/raw/asl-alphabet',
        unzip=True
    )

    compress_raw_data(
        raw_path='../../data/raw',
        compressed_dir='../../data_compressed',
        tar_name='data_raw.tar'
    )