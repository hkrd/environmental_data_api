import os
import gdown
import zipfile
from tqdm import tqdm

BASE_PATH = os.path.join(os.path.dirname(__file__), "..", "data")
URLS = [
    "https://drive.google.com/file/d/1W2E7nPTezw4x6vd77V1ok85kuOiCZVMB/view?usp=sharing"
]

def download_and_extract_file(url, output_path):
    # Download the file
    zip_path = os.path.join(output_path, f"temp_{url.split('/')[-2]}.zip")
    gdown.download(url, zip_path, quiet=False, fuzzy=True)

    # Extract the zip file
    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        for file in tqdm(zip_ref.namelist(), desc="Extracting files"):
            if file.endswith('.nc'):
                zip_ref.extract(file, output_path)

    # Remove the zip file
    os.remove(zip_path)

def ensure_data_files():
    if not os.path.exists(BASE_PATH):
        os.makedirs(BASE_PATH)

    existing_files = [f for f in os.listdir(BASE_PATH) if f.endswith('.nc')]

    if len(existing_files) < len(URLS):
        print("Downloading missing data files...")
        for url in URLS:
            download_and_extract_file(url, BASE_PATH)
        print("All data files downloaded and extracted successfully.")
    else:
        print("All data files are already present.")

    # Remove any non-.nc files
    for file in os.listdir(BASE_PATH):
        if not file.endswith('.nc'):
            os.remove(os.path.join(BASE_PATH, file))

    return [os.path.join(BASE_PATH, f) for f in os.listdir(BASE_PATH) if f.endswith('.nc')]

if __name__ == "__main__":
    ensure_data_files()
