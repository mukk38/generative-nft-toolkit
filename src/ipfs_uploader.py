# src/ipfs_uploader.py
import os
import requests
import json
from . import config


def _pinata_pin_file_to_ipfs(file_path):
    if not config.PINATA_API_KEY or not config.PINATA_API_SECRET:
        print("Hata: Pinata API anahtarları config dosyasında ayarlanmamış.")
        return None

    headers = {
        "pinata_api_key": config.PINATA_API_KEY,
        "pinata_secret_api_key": config.PINATA_API_SECRET
    }

    with open(file_path, 'rb') as fp:
        image_binary = fp.read()
        response = requests.post(
            config.PINATA_PIN_FILE_URL,
            files={"file": (os.path.basename(file_path), image_binary)},
            headers=headers
        )

    if response.status_code == 200:
        print(f"Dosya {os.path.basename(file_path)} Pinata'ya başarıyla yüklendi. CID: {response.json()['IpfsHash']}")
        return response.json()['IpfsHash']
    else:
        print(
            f"Hata: Pinata'ya dosya yüklenirken sorun oluştu. Status: {response.status_code}, Response: {response.text}")
        return None


def _pinata_pin_json_to_ipfs(json_data, filename="metadata.json"):
    if not config.PINATA_API_KEY or not config.PINATA_API_SECRET:
        print("Hata: Pinata API anahtarları config dosyasında ayarlanmamış.")
        return None

    headers = {
        "Content-Type": "application/json",
        "pinata_api_key": config.PINATA_API_KEY,
        "pinata_secret_api_key": config.PINATA_API_SECRET
    }

    payload = {
        "pinataOptions": {"cidVersion": 1},  # CIDv1 kullanmak genellikle daha iyidir
        "pinataMetadata": {"name": filename},
        "pinataContent": json_data
    }

    response = requests.post(config.PINATA_PIN_JSON_URL, json=payload, headers=headers)

    if response.status_code == 200:
        cid = response.json()['IpfsHash']
        print(f"JSON {filename} Pinata'ya başarıyla yüklendi. CID: {cid}")
        return cid
    else:
        print(
            f"Hata: Pinata'ya JSON yüklenirken sorun oluştu. Status: {response.status_code}, Response: {response.text}")
        return None


def _web3_storage_upload_file(file_path):
    if not config.WEB3_STORAGE_API_TOKEN:
        print("Hata: Web3.storage API token'ı config dosyasında ayarlanmamış.")
        return None

    headers = {
        "Authorization": f"Bearer {config.WEB3_STORAGE_API_TOKEN}",
        "Content-Type": "application/car"
    }
    with open(file_path, 'rb') as fp:
        response = requests.post(config.WEB3_STORAGE_UPLOAD_URL, data=fp, headers=headers)

    if response.status_code == 200:
        cid = response.json().get('cid')
        if cid:
            print(f"Dosya {os.path.basename(file_path)} Web3.storage'a başarıyla yüklendi. CID: {cid}")
            return cid
        else:
            print(f"Hata: Web3.storage'dan CID alınamadı. Response: {response.json()}")
            return None
    else:
        print(
            f"Hata: Web3.storage'a dosya yüklenirken sorun oluştu. Status: {response.status_code}, Response: {response.text}")
        return None


def upload_folder_to_ipfs(folder_path, service=config.IPFS_SERVICE):

    if not os.path.isdir(folder_path):
        print(f"Hata: {folder_path} bir klasör değil.")
        return None

    files_to_upload = [f for f in os.listdir(folder_path) if os.path.isfile(os.path.join(folder_path, f))]
    if not files_to_upload:
        print(f"Uyarı: {folder_path} içinde yüklenecek dosya bulunamadı.")
        return None

    print(f"\n'{folder_path}' klasöründeki dosyalar {service} kullanılarak IPFS'e yükleniyor...")

    first_successful_cid = None
    uploaded_file_cids = {}

    for filename in sorted(files_to_upload):
        file_path = os.path.join(folder_path, filename)
        cid = None
        if service == "pinata":
            cid = _pinata_pin_file_to_ipfs(file_path)
        elif service == "web3_storage":
            cid = _web3_storage_upload_file(file_path)
        else:
            print(f"Hata: Geçersiz IPFS servisi: {service}")
            return None  # veya {}

        if cid:
            uploaded_file_cids[filename] = cid
            if not first_successful_cid:
                first_successful_cid = cid

    if uploaded_file_cids:
        print(f"\n'{os.path.basename(folder_path)}' içindeki dosyalar için yükleme denemeleri tamamlandı.")
        return uploaded_file_cids
    else:
        print(f"'{os.path.basename(folder_path)}' klasöründen hiç dosya yüklenemedi.")
        return {}


def upload_json_files_to_ipfs(json_folder_path, service=config.IPFS_SERVICE):

    print(f"\n'{json_folder_path}' klasöründeki JSON dosyaları {service} kullanılarak IPFS'e yükleniyor...")
    if not os.path.isdir(json_folder_path):
        print(f"Hata: {json_folder_path} bir klasör değil.")
        return None

    files_to_upload = [f for f in os.listdir(json_folder_path) if f.endswith('.json')]
    if not files_to_upload:
        print(f"Uyarı: {json_folder_path} içinde yüklenecek JSON dosyası bulunamadı.")
        return None

    uploaded_json_cids = {}
    first_successful_cid = None  # Temsili "klasör" CID'i

    for filename in sorted(files_to_upload):
        file_path = os.path.join(json_folder_path, filename)
        cid = None
        with open(file_path, 'r') as f:
            json_data = json.load(f)

        if service == "pinata":
            cid = _pinata_pin_json_to_ipfs(json_data, filename=filename)
        elif service == "web3_storage":
            temp_json_path = os.path.join(config.OUTPUT_JSON_DIR, f"temp_{filename}")
            with open(temp_json_path, 'w') as tmp_f:
                json.dump(json_data, tmp_f)
            cid = _web3_storage_upload_file(temp_json_path)
            os.remove(temp_json_path)
        else:
            print(f"Hata: Geçersiz IPFS servisi: {service}")
            return None

        if cid:
            uploaded_json_cids[filename] = cid
            if not first_successful_cid:
                first_successful_cid = cid

    if uploaded_json_cids:
        print(f"\n'{os.path.basename(json_folder_path)}' içindeki JSON dosyaları için yükleme denemeleri tamamlandı.")
        return uploaded_json_cids
    else:
        print(f"'{os.path.basename(json_folder_path)}' klasöründen hiç JSON dosyası yüklenemedi.")
        return {}


if __name__ == "__main__":
    print("IPFS yükleyici başlatılıyor...")

    if not os.listdir(config.OUTPUT_IMAGES_DIR):
        print(f"'{config.OUTPUT_IMAGES_DIR}' klasörü boş. Lütfen önce görselleri oluşturun.")
    else:
        print("\n--- Görseller Yükleniyor ---")
        image_cids = upload_folder_to_ipfs(config.OUTPUT_IMAGES_DIR)
        if image_cids:
            print("Yüklenen görsel CID'leri:", image_cids)

    if not os.listdir(config.OUTPUT_JSON_DIR):
        print(f"'{config.OUTPUT_JSON_DIR}' klasörü boş. Lütfen önce metadata dosyalarını oluşturun.")
    else:
        print("\n--- JSON Metadatalar Yükleniyor ---")
        json_cids = upload_json_files_to_ipfs(config.OUTPUT_JSON_DIR)
        if json_cids:
            print("Yüklenen JSON CID'leri:", json_cids)
