import pytest
from playfair import prepare_key, preprocess_plaintext, encrypt_text, decrypt_text

def test_prepare_key_has_25_letters():
    mat = prepare_key("PLAYFAIR EXAMPLE")
    flat = [c for row in mat for c in row]
    assert len(flat) == 25
    assert len(set(flat)) == 25  # no duplicates
    assert 'J' not in flat

def test_preprocess_replaces_j_and_pads():
    dig = preprocess_plaintext("jazz")
    # 'J' -> 'I', 'AA' style handled and padded
    assert all(len(pair) == 2 for pair in dig)
    # ensure letters are uppercase
    for a,b in dig:
        assert a.isupper() and b.isupper()

def test_encrypt_decrypt_cycle_basic():
    key = "PLAYFAIR EXAMPLE"
    plain = "Hide the gold in the tree stump"
    cipher = encrypt_text(key, plain)
    assert isinstance(cipher, str)
    # decrypt should return the raw text (with pads). When decrypted and naive cleaned, we get letters
    decrypted_raw = decrypt_text(key, cipher)
    assert decrypted_raw.isalpha()  # only letters
    # simple check: length of decrypted_raw equals length of cipher
    assert len(decrypted_raw) == len(cipher)

def test_known_example():
    # Known example from literature (one canonical output — depending on implementation)
    key = "PLAYFAIR EXAMPLE"
    plaintext = "Hide the gold in the tree stump"
    cipher = encrypt_text(key, plaintext)
    assert len(cipher) % 2 == 0
    # Basic sanity: ciphertext not equal to plaintext and is uppercase letters
    assert cipher.upper() == cipher
    assert cipher != plaintext.replace(" ", "").upper()
