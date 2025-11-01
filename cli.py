#!/usr/bin/env python3
import argparse
import sys
from playfair import encrypt_text, decrypt_text, pretty_print_matrix, prepare_key

def main():
    parser = argparse.ArgumentParser(description="Playfair cipher CLI")
    sub = parser.add_subparsers(dest="command", required=True)

    # encrypt subcommand
    enc = sub.add_parser("encrypt", help="Encrypt plaintext")
    enc.add_argument("--key", "-k", required=True, help="Keyword for key matrix")
    enc.add_argument("--text", "-t", help="Plaintext to encrypt (mutually exclusive with --infile)")
    enc.add_argument("--infile", "-i", help="Input file with plaintext")
    enc.add_argument("--outfile", "-o", help="Write ciphertext to file instead of stdout")
    enc.add_argument("--show-matrix", action="store_true", help="Display generated key matrix")

    # decrypt subcommand
    dec = sub.add_parser("decrypt", help="Decrypt ciphertext")
    dec.add_argument("--key", "-k", required=True, help="Keyword for key matrix")
    dec.add_argument("--text", "-t", help="Ciphertext to decrypt (mutually exclusive with --infile)")
    dec.add_argument("--infile", "-i", help="Input file with ciphertext")
    dec.add_argument("--outfile", "-o", help="Write decrypted text to file instead of stdout")
    dec.add_argument("--show-matrix", action="store_true", help="Display generated key matrix")

    args = parser.parse_args()

    # decide input source
    if args.command == "encrypt":
        if args.text and args.infile:
            print("Error: use either --text or --infile, not both.", file=sys.stderr)
            sys.exit(1)
        if args.infile:
            with open(args.infile, "r", encoding="utf-8") as f:
                text = f.read()
        elif args.text:
            text = args.text
        else:
            print("Error: provide plaintext via --text or --infile.", file=sys.stderr)
            sys.exit(1)

        if args.show_matrix:
            print("Key matrix:")
            pretty_print_matrix(prepare_key(args.key))
            print()

        ciphertext = encrypt_text(args.key, text)
        if args.outfile:
            with open(args.outfile, "w", encoding="utf-8") as f:
                f.write(ciphertext)
            print(f"Ciphertext written to {args.outfile}")
        else:
            print("Ciphertext:")
            print(ciphertext)

    elif args.command == "decrypt":
        if args.text and args.infile:
            print("Error: use either --text or --infile, not both.", file=sys.stderr)
            sys.exit(1)
        if args.infile:
            with open(args.infile, "r", encoding="utf-8") as f:
                text = f.read()
        elif args.text:
            text = args.text
        else:
            print("Error: provide ciphertext via --text or --infile.", file=sys.stderr)
            sys.exit(1)

        if args.show_matrix:
            print("Key matrix:")
            pretty_print_matrix(prepare_key(args.key))
            print()

        plain_raw = decrypt_text(args.key, text)
        if args.outfile:
            with open(args.outfile, "w", encoding="utf-8") as f:
                f.write(plain_raw)
            print(f"Decrypted text written to {args.outfile}")
        else:
            print("Decrypted (raw, includes pads):")
            print(plain_raw)

if __name__ == "__main__":
    main()
