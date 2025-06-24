import heapq
import os
from collections import defaultdict
from PIL import Image
import pickle
import struct

# huffman tree node
class Node:
    def __init__(self, symbol=None, freq=0):
        self.symbol = symbol
        self.freq = freq
        self.left = None
        self.right = None

    def __lt__(self, other):
        return self.freq < other.freq

# build frequency table from input data
def build_frequency_table(data):
    freq = defaultdict(int)
    for byte in data:
        freq[byte] += 1
    return freq

# construct the huffman tree using a priority queue
def build_huffman_tree(freq_table):
    heap = [Node(symbol, freq) for symbol, freq in freq_table.items()]
    heapq.heapify(heap)

    while len(heap) > 1:
        n1 = heapq.heappop(heap)
        n2 = heapq.heappop(heap)
        merged = Node(freq=n1.freq + n2.freq)
        merged.left = n1
        merged.right = n2
        heapq.heappush(heap, merged)

    return heap[0]

# assign binary codes to each symbol by traversing the tree
def build_codes(root):
    codes = {}

    def traverse(node, code=""):
        if node is None:
            return
        if node.symbol is not None:
            codes[node.symbol] = code
            return
        traverse(node.left, code + "0")
        traverse(node.right, code + "1")

    traverse(root)
    return codes

# encode raw data into a binary bitstring using the huffman codes
def encode_data(data, codes):
    bitstring = ''.join(codes[byte] for byte in data)

    # add padding to make length divisible by 8
    padding = 8 - len(bitstring) % 8
    bitstring += '0' * padding
    padding_info = '{0:08b}'.format(padding)
    bitstring = padding_info + bitstring

    compressed_bytes = bytearray()
    for i in range(0, len(bitstring), 8):
        byte = bitstring[i:i+8]
        compressed_bytes.append(int(byte, 2))

    return compressed_bytes

# decode bitstring back to original data
def decode_data(compressed_bytes, codes):
    inverse_codes = {v: k for k, v in codes.items()}
    bitstring = ''
    for byte in compressed_bytes:
        bitstring += f"{byte:08b}"

    padding = int(bitstring[:8], 2)
    bitstring = bitstring[8:-padding] if padding > 0 else bitstring[8:]

    decoded = []
    code = ''
    for bit in bitstring:
        code += bit
        if code in inverse_codes:
            decoded.append(inverse_codes[code])
            code = ''
    return decoded

# compress an RGB image using huffman coding per channel
def compress(input_image_path, output_path):
    image = Image.open(input_image_path).convert("RGB")
    r, g, b = image.split()

    channels = [r.tobytes(), g.tobytes(), b.tobytes()]
    codes_list = []
    compressed_data_list = []

    for channel in channels:
        freq_table = build_frequency_table(channel)
        tree = build_huffman_tree(freq_table)
        codes = build_codes(tree)
        compressed = encode_data(channel, codes)

        codes_list.append(codes)
        compressed_data_list.append(compressed)

    with open(output_path, "wb") as f:
        # write image dimensions
        f.write(struct.pack("II", image.width, image.height))

        for codes, compressed in zip(codes_list, compressed_data_list):
            codes_pickle = pickle.dumps(codes)
            f.write(struct.pack("I", len(codes_pickle)))     # length of pickle data
            f.write(codes_pickle)                            # pickle data
            f.write(struct.pack("I", len(compressed)))       # length of compressed bytes
            f.write(compressed)                              # compressed byte data

# decompress a huffman-coded RGB image
def decompress(input_path, output_image_path):
    with open(input_path, "rb") as f:
        width, height = struct.unpack("II", f.read(8))
        channels = []

        for _ in range(3):
            codes_length = struct.unpack("I", f.read(4))[0]
            codes = pickle.loads(f.read(codes_length))
            compressed_length = struct.unpack("I", f.read(4))[0]
            compressed_data = f.read(compressed_length)
            decompressed = decode_data(compressed_data, codes)
            channels.append(bytes(decompressed))

    r = Image.frombytes("L", (width, height), channels[0])
    g = Image.frombytes("L", (width, height), channels[1])
    b = Image.frombytes("L", (width, height), channels[2])
    image = Image.merge("RGB", (r, g, b))
    image.save(output_image_path)
