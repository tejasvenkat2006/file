import heapq
from collections import Counter

class Node:
    def __init__(self, char, freq):
        self.char = char
        self.freq = freq
        self.left = None
        self.right = None

    def __lt__(self, other):
        return self.freq < other.freq


def build_tree(text):
    frequency = Counter(text)
    heap = [Node(char, freq) for char, freq in frequency.items()]
    heapq.heapify(heap)

    while len(heap) > 1:
        left = heapq.heappop(heap)
        right = heapq.heappop(heap)

        merged = Node(None, left.freq + right.freq)
        merged.left = left
        merged.right = right

        heapq.heappush(heap, merged)

    return heap[0]


def generate_codes(node, current_code="", codes=None):
    if codes is None:
        codes = {}

    if node is None:
        return codes

    if node.char is not None:
        codes[node.char] = current_code

    generate_codes(node.left, current_code + "0", codes)
    generate_codes(node.right, current_code + "1", codes)

    return codes


def encode(text, codes):
    return ''.join(codes[char] for char in text)


def decode(encoded_text, tree):
    decoded = ""
    current = tree

    for bit in encoded_text:
        if bit == '0':
            current = current.left
        else:
            current = current.right

        if current.char is not None:
            decoded += current.char
            current = tree

    return decoded


# -------- MAIN --------

# If input() causes error, use fixed text
try:
    text = input("Enter text to compress: ")
    if text.strip() == "":
        text = "hello huffman"
except:
    text = "hello huffman"

tree = build_tree(text)
codes = generate_codes(tree)

encoded_text = encode(text, codes)
decoded_text = decode(encoded_text, tree)

print("\nOriginal Text:", text)

print("\nHuffman Codes:")
for char, code in codes.items():
    print(f"{repr(char)} : {code}")

print("\nEncoded (Compressed):", encoded_text)
print("Decoded (Original):", decoded_text)
