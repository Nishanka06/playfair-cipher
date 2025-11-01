# decrypt_and_clean.py
# Decrypt ciphertext using playfair.decrypt_text and apply a conservative heuristic to remove padding X's.
# Usage:
#   python decrypt_and_clean.py <KEY> <CIPHERTEXT>
# Example:
#   python decrypt_and_clean.py "PLAYFAIR EXAMPLE" BMODZBXDNABEKUDMUIXMMOUVIF

import sys
from playfair import decrypt_text

def heuristic_clean(text: str) -> str:
    """
    Heuristic cleaning:
    - remove trailing single 'X' if it was likely a padding
    - collapse patterns A X A -> A A (i.e., remove X inserted between identical letters)
    This tries to preserve legitimate X where possible.
    """
    if not text:
        return text

    # 1) remove trailing X (common padding)
    if text.endswith('X'):
        text = text[:-1]

    # 2) collapse A X A -> AA
    out_chars = []
    i = 0
    n = len(text)
    while i < n:
        # check pattern char, 'X', same char
        if i + 2 < n and text[i+1] == 'X' and text[i] == text[i+2]:
            out_chars.append(text[i])  # keep one occurrence
            i += 3  # skip the pattern A X A
        else:
            out_chars.append(text[i])
            i += 1

    return ''.join(out_chars)

def main():
    if len(sys.argv) < 3:
        print("Usage: python decrypt_and_clean.py \"KEY\" CIPHERTEXT")
        print("Example: python decrypt_and_clean.py \"PLAYFAIR EXAMPLE\" BMODZBXDNABEKUDMUIXMMOUVIF")
        sys.exit(1)

    key = sys.argv[1]
    ciphertext = sys.argv[2]

    # decrypt (raw)
    try:
        raw = decrypt_text(key, ciphertext)
    except Exception as e:
        print("Error during decryption:", e)
        sys.exit(1)

    cleaned = heuristic_clean(raw)

    print("Raw decrypted :", raw)
    print("Heuristic cleaned:", cleaned)

if __name__ == "__main__":
    main()
