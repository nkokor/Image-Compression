import tkinter as tk
from tkinter import filedialog, ttk
from PIL import Image, ImageTk
import os
import math
import numpy as np
import glob
from skimage.metrics import structural_similarity as compare_ssim
from compressors import huffman, lzw, jpeg, jpeg2000

# global variables
selected_image_path = None
selected_test_image = None

# --- helper functions for metrics ---
def calculate_compression_rate(original_path, compressed_path):
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
    psnr = 20 * math.log10(PIXEL_MAX / math.sqrt(mse))
    return psnr

def calculate_ssim(original_img, reconstructed_img):
    original = np.array(original_img.convert('L'))
    reconstructed = np.array(reconstructed_img.convert('L'))
    ssim, _ = compare_ssim(original, reconstructed, full=True)
    return ssim

# show result window with original and reconstructed image and metrics
def show_results_window(original_img, reconstructed_img, comp_rate, psnr, ssim, compressed_path, reconstructed_path):
    window = tk.Toplevel()
    window.title("Compression Results")
    window.geometry("600x500")

    frame = tk.Frame(window)
    frame.pack(pady=10)

    original_display = original_img.copy()
    original_display.thumbnail((200, 200))
    photo_orig = ImageTk.PhotoImage(original_display)
    orig_label = tk.Label(frame, image=photo_orig)
    orig_label.image = photo_orig
    orig_label.grid(row=0, column=0, padx=10)
    tk.Label(frame, text="Original").grid(row=1, column=0)

    recon_display = reconstructed_img.copy()
    recon_display.thumbnail((200, 200))
    photo_recon = ImageTk.PhotoImage(recon_display)
    recon_label = tk.Label(frame, image=photo_recon)
    recon_label.image = photo_recon
    recon_label.grid(row=0, column=1, padx=10)
    tk.Label(frame, text="Reconstructed").grid(row=1, column=1)

    metrics_frame = tk.Frame(window)
    metrics_frame.pack(pady=10)

    tk.Label(metrics_frame, text=f"Compressed file: {compressed_path}", wraplength=550, justify="left").pack()
    tk.Label(metrics_frame, text=f"Reconstructed image: {reconstructed_path}", wraplength=550, justify="left").pack()
    tk.Label(metrics_frame, text=f"Compression Rate: {comp_rate:.2f}").pack()
    tk.Label(metrics_frame, text=f"PSNR: {psnr:.2f} dB").pack()
    tk.Label(metrics_frame, text=f"SSIM: {ssim:.4f}").pack()

# get list of test images from folder
def get_test_images():
    image_extensions = ('*.png', '*.jpg', '*.jpeg', '*.bmp', '*.tiff', '*.pgm')
    image_files = []
    for ext in image_extensions:
        image_files.extend(glob.glob(f"test_images/{ext}"))
    image_files = [os.path.basename(path) for path in image_files]
    return image_files

# select image from combobox
def select_test_image(event=None):
    global selected_image_path
    global selected_test_image
    filename = test_images_combo.get()
    if filename:
        selected_test_image = filename
        selected_image_path = os.path.join("test_images", filename)
        img = Image.open(selected_image_path)
        img.thumbnail((200, 200))
        photo = ImageTk.PhotoImage(img)
        image_label.config(image=photo)
        image_label.image = photo
        info_label.config(text=f"Selected image: {filename}")

# upload image from disk
def open_image():
    global selected_image_path
    file_path = filedialog.askopenfilename(
        title="Select an image",
        filetypes=[("Image files", "*.bmp *.png *.tiff *.jpg *.pgm")]
    )
    if file_path:
        selected_image_path = file_path
        img = Image.open(file_path)
        img.thumbnail((200, 200))
        photo = ImageTk.PhotoImage(img)
        image_label.config(image=photo)
        image_label.image = photo
        info_label.config(text=f"Selected image: {os.path.basename(file_path)}")
        test_images_combo.set('')

# compress image and show results
def compress_image():
    if not selected_image_path:
        result_text.set("You haven't selected an image.")
        return
    algorithm = selected_algorithm.get()
    if not algorithm:
        result_text.set("You haven't selected an algorithm.")
        return

    try:
        filename = os.path.splitext(os.path.basename(selected_image_path))[0]
        compressed_path = f"results/{filename}_{algorithm.lower()}.bin"
        reconstructed_path = f"results/{filename}_{algorithm.lower()}_reconstructed.png"
        os.makedirs("results", exist_ok=True)

        if algorithm == "Huffman":
            huffman.compress(selected_image_path, compressed_path)
            huffman.decompress(compressed_path, reconstructed_path)
        elif algorithm == "LZW":
            lzw.compress(selected_image_path, compressed_path)
            lzw.decompress(compressed_path, reconstructed_path)
        elif algorithm == 'JPEG':
            jpeg.compress(selected_image_path, compressed_path)
            jpeg.decompress(compressed_path, reconstructed_path)
        elif algorithm == 'JPEG 2000':
            jpeg.compress(selected_image_path, compressed_path)
            jpeg.decompress(compressed_path, reconstructed_path)
        else:
            result_text.set("This algorithm is not implemented yet.")
            return

        original_img = Image.open(selected_image_path).convert("RGB")
        reconstructed_img = Image.open(reconstructed_path).convert("RGB")

        comp_rate = calculate_compression_rate(selected_image_path, compressed_path)
        psnr = calculate_psnr(original_img, reconstructed_img)
        ssim = calculate_ssim(original_img, reconstructed_img)

        show_results_window(original_img, reconstructed_img, comp_rate, psnr, ssim, compressed_path, reconstructed_path)

        result_text.set("Compression and analysis completed.\nSee results in new window.")
    except Exception as e:
        result_text.set(f"Error: {e}")

# gui
root = tk.Tk()
root.title("Image Compression App")
root.geometry("800x650")

selected_algorithm = tk.StringVar()

tk.Label(root, text="Select an image from test_images folder:").pack(pady=(10, 0))
test_images_combo = ttk.Combobox(root, state="readonly")
test_images_combo['values'] = get_test_images()
test_images_combo.pack()
test_images_combo.bind("<<ComboboxSelected>>", select_test_image)

tk.Label(root, text="Or upload a new image:").pack(pady=(10, 0))
tk.Button(root, text="Upload an image", command=open_image).pack(pady=5)

image_label = tk.Label(root)
image_label.pack()
info_label = tk.Label(root, text="No image selected")
info_label.pack()

tk.Label(root, text="Select an algorithm:").pack(pady=(10, 0))
algo_menu = ttk.Combobox(root, textvariable=selected_algorithm, state="readonly")
algo_menu['values'] = ["Huffman", "LZW", "JPEG", "JPEG 2000"]
algo_menu.pack()

tk.Button(root, text="Compress", command=compress_image).pack(pady=10)

result_text = tk.StringVar()
tk.Label(root, textvariable=result_text, wraplength=700, justify="left", fg="blue").pack(pady=10)

root.mainloop()