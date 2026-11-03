import tkinter as tk
from PIL import Image, ImageTk, ImageOps

class HoverCanvasApp:
    
    STARTING_WIDTH:  int = 500
    STARTING_HEIGHT: int = 500    
    SCALE_IMAGE: float = 0.6
        
    def __init__(self, root, image_file_name: str, 
                 starting_width: int = STARTING_WIDTH, 
                 starting_height: int = STARTING_HEIGHT,
                 scale: float = SCALE_IMAGE) -> None:
                
        self.starting_width: int = starting_width
        self.starting_height: int = starting_height
        self.scale: float = scale
        self.image_file_name: str = image_file_name
        
        #
        # Create the window
        #
        self.root = root
        self.root.title("Smooth Hover Canvas")
        self.root.geometry("400x600")

        self.root.configure(background="white")

        #
        # Create a frame
        #
#        self.frame = tk.Frame(root, width=400, height=600, highlightthickness=0, highlightcolor="white", highlightbackground="white")
#        self.frame = tk.Frame(root, width=400, height=600)
        self.frame = tk.Frame(root)
        self.frame.pack_propagate(False)
        self.frame.pack(expand=True, fill = "both")

        self.frame.configure(background="white")

        #
        # Load the original image and resize it
        #        
        self.original_image = ImageOps.contain(Image.open(self.image_file_name), size=(self.starting_width, self.starting_height))
                
        self.base_width = int(self.starting_width * self.scale)
        self.base_height = int(self.starting_height * self.scale)

        self.current_width = self.base_width
        self.current_height = self.base_height

        self.target_width = self.base_width
        self.target_height = self.base_height
        
        self.canvas = tk.Canvas(self.frame, width=self.base_width, height=self.base_height, background="white", borderwidth=0, highlightthickness=0)
        self.canvas.pack(pady=20)

        #
        # Resize the image to the desired size on the canvas...
        #
        resized_image = self.original_image.resize((self.base_width, self.base_height))
        self.tk_image = ImageTk.PhotoImage(resized_image)
        self.image_id = self.canvas.create_image(0, 0, anchor="nw", image=self.tk_image)
        #borderwidth=0,compound="center",highlightthickness = 0

        #
        # Hover controls
        #
        self.canvas.bind("<Motion>", self.on_mouse_move)
        self.canvas.bind("<Leave>", self.on_mouse_leave)
        self.canvas.bind("<Button-1>", self.is_clicked)
        
        #
        # Animation controls
        #
        self.enlarged = False

#        self.resize_delta = 10
#        self.animation_speed = 2 # -> Pixels per frame

        self.resize_delta = 10
        self.animation_speed = 2 # -> Pixels per frame
        
        self.animate_resize()
        

    #
    #
    #
    def on_mouse_move(self, event):
        #
        # set margin to trigger mouse movement
        #
        margin_x = self.current_width * 0.25
        margin_y = self.current_height * 0.25
        
        if margin_x < event.x < self.current_width - margin_x and margin_y < event.y < self.current_height - margin_y :
            if not self.enlarged:
                self.enlarged = True
                self.target_width = self.base_width + self.resize_delta
                self.target_height = self.base_height + self.resize_delta
        else:
            if self.enlarged:
                self.enlarged = False
                self.target_width = self.base_width
                self.target_height = self.base_height

    #
    #
    #
    def on_mouse_leave(self, event):
        self.target_width = self.base_width
        self.target_height = self.base_height
        self.enlarged = False

    #
    #
    #
    def is_clicked(self, event):
        print("is clicked")
        pass
   
    #
    #
    #
    def animate_resize(self):
        
        if self.current_width != self.target_width or self.current_height != self.target_height:
            step_w = self.animation_speed if self.current_width < self.target_width else -self.animation_speed
            step_h = self.animation_speed if self.current_height < self.target_height else -self.animation_speed
        
            if abs(self.current_width - self.target_width) < self.animation_speed:
                self.current_width = self.target_width
            else:
                self.current_width += step_w
        
            if abs(self.current_height - self.target_height) < self.animation_speed:
                self.current_height = self.target_height
            else:
                self.current_height += step_h
            
            self.canvas.config(width=self.current_width, height=self.current_height)
            resized_image = self.original_image.resize((self.current_width, self.current_height))
            self.tk_image = ImageTk.PhotoImage(resized_image)
            
            self.canvas.itemconfig(self.image_id, image = self.tk_image)
        
        #
        # Call the process after 
        #            
        self.root.after(16, self.animate_resize)
            

        

if __name__ == "__main__":
    root = tk.Tk()
    image_file_name = "images/quizzer_900x900.png"    
    app = HoverCanvasApp(root, image_file_name)
    root.mainloop()
