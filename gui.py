# gui.py - simple Tkinter GUI for Playfair cipher
import tkinter as tk
from tkinter import ttk, scrolledtext, filedialog, messagebox
from playfair import prepare_key, encrypt_text, decrypt_text, pretty_print_matrix

def matrix_to_string(matrix):
    lines = []
    for row in matrix:
        lines.append(' '.join(row))
    return '\n'.join(lines)

class PlayfairGUI(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Playfair Cipher GUI")
        self.geometry("820x640")
        self.create_widgets()

    def create_widgets(self):
        frm = ttk.Frame(self, padding=10)
        frm.pack(fill='both', expand=True)

        # Key and controls
        ttk.Label(frm, text="Key (keyword):").grid(row=0, column=0, sticky='w')
        self.key_var = tk.StringVar(value="PLAYFAIR EXAMPLE")
        ttk.Entry(frm, textvariable=self.key_var, width=40).grid(row=0, column=1, sticky='w')

        ttk.Button(frm, text="Show Matrix", command=self.show_matrix).grid(row=0, column=2, padx=6)

        # Input and output
        ttk.Label(frm, text="Plain / Cipher text:").grid(row=1, column=0, sticky='w')
        self.text_input = tk.Text(frm, height=6, width=80)
        self.text_input.grid(row=2, column=0, columnspan=3, pady=6)

        btn_frame = ttk.Frame(frm)
        btn_frame.grid(row=3, column=0, columnspan=3, pady=6, sticky='w')
        ttk.Button(btn_frame, text="Encrypt", command=self.on_encrypt).grid(row=0, column=0, padx=4)
        ttk.Button(btn_frame, text="Decrypt", command=self.on_decrypt).grid(row=0, column=1, padx=4)
        ttk.Button(btn_frame, text="Clear", command=self.on_clear).grid(row=0, column=2, padx=4)
        ttk.Button(btn_frame, text="Save Trace", command=self.save_trace).grid(row=0, column=3, padx=4)

        # Matrix display
        ttk.Label(frm, text="Key Matrix:").grid(row=4, column=0, sticky='w')
        self.matrix_box = scrolledtext.ScrolledText(frm, height=6, width=30, state='disabled')
        self.matrix_box.grid(row=5, column=0, pady=6, sticky='nw')

        # Trace display
        ttk.Label(frm, text="Trace / Output:").grid(row=4, column=1, sticky='w')
        self.trace_box = scrolledtext.ScrolledText(frm, height=16, width=60)
        self.trace_box.grid(row=5, column=1, columnspan=2, pady=6, sticky='nsew')

        # Clean option for decrypt
        self.clean_var = tk.BooleanVar(value=True)
        ttk.Checkbutton(frm, text="Apply heuristic clean on decrypt (demo)", variable=self.clean_var).grid(row=6, column=1, sticky='w')

    def show_matrix(self):
        key = self.key_var.get()
        try:
            mat = prepare_key(key)
        except Exception as e:
            messagebox.showerror("Error", f"Key error: {e}")
            return
        txt = matrix_to_string(mat)
        self.matrix_box.configure(state='normal')
        self.matrix_box.delete('1.0', tk.END)
        self.matrix_box.insert(tk.END, txt)
        self.matrix_box.configure(state='disabled')

    def on_encrypt(self):
        key = self.key_var.get()
        text = self.text_input.get('1.0', tk.END).strip()
        if not text:
            messagebox.showinfo("Info", "Enter plaintext in the text area.")
            return
        ct, trace_lines = encrypt_text(key, text, trace=True)
        # Display
        self.trace_box.delete('1.0', tk.END)
        for line in trace_lines:
            self.trace_box.insert(tk.END, line + '\n')
        self.trace_box.insert(tk.END, '\nCiphertext (single-line):\n' + ct)
        self.show_matrix()

    def on_decrypt(self):
        key = self.key_var.get()
        text = self.text_input.get('1.0', tk.END).strip()
        if not text:
            messagebox.showinfo("Info", "Enter ciphertext in the text area.")
            return
        pt, trace_lines = decrypt_text(key, text, trace=True)
        self.trace_box.delete('1.0', tk.END)
        for line in trace_lines:
            self.trace_box.insert(tk.END, line + '\n')
        self.trace_box.insert(tk.END, '\nDecrypted (raw):\n' + pt + '\n')
        if self.clean_var.get():
            cleaned = self.heuristic_clean(pt)
            self.trace_box.insert(tk.END, '\nHeuristic cleaned (demo):\n' + cleaned + '\n')
        self.show_matrix()

    def heuristic_clean(self, text: str) -> str:
        if text.endswith('X'):
            text = text[:-1]
        out_chars = []
        i = 0
        n = len(text)
        while i < n:
            if i + 2 < n and text[i+1] == 'X' and text[i] == text[i+2]:
                out_chars.append(text[i])
                i += 3
            else:
                out_chars.append(text[i])
                i += 1
        return ''.join(out_chars)

    def save_trace(self):
        text = self.trace_box.get('1.0', tk.END).strip()
        if not text:
            messagebox.showinfo("Info", "No trace to save.")
            return
        path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text files","*.txt"),("All files","*.*")])
        if not path:
            return
        try:
            with open(path, "w", encoding="utf-8") as f:
                f.write(text)
            messagebox.showinfo("Saved", f"Trace saved to {path}")
        except Exception as e:
            messagebox.showerror("Error", f"Could not save file: {e}")

    def on_clear(self):
        self.text_input.delete('1.0', tk.END)
        self.trace_box.delete('1.0', tk.END)
        self.matrix_box.configure(state='normal'); self.matrix_box.delete('1.0', tk.END); self.matrix_box.configure(state='disabled')

if __name__ == "__main__":
    app = PlayfairGUI()
    app.mainloop()
