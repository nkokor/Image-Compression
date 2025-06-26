from PIL import Image
import os

def compress(input_image_path, output_path):
    image = Image.open(input_image_path).convert("RGB")
    # save image as JPEG with quality=75 and no chroma subsampling
    image.save(output_path, format="JPEG", quality=75, subsampling=0, optimize=True)

def decompress(input_path, output_image_path):
    image = Image.open(input_path).convert("RGB")
    image.save(output_image_path, format="PNG")
