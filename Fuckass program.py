



# WELCOME TO THE CODE!!!! Please do not change anything if you dont know how this works, credits to myself for making this AND CHATGPT for helping me by some minor issues
# HAVE FUN!
# GO CRAZY!




import tkinter as tk
from tkinter import filedialog, messagebox
from tkinter import ttk
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import imageio
import numpy as np
import threading
import os

class GoodnightMakerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Goodnight GIF Maker")

        self.input_path = tk.StringVar()
        self.output_path = tk.StringVar()
        self.custom_text = tk.StringVar(value="goodnight 💫")
        self.font_path = tk.StringVar()
        self.effects = {
            "Glow": tk.BooleanVar(value=True),
            "Sparkles": tk.BooleanVar(value=True),
            "Hearts": tk.BooleanVar(value=True),
        }

        self.create_widgets()

    def create_widgets(self):
        frame = ttk.Frame(self.root, padding=10)
        frame.pack(fill=tk.BOTH, expand=True)

        ttk.Label(frame, text="Select Image:").grid(row=0, column=0, sticky=tk.W)
        ttk.Entry(frame, textvariable=self.input_path, width=40).grid(row=0, column=1, sticky=tk.W)
        ttk.Button(frame, text="Browse...", command=self.browse_input).grid(row=0, column=2)

        ttk.Label(frame, text="Save As (GIF):").grid(row=1, column=0, sticky=tk.W)
        ttk.Entry(frame, textvariable=self.output_path, width=40).grid(row=1, column=1, sticky=tk.W)
        ttk.Button(frame, text="Browse...", command=self.browse_output).grid(row=1, column=2)

        ttk.Label(frame, text="Text:").grid(row=2, column=0, sticky=tk.W)
        ttk.Entry(frame, textvariable=self.custom_text, width=40).grid(row=2, column=1, sticky=tk.W, columnspan=2)

        ttk.Label(frame, text="Font (TTF):").grid(row=3, column=0, sticky=tk.W)
        ttk.Entry(frame, textvariable=self.font_path, width=40).grid(row=3, column=1, sticky=tk.W)
        ttk.Button(frame, text="Browse...", command=self.browse_font).grid(row=3, column=2)

        ttk.Label(frame, text="Effects:").grid(row=4, column=0, sticky=tk.NW)
        effects_frame = ttk.Frame(frame)
        effects_frame.grid(row=4, column=1, sticky=tk.W)
        for i, (eff, var) in enumerate(self.effects.items()):
            ttk.Checkbutton(effects_frame, text=eff, variable=var).grid(row=i, column=0, sticky=tk.W)

        self.progress = ttk.Progressbar(frame, length=300, mode='determinate')
        self.progress.grid(row=5, column=0, columnspan=3, pady=10)

        self.generate_button = ttk.Button(frame, text="Generate GIF", command=self.start_generation)
        self.generate_button.grid(row=6, column=0, columnspan=3, pady=5)

    def browse_input(self):
        path = filedialog.askopenfilename(filetypes=[("PNG/JPEG images", "*.png;*.jpg;*.jpeg;*.bmp")])
        if path:
            self.input_path.set(path)

    def browse_output(self):
        path = filedialog.asksaveasfilename(defaultextension=".gif", filetypes=[("GIF files", "*.gif")])
        if path:
            self.output_path.set(path)

    def browse_font(self):
        path = filedialog.askopenfilename(filetypes=[("Font files", "*.ttf;*.otf")])
        if path:
            self.font_path.set(path)

    def start_generation(self):
        if not os.path.isfile(self.input_path.get()):
            messagebox.showerror("Error", "Please select a valid input image file.")
            return
        if not self.output_path.get():
            messagebox.showerror("Error", "Please select a save path for the output GIF.")
            return

        self.generate_button.config(state=tk.DISABLED)
        self.progress['value'] = 0
        threading.Thread(target=self.generate_gif).start()

    def generate_gif(self):
        try:
            self._generate_gif()
            messagebox.showinfo("Success", f"GIF saved to:\n{self.output_path.get()}")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred:\n{e}")
        finally:
            self.generate_button.config(state=tk.NORMAL)
            self.progress['value'] = 0

    def _generate_gif(self):
        cat_img = Image.open(self.input_path.get()).convert("RGBA")

        canvas_size = (512, 512)
        canvas = Image.new("RGBA", canvas_size, (10, 10, 30, 255))

        cat_img = cat_img.resize((300, 300))
        cat_position = ((canvas_size[0] - cat_img.size[0]) // 2, 100)

        if self.font_path.get() and os.path.isfile(self.font_path.get()):
            font = ImageFont.truetype(self.font_path.get(), 42)
        else:
            font = ImageFont.load_default()

        def add_glow(base_img, img, pos, glow_radius=15, glow_color=(100, 100, 255, 180)):
            glow = Image.new("RGBA", base_img.size, (0,0,0,0))
            glow.paste(img, pos, img)
            glow = glow.filter(ImageFilter.GaussianBlur(radius=glow_radius))
            glow_layer = Image.new("RGBA", base_img.size, glow_color)
            glow = Image.alpha_composite(glow_layer, glow)
            return Image.alpha_composite(base_img, glow)

        def draw_star(draw, x, y, size=5, color=(255, 255, 255, 180)): # you can change the color of the stars :3
            draw.line((x - size, y, x + size, y), fill=color, width=1)
            draw.line((x, y - size, x, y + size), fill=color, width=1)
            draw.line((x - size, y - size, x + size, y + size), fill=color, width=1)
            draw.line((x - size, y + size, x + size, y - size), fill=color, width=1)

        def add_sparkles(image, sparkle_intensity):
            sparkle_layer = Image.new("RGBA", image.size, (0, 0, 0, 0))
            sparkle_draw = ImageDraw.Draw(sparkle_layer)
            for _ in range(sparkle_intensity):
                x = np.random.randint(0, image.size[0])
                y = np.random.randint(0, image.size[1])
                size = np.random.randint(2, 6)
                draw_star(sparkle_draw, x, y, size)
            return Image.alpha_composite(image, sparkle_layer)

        def add_floating_hearts(image, heart_intensity):
            heart_layer = Image.new("RGBA", image.size, (0,0,0,0))
            heart_draw = ImageDraw.Draw(heart_layer)
            for _ in range(heart_intensity):
                x = np.random.randint(0, image.size[0])
                y = np.random.randint(0, image.size[1])
                size = np.random.randint(8, 15)
                heart_draw.ellipse((x, y, x + size//2, y + size//2), fill=(255, 0, 100, 180))
                heart_draw.ellipse((x + size//2, y, x + size, y + size//2), fill=(255, 0, 100, 180))
                heart_draw.polygon([(x, y + size//4), (x + size, y + size//4), (x + size//2, y + size)], fill=(255, 0, 100, 180))
            return Image.alpha_composite(image, heart_layer)

        frames = []
        total_frames = 8

        for i in range(total_frames):
            self.progress['value'] = (i / total_frames) * 100
            self.root.update_idletasks()

            frame = canvas.copy()

            if self.effects["Glow"].get():
                frame = add_glow(frame, cat_img, cat_position)

            frame.paste(cat_img, cat_position, cat_img)

            if self.effects["Sparkles"].get():
                frame = add_sparkles(frame, sparkle_intensity=40)

            if self.effects["Hearts"].get():
                frame = add_floating_hearts(frame, heart_intensity=10)

            draw = ImageDraw.Draw(frame)
            text = self.custom_text.get()
            bbox = draw.textbbox((0, 0), text, font=font)
            w = bbox[2] - bbox[0]
            h = bbox[3] - bbox[1]
            draw.text(((canvas_size[0] - w) // 2, 20), text, font=font, fill=(200, 200, 255, 255))

            frames.append(frame)

        frames[0].save(self.output_path.get(), save_all=True, append_images=frames[1:], optimize=False, duration=200, loop=0)
        self.progress['value'] = 100
        self.root.update_idletasks()

def main():
    root = tk.Tk()
    app = GoodnightMakerApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
