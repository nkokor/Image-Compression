import os
from tkinter import filedialog
import glob
import tkinter as tk
import numpy as np
from PIL import Image, ImageTk
from skimage.metrics import structural_similarity as compare_ssim
import ttkbootstrap as ttk
from ttkbootstrap.constants import *

from compressors import huffman, lzw, deflate, jpeg, jpeg2000

from metrics import calculate_compression_rate, calculate_psnr, calculate_ssim

selected_image_path = None
selected_test_image = None

def show_results_window(original_img, reconstructed_img, comp_rate, psnr, ssim, compressed_path, reconstructed_path):
    window = tk.Toplevel()
    window.title("Compression Results")
    window.geometry("600x500")
    frame = ttk.Frame(window)
    frame.pack(pady=10)
    original_display = original_img.copy()
    original_display.thumbnail((200, 200))
    photo_orig = ImageTk.PhotoImage(original_display)
    orig_label = ttk.Label(frame, image=photo_orig)
    orig_label.image = photo_orig
    orig_label.grid(row=0, column=0, padx=10)
    ttk.Label(frame, text="Original").grid(row=1, column=0)
    recon_display = reconstructed_img.copy()
    recon_display.thumbnail((200, 200))
    photo_recon = ImageTk.PhotoImage(recon_display)
    recon_label = ttk.Label(frame, image=photo_recon)
    recon_label.image = photo_recon
    recon_label.grid(row=0, column=1, padx=10)
    ttk.Label(frame, text="Reconstructed").grid(row=1, column=1)
    metrics_frame = ttk.Frame(window)
    metrics_frame.pack(pady=10)
    ttk.Label(metrics_frame, text=f"Compressed file: {compressed_path}", wraplength=550, justify="left").pack()
    ttk.Label(metrics_frame, text=f"Reconstructed image: {reconstructed_path}", wraplength=550, justify="left").pack()
    ttk.Label(metrics_frame, text=f"Compression Rate: {comp_rate:.2f}").pack()
    ttk.Label(metrics_frame, text=f"PSNR: {psnr:.2f} dB").pack()
    ttk.Label(metrics_frame, text=f"SSIM: {ssim:.4f}").pack()

def get_test_images():
    image_extensions = ('*.png', '*.jpg', '*.jpeg', '*.bmp', '*.tiff', '*.pgm')
    image_files = []
    for ext in image_extensions:
        image_files.extend(glob.glob(f"test_images/{ext}"))
    return [os.path.basename(path) for path in image_files]

def select_test_image(event=None):
    global selected_image_path, selected_test_image
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

def open_image():
    global selected_image_path
    file_path = tk.filedialog.askopenfilename(
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
        compressed_path = f"results/{filename}_{algorithm.lower().replace(' ', '')}.bin"
        reconstructed_path = f"results/{filename}_{algorithm.lower().replace(' ', '')}_reconstructed.png"
        os.makedirs("results", exist_ok=True)
        if algorithm == "Huffman":
            huffman.compress(selected_image_path, compressed_path)
            huffman.decompress(compressed_path, reconstructed_path)
        elif algorithm == "LZW":
            lzw.compress(selected_image_path, compressed_path)
            lzw.decompress(compressed_path, reconstructed_path)
        elif algorithm == "DEFLATE":
            deflate.compress(selected_image_path, compressed_path)
            deflate.decompress(compressed_path, reconstructed_path)
        elif algorithm == "JPEG":
            quality = selected_jpeg_quality.get()
            jpeg.compress(selected_image_path, compressed_path, quality=quality)
            jpeg.decompress(compressed_path, reconstructed_path)
        elif algorithm == "JPEG 2000":
            ratio = selected_compression_ratio.get()
            jpeg2000.compress(selected_image_path, compressed_path, compression_ratio=ratio)
            jpeg2000.decompress(compressed_path, reconstructed_path)
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

app = ttk.Window(themename="flatly")
app.title("Image Compression App")
app.geometry("900x700")

selected_algorithm = tk.StringVar()
selected_compression_ratio = tk.IntVar(value=10)
selected_jpeg_quality = tk.IntVar(value=75)

main_frame = ttk.Frame(app, padding=20)
main_frame.pack(fill="both", expand=True)

top_frame = ttk.Frame(main_frame)
top_frame.pack(fill="x", pady=10)

image_select_frame = ttk.Labelframe(top_frame, text="Select Image", padding=10)
image_select_frame.pack(side="left", fill="both", expand=True, padx=10)

ttk.Label(image_select_frame, text="Choose from test_images:").pack(anchor="w")
test_images_combo = ttk.Combobox(image_select_frame, state="readonly")
test_images_combo['values'] = get_test_images()
test_images_combo.pack(fill="x")
test_images_combo.bind("<<ComboboxSelected>>", select_test_image)

ttk.Label(image_select_frame, text="Or upload a new image:").pack(anchor="w", pady=(10, 0))
ttk.Button(image_select_frame, text="Upload an image", command=open_image, bootstyle="secondary").pack(pady=5)

info_label = ttk.Label(image_select_frame, text="No image selected", bootstyle="info")
info_label.pack(pady=(10, 0))

image_label = ttk.Label(image_select_frame)
image_label.pack(pady=10)

algorithm_frame = ttk.Labelframe(top_frame, text="Compression Settings", padding=10)
algorithm_frame.pack(side="right", fill="both", expand=True, padx=10)

ttk.Label(algorithm_frame, text="Select an algorithm:").pack(anchor="w")
algo_menu = ttk.Combobox(algorithm_frame, textvariable=selected_algorithm, state="readonly")
algo_menu['values'] = ["Huffman", "LZW", "DEFLATE", "JPEG", "JPEG 2000"]
algo_menu.pack(fill="x")

ratio_label = ttk.Label(algorithm_frame, text="Compression Ratio (JPEG 2000 only):")
ratio_combo = ttk.Combobox(algorithm_frame, textvariable=selected_compression_ratio, state="readonly")
ratio_combo['values'] = [5, 10, 20, 50]
ratio_combo.current(1)
ratio_label.pack_forget()
ratio_combo.pack_forget()

jpeg_quality_label = ttk.Label(algorithm_frame, text="JPEG Quality:")
jpeg_quality_combo = ttk.Combobox(algorithm_frame, textvariable=selected_jpeg_quality, state="readonly")
jpeg_quality_combo['values'] = [30, 50, 75, 90, 95, 100]
jpeg_quality_combo.set(75)
jpeg_quality_label.pack_forget()
jpeg_quality_combo.pack_forget()

def on_algorithm_change(event=None):
    algo = selected_algorithm.get()
    if algo == "JPEG 2000":
        ratio_label.pack(pady=(10, 0), anchor="w")
        ratio_combo.pack(fill="x")
        jpeg_quality_label.pack_forget()
        jpeg_quality_combo.pack_forget()
    elif algo == "JPEG":
        jpeg_quality_label.pack(pady=(10, 0), anchor="w")
        jpeg_quality_combo.pack(fill="x")
        ratio_label.pack_forget()
        ratio_combo.pack_forget()
    else:
        ratio_label.pack_forget()
        ratio_combo.pack_forget()
        jpeg_quality_label.pack_forget()
        jpeg_quality_combo.pack_forget()

selected_algorithm.trace_add('write', lambda *args: on_algorithm_change())

bottom_frame = ttk.Frame(main_frame)
bottom_frame.pack(fill="x", pady=20)

ttk.Button(bottom_frame, text="Compress", command=compress_image, bootstyle="success outline", width=20).pack(pady=10)

result_text = tk.StringVar()
ttk.Label(bottom_frame, textvariable=result_text, wraplength=700, justify="left", bootstyle="info").pack(pady=10)

app.mainloop()
