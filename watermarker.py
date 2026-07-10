# ===================== IMPORTS =====================
import os
import tkinter as tk
from tkinter import filedialog, messagebox
import customtkinter as ctk
from PIL import Image

# ===================== LOGIC =====================
input_folder = ""
watermark_path = ""

def apply_watermark(input_folder, output_folder, watermark_path, width_percent, margin):
    watermark = Image.open(watermark_path).convert("RGBA")
    os.makedirs(output_folder, exist_ok=True)

    processed = 0
    for filename in os.listdir(input_folder):
        if not filename.lower().endswith((".png", ".jpg", ".jpeg")):
            continue

        image_path = os.path.join(input_folder, filename)
        image = Image.open(image_path).convert("RGBA")

        target_width = int(image.width * width_percent)
        scale = target_width / watermark.width
        target_height = int(watermark.height * scale)
        resized_watermark = watermark.resize((target_width, target_height))

        x = image.width - target_width - margin
        y = image.height - target_height - margin

        image.paste(resized_watermark, (x, y), resized_watermark)

        save_path = os.path.join(output_folder, filename)
        if filename.lower().endswith((".jpg", ".jpeg")):
            image.convert("RGB").save(save_path, quality=95)
        else:
            image.save(save_path)
        processed += 1

    return processed

# ===================== GUI CALLBACKS =====================
def get_input_folder():
    global input_folder
    input_folder = filedialog.askdirectory()
    parts = input_folder.split("/")
    display_path = "..." + "/".join(parts[-3:]) if len(parts) > 3 else input_folder
    label_input_path.configure(text=display_path)

def get_watermark_file():
    global watermark_path
    watermark_path = filedialog.askopenfilename(filetypes=[("PNG files", "*.png")])
    parts = watermark_path.split("/")
    display_path = "..." + "/".join(parts[-2:]) if len(parts) > 2 else watermark_path
    label_watermark_path.configure(text=display_path)

def run():
    if not input_folder or not watermark_path:
        messagebox.showerror("Error", "Choose both an input folder and a watermark file")
        return

    output_folder = os.path.join(input_folder, "watermarked")

    try:
        width_percent = float(entry_width_percent.get()) / 100
        margin = int(entry_margin.get())
        count = apply_watermark(input_folder, output_folder, watermark_path, width_percent, margin)
        messagebox.showinfo("Success", f"Processed {count} images.\nSaved to: {output_folder}")
    except Exception as e:
        messagebox.showerror("Error", str(e))

# ===================== GUI SETUP =====================
window = ctk.CTk()
window.title("Watermark Tool")
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("dark-blue")

# ===================== GUI WIDGETS =====================
label_input_path = ctk.CTkLabel(window, text="No input folder selected", width=10, anchor="w")
label_input_path.grid(row=0, column=0, columnspan=2, padx=5, pady=5, sticky="we")

button_input = ctk.CTkButton(window, text="Choose input folder", command=get_input_folder, width=200)
button_input.grid(row=0, column=2, padx=10, pady=5)

label_watermark_path = ctk.CTkLabel(window, text="No watermark selected", width=10, anchor="w")
label_watermark_path.grid(row=1, column=0, columnspan=2, padx=5, pady=5, sticky="we")

button_watermark = ctk.CTkButton(window, text="Choose watermark PNG", command=get_watermark_file, width=200)
button_watermark.grid(row=1, column=2, padx=10, pady=5)

label_width_percent = ctk.CTkLabel(window, text="Watermark width (% of image):")
label_width_percent.grid(row=2, column=0, sticky="w", padx=5)

entry_width_percent = ctk.CTkEntry(window, width=100)
entry_width_percent.insert(0, "60")
entry_width_percent.grid(row=2, column=1, padx=5, sticky="w")

label_margin = ctk.CTkLabel(window, text="Margin (px):")
label_margin.grid(row=3, column=0, sticky="w", padx=5)

entry_margin = ctk.CTkEntry(window, width=100)
entry_margin.insert(0, "0")
entry_margin.grid(row=3, column=1, padx=5, sticky="w")

button_run = ctk.CTkButton(window, text="Run", command=run, width=100)
button_run.grid(row=4, column=2, sticky="e", padx=5, pady=10)

window.mainloop()