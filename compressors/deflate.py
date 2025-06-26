import zlib
from PIL import Image
import struct
import os
import numpy as np

def compress(input_image_path, output_path):
    image = Image.open(input_image_path).convert("RGB")
    r, g, b = image.split()

    channels = [r.tobytes(), g.tobytes(), b.tobytes()]
    compressed_channels = [zlib.compress(channel, level=9) for channel in channels]

    with open(output_path, "wb") as f:
        f.write(struct.pack("II", image.width, image.height))
        for data in compressed_channels:
            f.write(struct.pack("I", len(data)))
            f.write(data)


def decompress(input_path, output_image_path):
    with open(input_path, "rb") as f:
        width, height = struct.unpack("II", f.read(8))
        channels = []

        for _ in range(3):
            length = struct.unpack("I", f.read(4))[0]
            data = f.read(length)
            decompressed = zlib.decompress(data)
            channels.append(bytes(decompressed))

    r = Image.frombytes("L", (width, height), channels[0])
    g = Image.frombytes("L", (width, height), channels[1])
    b = Image.frombytes("L", (width, height), channels[2])
    image = Image.merge("RGB", (r, g, b))
    image.save(output_image_path)