import tkinter as tk
from tkinter import filedialog, messagebox
from tkinter import ttk
from PIL import Image, ImageEnhance, ImageFont, ImageDraw
import matplotlib.font_manager as fm


def get_text_size(text, font_obj):
    # Create a dummy image to draw the text
    dummy_image = Image.new("RGB", (0, 0))
    draw = ImageDraw.Draw(dummy_image)

    # Calculate the size of the text
    _, _, width, height = draw.textbbox((0, 0), text=text, font=font_obj)
    return width, height


class WatermarkApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Watermark App")

        self.font_var = tk.StringVar(value="Arial")
        self.font_size_var = tk.IntVar(value=36)
        self.opacity_var = tk.StringVar(value="50")
        # self.watermark_ratio = tk.StringVar(value="100")

        # Get all fonts installed on the system
        self.fonts = fm.findSystemFonts(fontpaths="C:/Windows/Fonts", fontext='ttf')
        self.font_map = {fm.FontProperties(fname=f).get_name(): f for f in self.fonts}
        self.font_names = sorted(self.font_map.keys())
        # self.fonts = ["Arial", "Courier", "Helvetica", "Times New Roman", "Verdana"]

        outer_padding = 30  # Define outer padding value
        font_style = ("Helvetica", 10)  # Example font for text displayed on the application

        # Create a frame to hold all widgets
        main_frame = tk.Frame(root)
        main_frame.grid(row=0, column=0, padx=outer_padding, pady=outer_padding)

        # Upload Image Button
        self.upload_image_btn = tk.Button(main_frame, text="Upload Image", command=self.upload_image)
        self.upload_image_btn.grid(row=0, column=1, padx=10, pady=10, columnspan=5, sticky="W")

        # Image Path Label
        self.image_path_label = tk.Label(main_frame, width=25, text="No Image Selected", anchor="w")
        self.image_path_label.grid(row=0, column=0, padx=10, pady=10)

        # Upload Watermark Button
        self.upload_watermark_btn = tk.Button(main_frame, text="Upload Watermark", command=self.upload_watermark)
        self.upload_watermark_btn.grid(row=1, column=1, padx=10, pady=10, columnspan=10, sticky="W")

        # Watermark Path Label
        self.watermark_path_label = tk.Label(main_frame, width=25, text="No Watermark Image Selected", anchor="w")
        self.watermark_path_label.grid(row=1, column=0, padx=10, pady=10)

        self.watermark_ratio_label = tk.Label(main_frame, text="Watermark Resize Ratio (%)")
        self.watermark_ratio_label.grid(row=2, column=0, padx=10, pady=10, sticky="W")

        self.watermark_ratio = tk.Text(main_frame, width=5, height=1, font=font_style)
        self.watermark_ratio.grid(row=2, column=1, columnspan=2, padx=10, pady=10, sticky="W")

        self.watermark_ratio_100 = tk.Label(main_frame, width=3, text="/100", anchor="w")
        self.watermark_ratio_100.grid(row=2, column=2)

        self.or_label = tk.Label(main_frame, text="Or", width=3, anchor="center")
        self.or_label.grid(row=3, column=0, columnspan=11)

        # Watermark text label
        self.watermark_text_label = tk.Label(main_frame, width=25, text="Enter Watermark Text", anchor="w")
        self.watermark_text_label.grid(row=4, column=0, padx=10, pady=10, sticky="W")

        self.watermark_text = tk.Text(main_frame, width=15, height=1, font=font_style)
        self.watermark_text.grid(row=4, column=1, padx=10, pady=10, columnspan=10, sticky="W")

        #### Font start ####
        self.font_label = tk.Label(main_frame, width=25, text="Font / Size", anchor="w")
        self.font_label.grid(row=5, column=0, padx=10, pady=10, sticky="W")

        self.font_combobox = ttk.Combobox(main_frame, textvariable=self.font_var, values=self.font_names, width=25)
        self.font_combobox.grid(row=5, column=1, padx=10, pady=10, columnspan=10, sticky="W")
        # self.font_combobox.set("Arial")  # default font

        self.font_size_spinbox = tk.Spinbox(main_frame, from_=10, to=100, width=3, textvariable=self.font_size_var)
        self.font_size_spinbox.grid(row=5, column=11, padx=10, pady=10, sticky="W")
        #### font end ####

        # Select Position Dropdown
        self.position_label = tk.Label(main_frame, text="Select Position")
        self.position_label.grid(row=6, column=0, padx=10, pady=10, sticky="W")

        self.position_var = tk.StringVar(value="top-left")
        self.position_dropdown = ttk.Combobox(main_frame, textvariable=self.position_var,
                                              values=["top-left", "top-right", "bottom-left", "bottom-right", "middle"])
        self.position_dropdown.grid(row=6, column=1, padx=10, pady=10, columnspan=10, sticky="W")

        # Select Opacity
        self.position_label = tk.Label(main_frame, text="Select Transparency (%)")
        self.position_label.grid(row=7, column=0, padx=10, pady=10, sticky="W")

        opacity_vals = [str(i) for i in range(10, 101, 10)]
        self.opacity_dropdown = ttk.Combobox(main_frame, width=3, textvariable=self.opacity_var, values=opacity_vals)
        self.opacity_dropdown.grid(row=7, column=1, padx=10, pady=10, sticky="W")

        self.opacity_label = tk.Label(main_frame, width=3, text="/100", anchor="w")
        self.opacity_label.grid(row=7, column=2)

        # Add Watermark Button
        self.add_watermark_btn = tk.Button(main_frame, text="Add Watermark", command=self.add_watermark)
        self.add_watermark_btn.grid(row=8, column=2, columnspan=10, padx=10, pady=10, sticky="w")

        self.clear_btn = tk.Button(main_frame, text="Clear", command=self.clear_all_inputs, anchor="center")
        self.clear_btn.grid(row=8, column=0, padx=10, pady=10, sticky="e")

        self.image_path = None
        self.watermark_path = None

    def clear_all_inputs(self):
        # Clear entry widgets
        self.watermark_text.delete('1.0', tk.END)
        self.watermark_path_label.config(text="No Watermark Selected")
        self.image_path_label.config(text="No Image Selected")
        self.font_size_var.set(36)
        self.opacity_var.set("10")
        self.watermark_ratio.delete('1.0', tk.END)
        self.watermark_path = None
        self.image_path = None

    def select_font(self):
        font_path = filedialog.askopenfilename(filetypes=[("Font files", "*.ttf *.otf")])
        if font_path:
            self.font_var.set(font_path)

    def upload_image(self):
        self.image_path = filedialog.askopenfilename(filetypes=[("Image Files", "*.png;*.jpg;*.jpeg")])
        self.image_path_label.config(text=self.image_path if self.image_path else "No Image Selected")

    def upload_watermark(self):
        self.watermark_path = filedialog.askopenfilename(filetypes=[("Image Files", "*.png;*.jpg;*.jpeg")])
        self.watermark_path_label.config(text=self.watermark_path if self.watermark_path else "No Watermark Selected")

    def add_watermark(self):

        # self.image_path = "C:/Users/USER/Downloads/4928889775_41587b7b1e_o.jpg"
        # self.watermark_path = "C:/Users/USER/Downloads/Untitled-3 (5).png"

        if not self.image_path:
            tk.messagebox.showerror("Error", f"Select Image")
            return

        wm_text = self.watermark_text.get("1.0", 'end-1c')
        if wm_text == "" and not self.watermark_path:
            tk.messagebox.showerror("Error", f"Select Watermark Image or Enter Watermark Text")
            return

        save_path = filedialog.asksaveasfilename(defaultextension=".png", initialfile="watermarked_image.png",
                                                 filetypes=[("PNG files", "*.png"), ("All files", "*.*")])
        if save_path:
            opacity = int(self.opacity_var.get()) / 100

            original = Image.open(self.image_path).convert("RGBA")
            width, height = original.size

            if self.watermark_path:

                watermark = Image.open(self.watermark_path).convert("RGBA")
                wm_original_width, wm_original_height = watermark.size

                wm_ratio_val = self.watermark_ratio.get("1.0", 'end-1c')
                wm_ratio = int(wm_ratio_val) if wm_ratio_val != "" else 100

                wm_height = int(wm_original_height * (wm_ratio / 100))
                wm_width = int(wm_original_width * (wm_ratio / 100))

                watermark = watermark.resize((wm_width, wm_height), Image.LANCZOS)
                position = self.get_position(height, width, wm_height, wm_width)

                # reduce opacity
                alpha = watermark.split()[3]
                alpha = ImageEnhance.Brightness(alpha).enhance(opacity)
                watermark.putalpha(alpha)

                watermarked = Image.new("RGBA", (width, height), (0, 0, 0, 0))
                watermarked.paste(original, (0, 0))
                watermarked.paste(watermark, position, mask=watermark)

            else:
                watermark_text_img = Image.new("RGBA", (width, height), (255, 255, 255, 0))

                selected_font_name = self.font_var.get()
                font_path = self.font_map.get(selected_font_name)

                font = ImageFont.truetype(font_path, self.font_size_var.get())

                wm_width, wm_height = get_text_size(wm_text, font)
                position = self.get_position(height, width, wm_height, wm_width)

                watermark_draw_img = ImageDraw.Draw(watermark_text_img)
                # position = (10, 10)
                watermark_draw_img.text(position, self.watermark_text.get("1.0", 'end-1c'),
                                        fill=(255, 255, 255, int(255 * opacity)), font=font)
                watermarked = Image.alpha_composite(original, watermark_text_img)

            # watermarked.show()
            watermarked.save(save_path)
            tk.messagebox.showinfo("Image Saved", f"Image successfully saved to {save_path}")

    def get_position(self, height, width, wm_height, wm_width):
        global position
        pos = self.position_var.get()
        if pos == "top-left":
            position = (10, 10)
        elif pos == "top-right":
            position = (width - wm_width - 10, 10)
        elif pos == "bottom-left":
            position = (10, height - wm_height - 10)
        elif pos == "bottom-right":
            position = (width - wm_width - 10, height - wm_height - 10)
        elif pos == "middle":
            position = (int(width / 2 - wm_width / 2), int(height / 2 - wm_height / 2))

        return position
