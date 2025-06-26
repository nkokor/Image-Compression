from PIL import Image
import numpy as np
import glymur

def compress(input_image_path, output_path, compression_ratio=10):
    image = Image.open(input_image_path).convert("RGB")
    image_np = np.array(image)

    # lossy compression with selected compression ratio
    glymur.Jp2k(output_path, data=image_np, cratios=[compression_ratio])

def decompress(input_path, output_image_path):
    jp2 = glymur.Jp2k(input_path)
    image_data = jp2[:]
    image = Image.fromarray(image_data)
    image = image.convert("RGB")
    image.save(output_image_path, format="PNG")
