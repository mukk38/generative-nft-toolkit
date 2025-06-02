import json
import os
import time
from . import config


def generate_single_metadata(image_id, attributes, image_ipfs_uri):
    metadata = {
        "name": f"{config.COLLECTION_NAME} #{image_id}",
        "description": config.COLLECTION_DESCRIPTION,
        "image": image_ipfs_uri,
        "dna": "-".join(sorted([attr['value'].lower().replace(" ", "") for attr in attributes])),
        "edition": image_id,
        "date": int(time.time() * 1000),
        "attributes": attributes
    }

    output_path = os.path.join(config.OUTPUT_JSON_DIR, f"{image_id}.json")
    with open(output_path, 'w') as f:
        json.dump(metadata, f, indent=2)
    print(f"Metadata kaydedildi: {output_path}")
    return output_path


def generate_all_metadata(all_nft_attributes, images_folder_cid=None):

    if not all_nft_attributes:
        print("Hata: Özellik listesi boş, metadata oluşturulamıyor.")
        return

    if images_folder_cid:
        base_image_uri = f"ipfs://{images_folder_cid}"
        print(f"Görseller için temel IPFS URI'si: {base_image_uri}")
    else:
        base_image_uri = "ipfs://YOUR_IMAGES_FOLDER_CID_HERE"
        print("Uyarı: Görsel klasör CID'i sağlanmadı. Metadata'daki 'image' alanları yer tutucu içerecek.")

    for i, attributes in enumerate(all_nft_attributes):
        image_id = i + 1
        image_file_name = f"{image_id}.png"  # Görsel dosyasıyla eşleşmeli
        image_ipfs_uri = f"{base_image_uri}/{image_file_name}"

        generate_single_metadata(image_id, attributes, image_ipfs_uri)

    print(f"\nToplam {len(all_nft_attributes)} adet metadata dosyası oluşturuldu.")


if __name__ == "__main__":
    print("Metadata oluşturucu başlatılıyor...")


    sample_attributes_for_testing = [
        [{"trait_type": "Background", "value": "Blue"}, {"trait_type": "Body", "value": "Regular"}],
        [{"trait_type": "Background", "value": "Red"}, {"trait_type": "Body", "value": "Zombie"}]
    ]
    sample_images_cid = "QmXoypizjW3WknFiJnKLwHCnL72vedxjQkDDP1mXWo6uco"

    if not os.path.exists(config.OUTPUT_IMAGES_DIR) or not os.listdir(config.OUTPUT_IMAGES_DIR):
        print(f"Uyarı: '{config.OUTPUT_IMAGES_DIR}' klasöründe hiç görsel bulunamadı.")
        print("Lütfen önce görselleri oluşturun veya test için örnek özellikler kullanın.")
    else:

        num_generated_images = len(os.listdir(config.OUTPUT_IMAGES_DIR))
        if len(sample_attributes_for_testing) != num_generated_images and num_generated_images > 0:
            print("Gerçek özellikler bulunamadı, test için varsayılan özellikler kullanılıyor.")
            temp_attributes_for_testing = []
            for i in range(num_generated_images):
                temp_attributes_for_testing.append([{"trait_type": "Test", "value": f"Value {i + 1}"}])
            generate_all_metadata(temp_attributes_for_testing, sample_images_cid)
        elif num_generated_images > 0:
            generate_all_metadata(sample_attributes_for_testing, sample_images_cid)
        else:
            print("Test için hiç görsel üretilmemiş.")