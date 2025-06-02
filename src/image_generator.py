# src/image_generator.py
import os
import random
from PIL import Image
from . import config


def get_random_trait_from_layer(layer_name):
    layer_path = os.path.join(config.LAYERS_DIR, layer_name)
    if not os.path.exists(layer_path) or not os.path.isdir(layer_path):
        print(f"Uyarı: '{layer_path}' katman klasörü bulunamadı veya bir klasör değil.")
        return None

    traits = [f for f in os.listdir(layer_path) if f.endswith('.png')]
    if not traits:
        print(f"Uyarı: '{layer_name}' katmanında hiç PNG dosyası bulunamadı.")
        return None

    chosen_trait_file = random.choice(traits)
    return os.path.join(layer_path, chosen_trait_file)


def generate_single_image(image_id, attributes_list):

    base_image = Image.new('RGBA', (config.IMAGE_WIDTH, config.IMAGE_HEIGHT), (0, 0, 0, 0))

    print(f"Görsel #{image_id} oluşturuluyor...")

    for layer_name in config.LAYER_ORDER:
        trait_path = get_random_trait_from_layer(layer_name)

        if trait_path:
            try:
                trait_image = Image.open(trait_path).convert('RGBA')

                base_image.paste(trait_image, (0, 0),
                                 trait_image)

                trait_value = os.path.splitext(os.path.basename(trait_path))[0]
                attributes_list.append(
                    {"trait_type": layer_name.capitalize(), "value": trait_value.replace("_", " ").capitalize()})
                print(f"  Katman: {layer_name}, Özellik: {trait_value}")
            except Exception as e:
                print(f"Hata: {trait_path} yüklenirken veya işlenirken sorun oluştu - {e}")
        else:
            print(f"  Katman: {layer_name} için özellik bulunamadı/atlandı.")

    output_path = os.path.join(config.OUTPUT_IMAGES_DIR, f"{image_id}.png")
    base_image.save(output_path)
    print(f"Görsel kaydedildi: {output_path}")
    return output_path


def generate_all_images():

    all_nft_attributes = []
    generated_hashes = set()

    for i in range(1, config.TOTAL_NFTS + 1):
        nft_attributes = []


        generate_single_image(i, nft_attributes)
        all_nft_attributes.append(nft_attributes)


    print(f"\nToplam {config.TOTAL_NFTS} adet görsel oluşturuldu.")
    return all_nft_attributes


if __name__ == "__main__":
    print("Görsel oluşturucu başlatılıyor...")
    if not os.path.exists(config.LAYERS_DIR) or not os.listdir(config.LAYERS_DIR):
        print(f"Hata: '{config.LAYERS_DIR}' klasörü bulunamadı veya boş.")
        print("Lütfen katmanlarınızı bu klasöre ekleyin.")
    else:
        generated_attributes = generate_all_images()
