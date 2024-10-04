import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk
import numpy as np
import os

# Utility functions for image manipulation
def load_image(image_path):
    return Image.open(image_path)

def save_image(image, output_path):
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    image.save(output_path)

def encrypt_image(image, key):
    pixels = np.array(image, dtype=np.int32)
    encrypted_pixels = (pixels + key) % 256
    return Image.fromarray(encrypted_pixels.astype(np.uint8))

def decrypt_image(image, key):
    pixels = np.array(image, dtype=np.int32)
    decrypted_pixels = (pixels - key) % 256
    return Image.fromarray(decrypted_pixels.astype(np.uint8))

def swap_pixels(image, key):
    np.random.seed(key)
    pixels = np.array(image)
    idx = np.arange(pixels.size)
    np.random.shuffle(idx)
    swapped_pixels = pixels.flatten()[idx].reshape(pixels.shape)
    return Image.fromarray(swapped_pixels.astype(np.uint8))

def reverse_swap(image, key):
    np.random.seed(key)
    pixels = np.array(image)
    idx = np.arange(pixels.size)
    np.random.shuffle(idx)
    reverse_idx = np.argsort(idx)
    reversed_pixels = pixels.flatten()[reverse_idx].reshape(pixels.shape)
    return Image.fromarray(reversed_pixels.astype(np.uint8))

# GUI Application
class ImageEncryptionApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Image Encryption & Decryption")
        self.root.geometry("500x500")

        self.image_path = None
        self.image = None
        self.encryption_key = tk.IntVar(value=42)

        # UI Elements
        self.create_widgets()

    def create_widgets(self):
        # Label for Key
        tk.Label(self.root, text="Enter Encryption Key:").pack(pady=10)
        
        # Entry for key input
        self.key_entry = tk.Entry(self.root, textvariable=self.encryption_key)
        self.key_entry.pack()

        # Load Image Button
        tk.Button(self.root, text="Load Image", command=self.load_image).pack(pady=10)
        
        # Buttons for Encryption and Decryption
        tk.Button(self.root, text="Encrypt Image", command=self.encrypt_image).pack(pady=5)
        tk.Button(self.root, text="Decrypt Image", command=self.decrypt_image).pack(pady=5)
        
        # Buttons for Pixel Swapping
        tk.Button(self.root, text="Swap Pixels", command=self.swap_pixels).pack(pady=5)
        tk.Button(self.root, text="Reverse Swap Pixels", command=self.reverse_swap).pack(pady=5)

        # Image display area
        self.image_label = tk.Label(self.root)
        self.image_label.pack(pady=10)

    def load_image(self):
        # File dialog to choose an image
        file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.png;*.jpg;*.jpeg;*.bmp")])
        if file_path:
            self.image_path = file_path
            self.image = load_image(file_path)
            self.display_image(self.image)

    def save_and_notify(self, img, action):
        output_dir = os.path.dirname(self.image_path)
        output_path = os.path.join(output_dir, f"{action}_image.png")
        save_image(img, output_path)
        messagebox.showinfo("Success", f"Image {action} and saved as '{output_path}'")

    def encrypt_image(self):
        if self.image:
            key = self.encryption_key.get()
            encrypted_img = encrypt_image(self.image, key)
            self.display_image(encrypted_img)
            self.save_and_notify(encrypted_img, 'encrypted')

    def decrypt_image(self):
        if self.image:
            key = self.encryption_key.get()
            decrypted_img = decrypt_image(self.image, key)
            self.display_image(decrypted_img)
            self.save_and_notify(decrypted_img, 'decrypted')

    def swap_pixels(self):
        if self.image:
            key = self.encryption_key.get()
            swapped_img = swap_pixels(self.image, key)
            self.display_image(swapped_img)
            self.save_and_notify(swapped_img, 'swapped')

    def reverse_swap(self):
        if self.image:
            key = self.encryption_key.get()
            unswapped_img = reverse_swap(self.image, key)
            self.display_image(unswapped_img)
            self.save_and_notify(unswapped_img, 'unswapped')

    def display_image(self, img):
        img.thumbnail((300, 300))
        img_tk = ImageTk.PhotoImage(img)
        self.image_label.config(image=img_tk)
        self.image_label.image = img_tk

# Run the application
if __name__ == "__main__":
    root = tk.Tk()
    app = ImageEncryptionApp(root)
    root.mainloop()
