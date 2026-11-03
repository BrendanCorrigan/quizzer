import os
import tkinter as tk
from PIL import Image, ImageTk, ImageOps

# ---------------------------------------------------------------------------------------------------------------
#    
# ---------------------------------------------------------------------------------------------------------------
class ImagePanel(tk.Frame):
    '''
    A simple Tkinter Frame that displays an image.
    '''
    def __init__(self, parent, image_path: str, size=(256, 256), background: str ="white"):
        super().__init__(parent, bg=background)
        
        self.configure(background=background)
        self.image_cache = {}
        self.background = background
        self.size = size
        self.label = tk.Label(self, bg=self.background)
        self.label.pack()

        if image_path:
            self.update_image_path(image_path)
        # else:
        #     self.update_image(image)

    def update_image(self, image):
        '''
        Resize - maintain aspect ratio
        '''
        self.image = image.resize(self.size)
        self.image = ImageOps.contain(image, self.size)
        self.image_width, self.image_height = self.image.size

        self.photo = ImageTk.PhotoImage(self.image)
        self.label["image"] = self.photo
        
        self.label.pack()

    def update_image_path(self, image_path):
        '''
        Update the image displayed in the panel.
        '''
        image = self.__load_image(image_path)
        self.photo = ImageTk.PhotoImage(image)
        self.label["image"] = self.photo
        
        self.label.pack()

    def __load_image(self, image_path: str):
        '''
        Load and resize the image from the given path.
        '''
        if image_path in self.image_cache:
            return self.image_cache[image_path]
        
        if not os.path.exists(image_path):
            raise FileNotFoundError(f"Image file not found: {image_path}")
        
        image = Image.open(image_path).resize(self.size)  # Resize the new image
        self.image_cache[image_path] = image
        return image
    
# -----------------------------------------------------------------------
#    
# -----------------------------------------------------------------------
# class FooterPanel(tk.Frame):
#     '''
#     A simple Tkinter Frame that displays an image.
#     '''
#     def __init__(self, parent, text: str = "", background="white", foreground="black", font=("Arial", 10), footer_image_path: str = ""):
#         super().__init__(parent, bg=background)

#         self.configure(bg=background)
#         self.footer_image = None
        
#         self._original = Image.open(image_path)
#         self._photo = None          # keep a reference or Tk will garbage-collect it
#         self._last_width = 0
#         self._after_id = None
#         parent.bind("<Configure>", self._on_parent_configure, add="+")
                
#         # self.image_cache = {}
#         # self.background = background

#         if footer_image_path and not footer_image_path == "":
#             if os.path.exists(footer_image_path):
#                 if self.footer_image is None:
#                     self.footer_image = tk.PhotoImage(file=footer_image_path)
#             else:
#                 raise ValueError(f"Footer image file: '{footer_image_path}' not found")
#             self.footer_image_label = tk.Label(self, image=self.footer_image, background=background, border=0)
#             self.footer_image_label.pack(anchor="w", expand=True, fill="x")

#         else:
#             self.label = tk.Label(self, text=text, bg=background, fg=foreground, font=font)
#             self.label.pack()
    
#     def _on_parent_configure(self, event):
#         # Only react to the parent itself, and only if the width changed.
#         # (Ignoring height avoids a resize feedback loop, since changing the
#         # footer height changes the layout and fires another <Configure>.)
#         if event.widget is not self.master or event.width == self._last_width:
#             return
#         self._last_width = event.width
#         if self._after_id:
#             self.after_cancel(self._after_id)
#         self._after_id = self.after(30, self._resize, event.width)  # debounce

#     def _resize(self, width):
#         self._after_id = None
#         if width < 1:
#             return
#         ow, oh = self._original.size
#         height = max(1, round(width * oh / ow))
#         resized = self._original.resize((width, height), Image.LANCZOS)
#         self._photo = ImageTk.PhotoImage(resized)
#         self.configure(image=self._photo)

# -----------------------------------------------------------------------
#    
# -----------------------------------------------------------------------
class FooterPanel(tk.Label):
    """
    CLAUDE
    Decorative footer that scales to its parent's width, keeping aspect ratio.
    """
    
    def __init__(self, parent, text: str = "", background="white", foreground="black", font=("Arial", 10), footer_image_path: str = "", **kwargs):        
        super().__init__(parent, bd=0, highlightthickness=0, **kwargs)
                
        self._original = Image.open(footer_image_path)
        self._photo = None          # keep a reference or Tk will garbage-collect it
        self._last_width = 0
        self._after_id = None
        parent.bind("<Configure>", self._on_parent_configure, add="+")
        self.configure(bg=background)

    def _on_parent_configure(self, event):
        # Only react to the parent itself, and only if the width changed.
        # (Ignoring height avoids a resize feedback loop, since changing the
        # footer height changes the layout and fires another <Configure>.)
        if event.widget is not self.master or event.width == self._last_width:
            return
        self._last_width = event.width
        if self._after_id:
            self.after_cancel(self._after_id)
        self._after_id = self.after(30, self._resize, event.width)  # debounce

    def _resize(self, width):
        self._after_id = None
        if width < 1:
            return
        ow, oh = self._original.size
        height = max(1, round(width * oh / ow))
        resized = self._original.resize((width, height), Image.Resampling.LANCZOS)
        self._photo = ImageTk.PhotoImage(resized)
        self.configure(image=self._photo)