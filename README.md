Playfair Cipher Encryption & Decryption Tool

This project is a Python-based implementation of the Playfair Cipher, a classical cryptographic algorithm used to encrypt and decrypt text using a 5×5 key matrix. It includes both a GUI application (Tkinter) and command-line scripts.

Features:
Encrypts plaintext using Playfair Cipher rules

Decrypts ciphertext back to plaintext

Supports automatic text formatting

GUI for easy usage

Handles repeated letters and odd-length inputs

Removes special characters and spaces

How It Works

The Playfair Cipher encrypts text two letters at a time (digraphs). A key word is used to generate a 5×5 matrix of letters. Based on the positions of letter pairs in this matrix, substitutions are made using three rules:

Same Row: Replace each letter with the letter to its right

Same Column: Replace each letter with the one below it

Different Row & Column: Swap to form rectangle corners

This tool automates the full process for both encryption and decryption.

Technologies Used:

Python 3

Tkinter GUI

File handling & text processing


