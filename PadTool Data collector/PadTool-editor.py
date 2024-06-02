import tkinter as tk
from tkinter import filedialog, messagebox
import requests
import time
import os
import json
from threading import Thread

class App:
    def __init__(self, root):
        self.root = root
        self.root.title('PadTool data collector')
        self.root.geometry('500x400')  # Fenêtre plus grande
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)

        # Variables
        self.json_url = tk.StringVar()
        self.dls_path = tk.StringVar()
        self.slide_path = tk.StringVar()
        self.running = False

        # Load settings
        self.load_settings()

        # URL Entry
        tk.Label(root, text="JSON URL:").pack()
        tk.Entry(root, textvariable=self.json_url, width=50).pack()

        # DLS Path Selector
        tk.Label(root, text="DLS File Path:").pack()
        tk.Entry(root, textvariable=self.dls_path, width=50).pack()
        tk.Button(root, text="Browse", command=self.browse_dls).pack()

        # Slide Path Selector
        tk.Label(root, text="Slide Folder Path:").pack()
        tk.Entry(root, textvariable=self.slide_path, width=50).pack()
        tk.Button(root, text="Browse", command=self.browse_slide).pack()

        # Control Buttons
        tk.Button(root, text="Start", command=self.start).pack()
        tk.Button(root, text="Stop", command=self.stop).pack()

    def browse_dls(self):
        directory = filedialog.askdirectory()
        if directory:
            self.dls_path.set(directory)

    def browse_slide(self):
        directory = filedialog.askdirectory()
        if directory:
            self.slide_path.set(directory)

    def fetch_and_save_data(self):
        while self.running:
            response = requests.get(self.json_url.get())
            if response.status_code == 200:
                data = response.json()
                if "artist" in data and "title" in data and "slide" in data:
                    artist_title = f"{data['artist']} - {data['title']}"
                    slide_url = data["slide"]

                    with open(os.path.join(self.dls_path.get(), "dls.dls"), 'w') as file:
                        file.write(artist_title)

                    image_path = os.path.join(self.slide_path.get(), "slide.jpg")
                    response = requests.get(slide_url)
                    if response.status_code == 200:
                        with open(image_path, 'wb') as file:
                            file.write(response.content)
            time.sleep(30)

    def start(self):
        if not self.json_url.get() or not self.dls_path.get() or not self.slide_path.get():
            messagebox.showwarning("Warning", "Please make sure all fields are filled out correctly.")
            return
        if not self.running:
            self.running = True
            self.thread = Thread(target=self.fetch_and_save_data)
            self.thread.start()

    def stop(self):
        self.running = False
        if self.thread.is_alive():
            self.thread.join()

    def save_settings(self):
        settings = {
            'json_url': self.json_url.get(),
            'dls_path': self.dls_path.get(),
            'slide_path': self.slide_path.get(),
        }
        with open('settings.json', 'w') as f:
            json.dump(settings, f)

    def load_settings(self):
        try:
            with open('settings.json', 'r') as f:
                settings = json.load(f)
                self.json_url.set(settings.get('json_url', ''))
                self.dls_path.set(settings.get('dls_path', ''))
                self.slide_path.set(settings.get('slide_path', ''))
        except FileNotFoundError:
            pass  # Le fichier n'existe pas encore, ignorer

    def on_closing(self):
        if self.running:
            self.stop()
        self.save_settings()
        self.root.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()
