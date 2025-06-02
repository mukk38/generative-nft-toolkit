# src/config.py
import os
from dotenv import load_dotenv

load_dotenv()


COLLECTION_NAME = "Benim Harika NFT Koleksiyonum"
COLLECTION_DESCRIPTION = "Bu eşsiz koleksiyon, çeşitli özelliklerin birleşimiyle oluşturulmuştur."
TOTAL_NFTS = 10
IMAGE_WIDTH = 500
IMAGE_HEIGHT = 500


LAYER_ORDER = [
    "background",
    "body",
    "eyes",
    "mouth",
     "accessories"
]

# --- IPFS AYARLARI ---
PINATA_API_KEY = os.getenv("PINATA_API_KEY")
PINATA_API_SECRET = os.getenv("PINATA_API_SECRET")
PINATA_BASE_URL = "https://api.pinata.cloud"
PINATA_PIN_FILE_URL = f"{PINATA_BASE_URL}/pinning/pinFileToIPFS"
PINATA_PIN_JSON_URL = f"{PINATA_BASE_URL}/pinning/pinJSONToIPFS" # Sadece JSON için


WEB3_STORAGE_API_TOKEN = os.getenv("WEB3_STORAGE_API_TOKEN")
WEB3_STORAGE_UPLOAD_URL = "https://api.web3.storage/upload"


IPFS_SERVICE = "pinata" # veya "web3_storage"

# --- DOSYA YOLLARI ---
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) # nft_collection_generator/
LAYERS_DIR = os.path.join(BASE_DIR, "layers")
OUTPUT_DIR = os.path.join(BASE_DIR, "output")
OUTPUT_IMAGES_DIR = os.path.join(OUTPUT_DIR, "images")
OUTPUT_JSON_DIR = os.path.join(OUTPUT_DIR, "json")

# Klasörlerin var olduğundan emin ol
os.makedirs(OUTPUT_IMAGES_DIR, exist_ok=True)
os.makedirs(OUTPUT_JSON_DIR, exist_ok=True)