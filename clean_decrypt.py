# clean_decrypt.py
def naive_clean_decrypted(text: str) -> str:
    # remove trailing pad
    if text.endswith('X'):
        text = text[:-1]

    # remove X inserted between identical letters: e.g. A X A -> A A  => keep single A
    out = []
    i = 0
    while i < len(text):
        if i + 2 < len(text) and text[i] == text[i+2] and text[i+1] == 'X':
            out.append(text[i])
            # skip the X, move to the next letter (i+2)
            i += 2
        else:
            out.append(text[i])
            i += 1
    return ''.join(out)

if __name__ == "__main__":
    # paste the raw decrypted text you get from the CLI here:
    raw = "HIDETHEGOLDINTHETREEXSTUMPX"  # replace with your actual raw output
    cleaned = naive_clean_decrypted(raw)
    print("Raw decrypted :", raw)
    print("Naive cleaned  :", cleaned)
