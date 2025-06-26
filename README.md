# 🖼️ Image Compression GUI Application (Huffman, LZW, DEFLATE, JPEG, JPEG 2000)

This application provides a simple and intuitive interface for experimenting with five image compression algorithms: **Huffman**, **LZW**, **DEFLATE**, **JPEG**, and **JPEG 2000**. It is developed in Python using the Tkinter library for the GUI, and follows a modular project structure that makes it easy to maintain, expand, and evaluate.


### 💡 Purpose
The main purpose of this application is to simplify the testing and comparison of various image compression algorithms. It allows users to experiment without writing additional code, track performance through relevant metrics, and visually evaluate the quality of reconstructed images. The modular structure also allows for easy future extensions. This application was developed as part of my master's thesis, where I focused on methods and algorithms for image compression in multimedia systems.


# 📂 Project Structure
```bash
.
├── compressors/           # Contains individual Python scripts for each compression algorithm
│   ├── huffman.py
│   ├── lzw.py
│   ├── deflate.py
│   ├── jpeg_module.py
│   └── jpeg2000.py
├── test_images/           # Test images used for evaluation
├── results/               # Output directory for compressed and reconstructed images
├── metrics.py             # Compression quality metric calculations (compression rate, PSNR, SSIM)
├── main.py                # Main script that launches the GUI and integrates all components
└── README.md              
```

# 📖 How to run


### Clone the repository

```bash
git clone https://github.com/nkokor/Image-Compression.git
cd Image-Compression
```


### Install dependencies
Install the required libraries using pip:

```bash
pip install pillow numpy glymur ttkbootstrap scikit-image
```
⚠️ Important: The glymur library requires OpenJPEG version 2.3 or higher to be installed on your system.


### ▶️ Running the Application
Once all dependencies are installed, you can start the application by running:

```bash
python main.py
```

This will launch the graphical interface, where you can:

- Select one of the available test images or upload your own image
- Choose a compression algorithm from a dropdown menu
- If JPEG or JPEG 2000 is selected, choose the desired quality or compression ratio
- Click the Compress button to start the compression process

After compression is complete, decompression is automatically performed, and both the original and reconstructed images are displayed side-by-side. Additionally, compression metrics such as Compression Ratio, PSNR, and SSIM are shown in the results window.
