import heapq
from collections import Counter
import math

sample_text_ukr = """Для досягнення бажаного результату важливо обрати перевірене та надійне рішення."""

print("="*50)
print(f"1. Початковий текст ({len(sample_text_ukr.split())} слів)")
print(sample_text_ukr)
print("="*50)

# Обробка тексту
def preprocess_text(text):
    text = text.lower()
    allowed_chars = "абвгдеєжзиіїйклмнопрстуфхцчшщьюя "  # Літери та пробіл
    cleaned_text = ''.join(filter(lambda char: char in allowed_chars, text))
    cleaned_text = ' '.join(cleaned_text.split())  # Видалення зайвих пробілів
    return cleaned_text

processed_text = preprocess_text(sample_text_ukr)
print(f"2. Оброблений текст ({len(processed_text.split())} слів)")
print(processed_text)
print("="*50)

# Кодування Хаффмана
class HuffmanNode:
    def __init__(self, char, freq):
        self.char = char
        self.freq = freq
        self.left = None
        self.right = None
    def __lt__(self, other):
        return self.freq < other.freq

def build_huffman_tree(text):
    if not text: return None
    frequency = Counter(text)
    priority_queue = [HuffmanNode(char, freq) for char, freq in frequency.items()]
    heapq.heapify(priority_queue)
    while len(priority_queue) > 1:
        left = heapq.heappop(priority_queue)
        right = heapq.heappop(priority_queue)
        merged = HuffmanNode(None, left.freq + right.freq)
        merged.left = left
        merged.right = right
        heapq.heappush(priority_queue, merged)
    return priority_queue[0] if priority_queue else None

def generate_huffman_codes(node, prefix="", codebook={}):
    if node is None:
        return codebook
    if node.char is not None:
        codebook[node.char] = prefix if prefix else "0"
    else:
        generate_huffman_codes(node.left, prefix + "0", codebook)
        generate_huffman_codes(node.right, prefix + "1", codebook)
    return codebook

def huffman_encode(text, codebook):
    return "".join([codebook[char] for char in text if char in codebook])

huffman_tree_root = build_huffman_tree(processed_text)
huffman_codes = generate_huffman_codes(huffman_tree_root, codebook={})
encoded_bits = huffman_encode(processed_text, huffman_codes)

print("3. Кодування Хаффмана")
if encoded_bits:
    print("Таблиця кодів Хаффмана:")
    print(f"{'Символ':^10} | {'Код':^10}")
    print("-" * 23)
    for char, code in sorted(huffman_codes.items()):
        char_repr = "'space'" if char == ' ' else char
        print(f"{char_repr:^10} | {code:^10}")
    print("-" * 23)
    print("\nЗакодована бітова послідовність:")
    print(encoded_bits)
    print(f"(Довжина: {len(encoded_bits)} біт)")
else:
    print("Текст порожній або неможливо згенерувати коди.")
print("="*50)

# Алгоритм перестановки
def permute_matrix_simple(text, num_cols):
    if not text or num_cols <= 0:
        return ""
    text_len = len(text)
    num_rows = math.ceil(text_len / num_cols)
    padded_text = text.ljust(num_rows * num_cols, '0')
    matrix = [padded_text[i:i + num_cols] for i in range(0, len(padded_text), num_cols)]
    permuted_text = ""
    for col_idx in range(num_cols):
        for row_idx in range(num_rows):
            permuted_text += matrix[row_idx][col_idx]
    return permuted_text

cols_for_permutation = 8

if encoded_bits:
    permuted_bits_simple = permute_matrix_simple(encoded_bits, cols_for_permutation)
    print(f"4. Матрична перестановка ({cols_for_permutation} стовпців)")
    print("Бітова послідовність після перестановки:")
    print(permuted_bits_simple)
    print(f"(Довжина: {len(permuted_bits_simple)} біт)")
else:
    print("Перестановка пропущена (немає бітової послідовності).")
print("="*50)

# Ключ
print("5. Інформація про ключ для перестановки")
print(f"Кількість стовпців (ключ): {cols_for_permutation}")
print("Зчитування: стовпцями зверху вниз.")
print("="*50)

# Квадрат Полібія
def build_polybius_square_ukr(size=6):
    alphabet = "абвгґдеєжзиіїйклмнопрстуфхцчшщьюя .,"
    square = {}
    reverse_square = {}
    k = 0
    for r in range(1, size + 1):
        for c in range(1, size + 1):
            if k < len(alphabet):
                char = alphabet[k]
                coord = f"{r}{c}"
                square[char] = coord
                reverse_square[coord] = char
                k += 1
    return square, reverse_square

def polybius_encrypt(text, square):
    encrypted = ""
    for char in text:
        encrypted += square.get(char, "")
    return encrypted

def polybius_decrypt(text, reverse_square):
    decrypted = ""
    if len(text) % 2 != 0:
        text = text[:-1]
    for i in range(0, len(text), 2):
        coord = text[i:i+2]
        decrypted += reverse_square.get(coord, "?")
    return decrypted

polybius_map, polybius_reverse_map = build_polybius_square_ukr(size=6)

print("6. Квадрат Полібія")
print("Таблиця символів та їх координат:")
print(f"{'Символ':^6} | {'Координата':^10}")
print("-" * 19)
for char, coord in sorted(polybius_map.items()):
    print(f"{char:^6} | {coord:^10}")
print("-" * 19)

if processed_text:
    encrypted_polybius = polybius_encrypt(processed_text, polybius_map)
    decrypted_polybius = polybius_decrypt(encrypted_polybius, polybius_reverse_map)

    print("\nРезультат шифрування Полібієм:")
    print(f"Оброблений текст:     '{processed_text}'")
    print(f"Зашифрований текст:    '{encrypted_polybius}'")
    print(f"Розшифрований текст:   '{decrypted_polybius}'")
    print(f"Розшифровка співпадає: {''.join(filter(lambda c: c in polybius_map, processed_text)) == decrypted_polybius}")
else:
    print("(Шифрування Полібія пропущено)")
print("="*50)
