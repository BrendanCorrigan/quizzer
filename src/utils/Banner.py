import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk

class Banner(tk.Frame):

	DEFAULT_SIZE = (48,48)

	# -------------------------------------------------------
	# 
	# -------------------------------------------------------		   
	def __init__(self, parent, text = None, imageFile = None, imageSize = None):	
		tk.Frame.__init__(self, parent)
		
		self.imageSize = imageSize
		self.parent = parent
		self.pack(fill='x')
	
		self.defaultSize = Banner.DEFAULT_SIZE

		if imageFile:
			self.imageIcon = Image.open(imageFile)
			
			if imageSize:
				self.defaultSize = (imageSize, imageSize)
			
			resizedImage = self.imageIcon.resize(self.defaultSize) 
			self.iconPhoto = ImageTk.PhotoImage(resizedImage)
			
			iconLabel = ttk.Label(self, image=self.iconPhoto)
			iconLabel.pack(side="left", padx=10, pady=10)
			
		if text:
			textLabel = ttk.Label(self, text=text, font=("Helvetica", 14))
			textLabel.pack(side="left", padx=10)
		
		

# -------------------------------------------------------

#if __name__ == "__main__":
#	app = Quiz("quizzes/solarSystemQuiz.json")


	   