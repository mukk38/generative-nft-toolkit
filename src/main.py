# src/main.py
import os
from . import config
from . import image_generator
from . import metadata_generator
from . import ipfs_uploader


def main():
    print("NFT Koleksiyon Oluşturucu Başlatılıyor...")
    print("-----------------------------------------")

    print("\nADIM 1: Görseller Oluşturuluyor...")
    if not os.path.exists(config.LAYERS_DIR) or not os.listdir(config.LAYERS_DIR):
        print(f"HATA: Katman klasörü '{config.LAYERS_DIR}' bulunamadı veya boş.")
        print("Lütfen katmanlarınızı (PNG dosyaları) bu klasör altına uygun alt klasörlerle yerleştirin.")
        return

    all_nft_attributes = image_generator.generate_all_images()
    if not all_nft_attributes:
        print("HATA: Hiçbir görsel özelliği oluşturulamadı. İşlem durduruluyor.")
        return
    print("Görsel oluşturma tamamlandı.")
    print("-----------------------------------------")

    print("\nADIM 2: Görseller IPFS'e Yükleniyor...")


    uploaded_image_details = ipfs_uploader.upload_folder_to_ipfs(config.OUTPUT_IMAGES_DIR)
    if not uploaded_image_details:  # Bu, dosya_adı:cid sözlüğü
        print("HATA: Görseller IPFS'e yüklenemedi. İşlem durduruluyor.")
        return
    print("Görsel yüklemesi (denemeleri) tamamlandı.")
    print("-----------------------------------------")

    print("\nADIM 3: Metadata Dosyaları Oluşturuluyor...")


    updated_all_nft_attributes = []
    for i, attributes in enumerate(all_nft_attributes):
        image_id = i + 1
        image_filename = f"{image_id}.png"
        if image_filename in uploaded_image_details:
            image_cid = uploaded_image_details[image_filename]
            image_ipfs_uri = f"ipfs://{image_cid}"
            metadata_generator.generate_single_metadata(image_id, attributes, image_ipfs_uri)
            updated_all_nft_attributes.append(attributes)  # Başarıyla işlenenler
        else:
            print(f"Uyarı: {image_filename} için IPFS CID bulunamadı, metadata oluşturulamadı.")

    if not updated_all_nft_attributes:
        print("HATA: Hiçbir metadata dosyası oluşturulamadı. İşlem durduruluyor.")
        return
    print("Metadata dosyalarının oluşturulması tamamlandı.")
    print("-----------------------------------------")


    print("\nADIM 4: Metadata JSON Dosyaları IPFS'e Yükleniyor...")

    uploaded_json_details = ipfs_uploader.upload_json_files_to_ipfs(config.OUTPUT_JSON_DIR)
    if not uploaded_json_details:  # Bu da dosya_adı:cid sözlüğü
        print("UYARI: Metadata JSON dosyaları IPFS'e yüklenemedi veya CID alınamadı.")
    else:
        print("Metadata JSON yüklemesi (denemeleri) tamamlandı.")
        print("Yüklenen JSON detayları (dosya_adı: CID):", uploaded_json_details)

    print("-----------------------------------------")
    print("\nNFT Koleksiyon Oluşturma Süreci Tamamlandı!")
    print(f"Oluşturulan görseller: {config.OUTPUT_IMAGES_DIR}")
    print(f"Oluşturulan metadatalar: {config.OUTPUT_JSON_DIR}")
    print("Lütfen IPFS CID'lerini kontrol edin ve akıllı kontratınızda kullanın.")


if __name__ == "__main__":
    main()