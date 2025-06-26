from PIL import Image

def compress(input_image_path, output_path, quality=75):
    image = Image.open(input_image_path).convert("RGB")
    image.save(output_path, format="JPEG", quality=quality, subsampling=0, optimize=True)

def decompress(input_path, output_image_path):
    image = Image.open(input_path).convert("RGB")
    image.save(output_image_path, format="PNG")
