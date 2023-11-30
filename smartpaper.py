import os
import tkinter as tk
from tkinter import ttk
from tkinter.messagebox import showinfo

from smartpaper import *

library_dir = "..\outbox\My Device\Library"
output_dir = "..\inbox"
version = "0.0.1"


def run_conversion():
    status["text"] = "working..."
    src_dir = os.path.join(library_dir, selected_dir.get())
    pdf_name = os.path.split(get_pdf_path(src_dir))[-1]
    output_pdf = os.path.join(output_dir, pdf_name)
    create_pdf(src_dir, output_pdf)
    status["text"] = "done"


root = tk.Tk()
root.geometry("300x130")
root.resizable(False, False)
root.title(f"SmartPaper PDF {version}")

label = ttk.Label(text="Library book:")
label.pack(fill=tk.X, padx=5, pady=5)

selected_dir = tk.StringVar()
folder_cb = ttk.Combobox(root, textvariable=selected_dir)
dirs = []
for f in os.listdir(library_dir):
    if os.path.isdir(os.path.join(library_dir, f)):
        dirs.append(f)
folder_cb["values"] = dirs
folder_cb["state"] = "readonly"
folder_cb.current(0)
folder_cb.pack(fill=tk.X, padx=5, pady=5)

convert_bt = ttk.Button(root, text="Merge and Replace", command=run_conversion)
convert_bt.pack(fill=tk.X, padx=5, pady=5)

status = ttk.Label(text="")
status.pack(fill=tk.X, padx=5, pady=5)

root.mainloop()
