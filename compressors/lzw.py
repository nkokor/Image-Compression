import os
from collections import defaultdict
from PIL import Image
import struct

# compress an RGB image using LZW per channel
def compress(input_image_path, output_path):
    image = Image.open(input_image_path).convert("RGB")
    r, g, b = image.split()

    channels = [r.tobytes(), g.tobytes(), b.tobytes()]
    compressed_channels = []

    for channel in channels:
        compressed = lzw_compress(channel)
        compressed_channels.append(compressed)

    with open(output_path, "wb") as f:
        f.write(struct.pack("II", image.width, image.height))

        for compressed in compressed_channels:
            f.write(struct.pack("I", len(compressed)))
            f.write(bytes(compressed))

# cecompress LZW-compressed RGB image
def decompress(input_path, output_image_path):
    with open(input_path, "rb") as f:
        width, height = struct.unpack("II", f.read(8))
        channels = []

        for _ in range(3):
            length = struct.unpack("I", f.read(4))[0]
            compressed = list(f.read(length))
            decompressed = lzw_decompress(compressed)
            channels.append(bytes(decompressed))

    r = Image.frombytes("L", (width, height), channels[0])
    g = Image.frombytes("L", (width, height), channels[1])
    b = Image.frombytes("L", (width, height), channels[2])
    image = Image.merge("RGB", (r, g, b))
    image.save(output_image_path)

# LZW compression algorithm
def lzw_compress(uncompressed):
    dict_size = 256
    dictionary = {bytes([i]): i for i in range(dict_size)}

    w = b""
    result = []

    for c in uncompressed:
        wc = w + bytes([c])
        if wc in dictionary:
            w = wc
        else:
            result.append(dictionary[w])
            dictionary[wc] = dict_size
            dict_size += 1
            w = bytes([c])

    if w:
        result.append(dictionary[w])

    # convert codes to byte stream (4 bytes per code)
    output_bytes = []
    for code in result:
        output_bytes.extend(struct.pack("I", code))  # 4 bytes per code
    return output_bytes

# LZW decompression algorithm
def lzw_decompress(compressed_bytes):
    dict_size = 256
    dictionary = {i: bytes([i]) for i in range(dict_size)}

    compressed = [struct.unpack("I", bytes(compressed_bytes[i:i+4]))[0] for i in range(0, len(compressed_bytes), 4)]

    w = bytes([compressed.pop(0)])
    result = bytearray(w)

    for k in compressed:
        if k in dictionary:
            entry = dictionary[k]
        elif k == dict_size:
            entry = w + bytes([w[0]])
        else:
            raise ValueError("Bad compressed k: %s" % k)

        result.extend(entry)
        dictionary[dict_size] = w + bytes([entry[0]])
        dict_size += 1
        w = entry

    return result
