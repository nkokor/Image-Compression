import math
import numpy as np
from PIL import Image
from skimage.metrics import structural_similarity as compare_ssim

def calculate_compression_rate(original_path, compressed_path):
    import os
    original_size = os.path.getsize(original_path)
    compressed_size = os.path.getsize(compressed_path)
    return original_size / compressed_size if compressed_size != 0 else 0

def calculate_psnr(original_img, reconstructed_img):
    original = np.array(original_img).astype(np.float64)
    reconstructed = np.array(reconstructed_img).astype(np.float64)
    mse = np.mean((original - reconstructed) ** 2)
    if mse == 0:
        return float('inf')
    PIXEL_MAX = 255.0
    return 20 * math.log10(PIXEL_MAX / math.sqrt(mse))

def calculate_ssim(original_img, reconstructed_img):
    original = np.array(original_img.convert('L'))
    reconstructed = np.array(reconstructed_img.convert('L'))
    ssim, _ = compare_ssim(original, reconstructed, full=True)
    return ssim
