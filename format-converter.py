from PIL import Image
import os

input_folder = "test_images"
input_filename = "baboon.bmp"
input_path = os.path.join(input_folder, input_filename)

img = Image.open(input_path)

formats = ["jpeg", "png", "webp", "gif", "tiff"]

for fmt in formats:
    base_name = os.path.splitext(input_filename)[0]
    output_filename = f"{base_name}.{fmt}"
    output_path = os.path.join(input_folder, output_filename)

    if fmt == "gif":
        img_converted = img.convert("P")
    else:
        img_converted = img

    img_converted.save(output_path, format=fmt.upper())

    print(f"Saved {output_path}")
