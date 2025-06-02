# Python NFT Generator & IPFS Uploader

##  Description

A Python-based tool to programmatically generate unique NFT image collections by combining image layers. It also creates OpenSea-compatible JSON metadata and uploads both images and metadata to IPFS using Pinata or Web3.storage. Ideal for developers and artists looking to automate NFT collection creation.

This project uses the configuration provided in `src/config.py` and manages sensitive API keys via a `.env` file.

##  Features

* **Generative Art:** Creates unique images by layering PNG assets from organized folders.
* **Metadata Generation:** Automatically produces JSON metadata files compatible with OpenSea and other marketplaces.
* **IPFS Integration:** Uploads images and JSON metadata to IPFS via Pinata or Web3.storage.
* **Configurable:** Easily customize collection size, image dimensions, layer order, descriptions, and more through `src/config.py`.
* **Secure:** Keeps your API keys safe using a `.env` file.

##  Prerequisites

* Python (3.8+ recommended)
* Pip (Python package installer)
* Git (for cloning the repository)
* An active account with [Pinata](https://www.pinata.cloud/) and/or [Web3.storage](https://web3.storage/) if you plan to use IPFS upload features.

##  Setup & Installation

### 1. Clone the Repository
```bash
git clone <your-repository-url>
cd <your-repository-name>
```
### 2. Create Virtual Environment & Install Dependencies
It's recommended to use a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows use `venv\Scripts\activate`
```
Create a requirements.txt file in the root of your project with the following content
```bash
Pillow
python-dotenv
requests
```
Then, install the dependencies:
```bash
pip install -r requirements.txt
```

### 3. Set Up Environment Variables (.env file)

Create a .env file in the root directory of your project. This file will store your API keys. Do not commit this file to Git.

Copy the following structure into your .env file and replace the placeholder values with your actual keys:

```bash
# .env

# Pinata API Keys
PINATA_API_KEY="YOUR_PINATA_API_KEY"
PINATA_API_SECRET="YOUR_PINATA_API_SECRET_KEY"

# Web3.storage API Token
WEB3_STORAGE_API_TOKEN="YOUR_WEB3_STORAGE_API_TOKEN"
```

#### Getting Pinata API Keys:
1.  Go to [Pinata.cloud](https://www.pinata.cloud/) and sign up or log in.
2.  Navigate to the **API Keys** section (usually found by clicking your profile icon or in the developer section).
3.  Click on **"New Key"**.
4.  Enable **Admin** permissions (or ensure at least `Pinning` permissions: `pinFileToIPFS` and `pinJSONToIPFS`).
5.  Give your key a name and complete the key creation.
6.  You will be shown an `API Key`, a `Secret API Key`, and possibly a `JWT`.
7.  Copy the **`API Key`** and paste it as `PINATA_API_KEY` in your `.env` file.
8.  Copy the **`Secret API Key`** (this is distinct from the JWT and is shown only once) and paste it as `PINATA_API_SECRET` in your `.env` file.

#### Getting Web3.storage API Token:
1.  Go to [Web3.storage](https://web3.storage/) and sign up or log in.
2.  Navigate to your account page and find the **API Tokens** section.
3.  Click on **"Create a new API token"** (or similar).
4.  Give your token a name.
5.  Copy the generated **API Token**. This token is shown only once.
6.  Paste it as `WEB3_STORAGE_API_TOKEN` in your `.env` file.


##  Configuration (`src/config.py`)

The main behavior of the NFT generator is controlled by the `src/config.py` file. Below is an explanation of its variables:

##### Key Configuration Points:

- COLLECTION_NAME, COLLECTION_DESCRIPTION: Define the branding for your NFT series.
- TOTAL_NFTS: Specifies how many unique NFTs will be generated.
- IMAGE_WIDTH, IMAGE_HEIGHT: Set the dimensions for your output images. Ensure your layer assets are designed to fit these dimensions.
- LAYER_ORDER: Crucial for correct image composition. The order in this list determines the stacking order of image layers. Each name must correspond to a sub-folder in your LAYERS_DIR.
- IPFS_SERVICE: Toggles between Pinata and Web3.storage for uploading your assets. Make sure the corresponding API keys are set in .env.
- Paths (LAYERS_DIR, OUTPUT_IMAGES_DIR, etc.): These are usually fine as is, but good to know where your input layers should go and where output will be stored.

##  Usage

### 1. Prepare Your Layers
* Create your image layers as PNG files with transparent backgrounds (except for the background layer itself, usually).
* Organize these layers into sub-folders within the `layers` directory. Each sub-folder name must exactly match an entry in the `LAYER_ORDER` list in `src/config.py`.
* For example, if `LAYER_ORDER = ["background", "body"]`, you need `layers/background/` and `layers/body/` directories.

### 2. Configure the Project
* Set up your `.env` file with API keys as described in the sections above (Getting Pinata API Keys, Getting Web3.storage API Token).
* Modify `src/config.py` to define your collection's name, description, total number of NFTs, image dimensions, layer order, and preferred IPFS service.

### 3. Run the Script
You will need to create a main Python script (e.g., `src/main.py`) that imports the configuration from `src/config.py` and orchestrates the following steps:
1.  Reading layer files.
2.  Generating unique image combinations based on your rarity rules and layer selections.
3.  Saving the generated images to `OUTPUT_IMAGES_DIR`.
4.  Creating JSON metadata for each image and saving it to `OUTPUT_JSON_DIR`.
5.  (Optional) Uploading the images and then the JSON files to the selected IPFS service.
6.  (Optional) Updating the JSON metadata with the final IPFS image URLs before uploading the JSON files.

Execute your main script from the root directory:
```bash
python src/main.py
```