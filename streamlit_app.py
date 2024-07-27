import streamlit as st
import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image
import piexif
import os

class ExifEditor:
    def __init__(self, root):
        self.root = root
        self.root.title("Exif Editor")
        self.fields = {}
        self.image_path = "maphoto.jpg"

        # Load image and EXIF data
        self.load_image_and_exif()

        # Create form
        self.create_form()

        # Save button
        save_button = tk.Button(root, text="Save", command=self.save_exif_data)
        save_button.pack()

    def load_image_and_exif(self):
        try:
            self.img = Image.open(self.image_path)
            self.exif_dict = piexif.load(self.img.info['exif'])
        except Exception as e:
            messagebox.showerror("Error", f"Error loading image: {e}")
            self.root.destroy()

    def create_form(self):
        for ifd in self.exif_dict:
            for tag, value in self.exif_dict[ifd].items():
                frame = tk.Frame(self.root)
                frame.pack(fill="x")
                
                label = tk.Label(frame, text=piexif.TAGS[ifd][tag]["name"], width=20, anchor="w")
                label.pack(side="left")
                
                entry = tk.Entry(frame)
                entry.insert(0, str(value))
                entry.pack(side="left", fill="x", expand=True)
                
                self.fields[(ifd, tag)] = entry

    def save_exif_data(self):
        try:
            for (ifd, tag), entry in self.fields.items():
                value = entry.get()
                try:
                    value = int(value)
                except ValueError:
                    pass
                self.exif_dict[ifd][tag] = value
            
            exif_bytes = piexif.dump(self.exif_dict)
            self.img.save("edited_" + os.path.basename(self.image_path), "jpeg", exif=exif_bytes)
            messagebox.showinfo("Success", "EXIF data saved successfully!")
        except Exception as e:
            messagebox.showerror("Error", f"Error saving EXIF data: {e}")

if __name__ == "__main__":
    root = tk.Tk()
    app = ExifEditor(root)
    root.mainloop()
