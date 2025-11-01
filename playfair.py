"""
playfair.py
Full Playfair cipher implementation with trace support.

Functions:
- prepare_key(key) -> 5x5 matrix
- preprocess_plaintext(text, pad_char='X') -> list of digraph tuples
- find_position(matrix, ch) -> (row,col)
- encrypt_pair / decrypt_pair
- encrypt_text(key, plaintext, pad_char='X', trace=False)
- decrypt_text(key, ciphertext, trace=False)
- pretty_print_matrix(matrix)
- _pair_trace_info helper
"""

from typing import List, Tuple

def prepare_key(key: str) -> List[List[str]]:
    key = key.upper().replace(" ", "")
    key = key.replace("J", "I")
    seen = set()
    matrix_letters = []
    for ch in key:
        if ch.isalpha() and ch not in seen:
            seen.add(ch)
            matrix_letters.append(ch)
    for ch in "ABCDEFGHIKLMNOPQRSTUVWXYZ":  # J skipped
        if ch not in seen:
            seen.add(ch)
            matrix_letters.append(ch)
    matrix = [matrix_letters[i*5:(i+1)*5] for i in range(5)]
    return matrix

def preprocess_plaintext(plaintext: str, pad_char: str = 'X') -> List[Tuple[str,str]]:
    filtered = []
    for ch in plaintext.upper():
        if ch.isalpha():
            if ch == 'J':
                filtered.append('I')
            else:
                filtered.append(ch)
    digraphs = []
    i = 0
    while i < len(filtered):
        a = filtered[i]
        if i + 1 < len(filtered):
            b = filtered[i + 1]
            if a == b:
                digraphs.append((a, pad_char))
                i += 1
            else:
                digraphs.append((a, b))
                i += 2
        else:
            digraphs.append((a, pad_char))
            i += 1
    return digraphs

def find_position(matrix: List[List[str]], ch: str) -> Tuple[int,int]:
    if ch == 'J':
        ch = 'I'
    for r in range(5):
        for c in range(5):
            if matrix[r][c] == ch:
                return r, c
    raise ValueError(f"Character {ch} not in key matrix")

def encrypt_pair(matrix: List[List[str]], a: str, b: str) -> str:
    ra, ca = find_position(matrix, a)
    rb, cb = find_position(matrix, b)
    if ra == rb:
        return matrix[ra][(ca + 1) % 5] + matrix[rb][(cb + 1) % 5]
    elif ca == cb:
        return matrix[(ra + 1) % 5][ca] + matrix[(rb + 1) % 5][cb]
    else:
        return matrix[ra][cb] + matrix[rb][ca]

def decrypt_pair(matrix: List[List[str]], a: str, b: str) -> str:
    ra, ca = find_position(matrix, a)
    rb, cb = find_position(matrix, b)
    if ra == rb:
        return matrix[ra][(ca - 1) % 5] + matrix[rb][(cb - 1) % 5]
    elif ca == cb:
        return matrix[(ra - 1) % 5][ca] + matrix[(rb - 1) % 5][cb]
    else:
        return matrix[ra][cb] + matrix[rb][ca]

def _pair_trace_info(matrix: List[List[str]], a: str, b: str, mode: str = 'encrypt'):
    """
    Return (result_pair, trace_line) describing the transformation of (a,b).
    mode in {'encrypt','decrypt'}.
    """
    ra, ca = find_position(matrix, a)
    rb, cb = find_position(matrix, b)
    if ra == rb:
        if mode == 'encrypt':
            res = matrix[ra][(ca + 1) % 5] + matrix[rb][(cb + 1) % 5]
            rule = "same row -> take right (wrap)"
        else:
            res = matrix[ra][(ca - 1) % 5] + matrix[rb][(cb - 1) % 5]
            rule = "same row -> take left (wrap)"
    elif ca == cb:
        if mode == 'encrypt':
            res = matrix[(ra + 1) % 5][ca] + matrix[(rb + 1) % 5][cb]
            rule = "same column -> take below (wrap)"
        else:
            res = matrix[(ra - 1) % 5][ca] + matrix[(rb - 1) % 5][cb]
            rule = "same column -> take above (wrap)"
    else:
        res = matrix[ra][cb] + matrix[rb][ca]
        rule = "rectangle -> swap columns"
    trace = f"Pair ({a},{b}): positions ({ra},{ca}) & ({rb},{cb}) | {rule} -> {res}"
    return res, trace

def encrypt_text(key: str, plaintext: str, pad_char: str = 'X', trace: bool = False):
    matrix = prepare_key(key)
    digraphs = preprocess_plaintext(plaintext, pad_char)
    parts = []
    trace_lines = []
    for a, b in digraphs:
        res, trace_line = _pair_trace_info(matrix, a, b, mode='encrypt')
        parts.append(res)
        trace_lines.append(trace_line)
    ciphertext = ''.join(parts)
    if trace:
        header = ["Key matrix:"]
        for row in matrix:
            header.append(' '.join(row))
        header.append("")
        header.append("Preprocessed digraphs: " + ', '.join([f"({a},{b})" for a,b in digraphs]))
        header.append("")
        return ciphertext, header + trace_lines + ["", f"Ciphertext: {ciphertext}"]
    return ciphertext

def decrypt_text(key: str, ciphertext: str, trace: bool = False):
    matrix = prepare_key(key)
    filtered = [ (ch if ch != 'J' else 'I') for ch in ciphertext.upper() if ch.isalpha() ]
    if len(filtered) % 2 != 0:
        raise ValueError("Ciphertext length must be even.")
    parts = []
    trace_lines = []
    digraphs = []
    for i in range(0, len(filtered), 2):
        a, b = filtered[i], filtered[i+1]
        digraphs.append((a,b))
        res, trace_line = _pair_trace_info(matrix, a, b, mode='decrypt')
        parts.append(res)
        trace_lines.append(trace_line)
    plaintext = ''.join(parts)
    if trace:
        header = ["Key matrix:"]
        for row in matrix:
            header.append(' '.join(row))
        header.append("")
        header.append("Cipher digraphs: " + ', '.join([f"({a},{b})" for a,b in digraphs]))
        header.append("")
        return plaintext, header + trace_lines + ["", f"Decrypted (raw): {plaintext}"]
    return plaintext

def pretty_print_matrix(matrix: List[List[str]]):
    print("\nPlayfair Cipher Matrix:")
    for row in matrix:
        print(" ".join(row))
    print()

if __name__ == "__main__":
    # quick smoke test
    key = "PLAYFAIR EXAMPLE"
    sample = "Hide the gold in the tree stump"
    print("Key matrix:")
    pretty_print_matrix(prepare_key(key))
    print("Plaintext:", sample)
    print("Digraphs:", preprocess_plaintext(sample))
    cipher = encrypt_text(key, sample)
    print("Ciphertext:", cipher)
    raw = decrypt_text(key, cipher)
    print("Decrypted (raw):", raw)
