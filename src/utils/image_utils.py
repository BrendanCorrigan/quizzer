import os
from PIL import Image, ImageTk
from pathlib import Path
#from PIL import Image, ImageTk
import tkinter as tk

from pathlib import Path

class ImageUtils:


    @staticmethod
    def load_image_from_file(image_file_name: str) -> Image.Image:
        '''
        Load an image from the given file name...
        '''
        image = None
        if not Path(image_file_name).is_file():
            raise FileNotFoundError(f"-> No file found for {image_file_name!r}")

        try:
            image = Image.open(image_file_name)
        except IOError:
            raise ValueError(f"-> can't open image {image_file_name!r}")

        return image


    @staticmethod
    def load_image(filename: str):
        if os.path.isfile(filename) and filename.endswith(".png"):
            img = Image.open(filename)
            # name = os.path.splitext(filename)[0]                    
            name = Path(filename).stem

            return {
                "name" : name,
                "filename" : filename,
                "image" : img
            }
        return None

    @staticmethod
    def load_images_from_list(filenames):
        images = {}
        index = 0
        for filename in filenames:
            if os.path.isfile(filename) and filename.endswith(".png"):
                result = ImageUtils.load_image(filename)
                if result:
                    result["index"] = index
                    images[result["name"]] = result
                    index += 1
                    
        return images


    @staticmethod
    def load_images_from_directory(directory):
        """
        Load all PNG images from the specified directory.
        """
        
        images = {}
        index = 0
        if os.path.isdir(directory):
            for filename in os.listdir(directory):                
                if filename.endswith(".png"):
                    img_path = os.path.join(directory, filename)
                    img = Image.open(img_path)

                    name = os.path.splitext(filename)[0]                    
                    images[name] = {
                        "index" : index,
                        "filename" : filename,
                        "image" : img
                    }
                    index += 1
                    #print(f"images[{name}]: {images[name]}")

            return images
        else:
            print(f"This is not a directory: {directory}")
        
        return images

    @staticmethod
    def resize_image(image, width: int, height: int, keep_square = True) ->ImageTk.PhotoImage: 
        if keep_square:
            size = min(width, height)
            width = size
            height = size
            
        resized_image = image.resize((width, height), Image.Resampling.LANCZOS)
        return ImageTk.PhotoImage(resized_image)


    @staticmethod
    def resize_images(images: dict, width: int, height: int, keep_square = True) -> dict: 
        if keep_square:
            size = min(width, height)
            width = size
            height = size
            
        for key in images:
            pil_image = images[key]["image"]
    
                    
                                    
            resized_image = pil_image.resize((width, height), Image.Resampling.LANCZOS)
            tk_image = ImageTk.PhotoImage(resized_image)
            images[key]["resized"] = tk_image
            
        return images

    @staticmethod
    def resize_images_direct(images: dict, width: int, height: int, keep_square = True) -> dict: 

        if keep_square:
            size = min(width, height)
            width = size
            height = size
            
        for key in images:
            pil_image = images[key]["image"]                                    
            images[key]["resized"] = pil_image.resize((width, height), Image.Resampling.LANCZOS)
            
        return images

    @staticmethod
    def scale_images(images: dict, scale = 1.0) -> dict: 
            
        for key in images:
            pil_image = images[key]["image"]
            
            width  = int(pil_image.width * scale)
            height = int(pil_image.height * scale)
                                    
            resized_image = pil_image.resize((width, height), Image.Resampling.LANCZOS)
            tk_image = ImageTk.PhotoImage(resized_image)
            images[key]["resized"] = tk_image
            
        return images

    @staticmethod
    def scale_images_direct(images: dict, scale = 1.0) -> dict: 
            
        for key in images:
            pil_image = images[key]["image"]
            
            width  = int(pil_image.width * scale)
            height = int(pil_image.height * scale)
                                    
            resized_image = pil_image.resize((width, height), Image.Resampling.LANCZOS)
            images[key]["resized"] = resized_image
            
        return images


    # --------------------------------------------------------------
    @staticmethod
    def load_frames(sprite_sheet_path: str, frame_count: int = None) -> list[ImageTk.PhotoImage] : # type: ignore
        """
        Slice the sprite sheet into individual frames.
        Args:
            sprite_sheet: Path to the sprite sheet image.
        Returns:
            List of PhotoImage frames.
        """
        if os.path.isfile(sprite_sheet_path):
        
            sprite_sheet = Image.open(sprite_sheet_path)
            
            if frame_count is None:
                frame_count = sprite_sheet.width // sprite_sheet.height
                
            frame_height = sprite_sheet.height
            frame_width = sprite_sheet.width // frame_count

            # print(f"  Frame size: {frame_width}x{frame_height}, count: {frame_count}")
            
            frames = []
            for i in range(frame_count):
                box = (i * frame_width, 0, (i + 1) * frame_width, frame_height)
                frame = sprite_sheet.crop(box)
#                frames.append(ImageTk.PhotoImage(frame))
                frames.append(frame)

            return frames
        else:
            return []

    # --------------------------------------------------------------
    @staticmethod
    def load_images_from_spritesheet(sprite_sheet_path: str, frame_count: int = None, names: list[str] = None) : # type: ignore
        frames = ImageUtils.load_frames(sprite_sheet_path, frame_count)

        images = {}
        index = 0
        
        for index, frame in enumerate(frames):
            if names and index < len(names):
                name = names[index]
            else:
                name = f"img{index}"
                
            images[name] = {
                "index" : index,
                "filename" : None,
                "image" : frame
            }
            
        return images


if __name__ == "__main__":
    images = ImageUtils.load_images_from_directory("images/TrainTracks")
    print(images)


