from kaggle.api.kaggle_api_extended import KaggleApi


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
