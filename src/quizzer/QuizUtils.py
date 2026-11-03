from pathlib import Path
import json
from typing import Any, Optional
from quizzer import DEFAULT_THEME
from PIL import Image, ImageTk
from utils.image_utils import ImageUtils

class QuizUtils(object):
    
    @staticmethod
    def load_theme(theme_file_name: str = DEFAULT_THEME):
        if theme_file_name and Path(theme_file_name).is_file():
            with open(theme_file_name, "r", encoding="utf-8") as theme_file:
                theme_data = json.load(theme_file)
                return theme_data
        
        raise ValueError(f"Need to pass the location of a valid theme file (e.g. theme.json)")
    

    @staticmethod
    def load_photoimage(filename: str, size: int = 64) -> Optional[ImageTk.PhotoImage]:
                
        photo_image = None        
        img : Optional[Image.Image] = ImageUtils.load_image_from_file(filename)
        if img:
            photo_image = ImageUtils.resize_image(img, size, size, True)
        return photo_image
            
        
        
        # if Path(filename).is_file():
        #     try:
        #         img = Image.open(filename).convert("RGBA")
        #         img.thumbnail((size, size), Image.LANCZOS)
        #         return ImageTk.PhotoImage(img)
        
        #     except (tk.TclError, OSError):
        #         return None  # unreadable/unsupported file -> caller uses placeholder

    
    # -------------------------------------------------------------------------------
    #
    # -------------------------------------------------------------------------------
    @staticmethod
    def as_number(value: Any) -> Optional[float]:
        """
        Convert "value" to a float, or None if it isn't numeric.
        """
        if isinstance(value, bool):
            return None
        
        if isinstance(value, (int, float)):
            return float(value)
        try:
            return float(str(value).strip().rstrip("%"))
        except ValueError:
            return None


if __name__ == "__main__":
    theme = QuizUtils.load_theme()
    print(theme)
    