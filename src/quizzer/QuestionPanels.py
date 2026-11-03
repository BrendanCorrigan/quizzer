import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk, ImageOps
import random

from quizzer.QuizTheme import QuizTheme
from quizzer.QuizUtils import QuizUtils

    # -------------------------------------------------------
    #
    # -------------------------------------------------------

# class TrueFalseQuestion(tk.Frame):
#     def __init__(self, parent, theme, answers: list):
#         super().__init__(parent)

#         self.background_colour = theme["config"].get("theme_primary_colour", DEFAULT_THEME_PRIMARY_COLOUR)                
#         self.text_colour = theme["config"].get("font_primary_colour", DEFAULT_THEME_FONT_PRIMARY_COLOUR)                

#         style = ttk.Style()
#         style.configure("W.TButton", background=self.background_colour, foreground=self.text_colour, font=("calibri", 15, "bold"))
        
#         for answer in answers:

#             self.imageIcon = None
#             if answer["text"].lower() == "true" or answer["text"].lower() == "yes":
#                 self.imageIcon = QuestionPanel.thumbsUpImage
#             else:
#                 self.imageIcon = QuestionPanel.thumbsDownImage

#             button = ttk.Button(self, text=answer["text"], style="W.TButton", image=self.imageIcon, compound="top",
#                                 command=lambda btext=answer["text"]: self.buttonPressed(btext))
#             button.pack(side="left", expand=True, fill="both", pady=5)

#     def buttonPressed(self, buttonText):
#         chosenAnswer = None
#         for answer in self.question["answers"]:
#             if answer["text"] == buttonText:
#                 chosenAnswer = answer
#                 break

#         assert chosenAnswer, "Problem with code - no answer selected!"
#         self.callback(chosenAnswer)

# --------------------------------------------------------------------------------------------------
#
# --------------------------------------------------------------------------------------------------
class QuestionPanel(tk.Frame):

    DEFAULTS_SET = False

    thumbsUpImage = None
    thumbsDownImage = None
    tickImage = None
    crossImage = None

	# ---------------------------------------------------------------------------------------
	# 
	# ---------------------------------------------------------------------------------------
    def __init__(self, parent, theme: QuizTheme, question, callback):
        super().__init__(parent)
        # self.controller = controller
        self.callback = callback
        self.theme = theme
        self.configure(bg=theme.background_colour)

        assert question, "Quesion Panel require a question to ask"
        self.question = question

        self.load_assets(theme)

        if "picture" in self.question:
            pic_resized = ImageOps.contain(Image.open(self.question["picture"]), size=(250, 250))
            self.picture = ImageTk.PhotoImage(pic_resized)

            iconLabel = ttk.Label(self, image=self.picture, background=theme.background_colour)
            # iconLabel.pack(padx=10, pady=10)
            iconLabel.pack(pady=20)

        style = ttk.Style()
        style.configure("W.TLabel", background=theme.background_colour, foreground=theme.font_primary_colour, font=theme.medium_font)

        questionTextLabel = ttk.Label(self, text=self.question["question"], style="W.TLabel", wraplength=375, anchor="center", justify="center")
        questionTextLabel.pack(expand=True, fill="both", padx=10, pady=10)

        type = self.question["type"]

        if type == "multiplechoice":
            answerFrame = self.multiChoiceFrame(self.question["answers"], theme)
            answerFrame.pack(expand=True, fill="both", padx=10, pady=10)

        elif type == "truefalse":
            answerFrame = self.trueFalseFrame(self.question["answers"], theme)
            answerFrame.pack(expand=True, fill="both", padx=10, pady=10)

        self.pack(expand=True, fill="both")

	# ---------------------------------------------------------------------------------------
	# 
	# ---------------------------------------------------------------------------------------
    def load_assets(self, theme):

        if not QuestionPanel.DEFAULTS_SET:
            QuestionPanel.thumbsUpImage = QuizUtils.load_photoimage(theme.thumbsUpImage_file, size=64)
            QuestionPanel.thumbsDownImage = QuizUtils.load_photoimage(theme.thumbsDownImage_file, size=64)
            QuestionPanel.tickImage = QuizUtils.load_photoimage(theme.tick_file, size=64)
            QuestionPanel.crossImage = QuizUtils.load_photoimage(theme.cross_file, size=64)
            QuestionPanel.DEFAULTS_SET = True
            
	# ---------------------------------------------------------------------------------------
	# 
	# ---------------------------------------------------------------------------------------
    def buttonPressed(self, buttonText):
        chosenAnswer = None
        for answer in self.question["answers"]:
            if answer["text"] == buttonText:
                chosenAnswer = answer
                break

        assert chosenAnswer, "Problem with code - no answer selected!"
        self.callback(chosenAnswer)

	# ---------------------------------------------------------------------------------------
	# 
	# ---------------------------------------------------------------------------------------
    def multiChoiceFrame(self, answers: list, theme: QuizTheme):
        frame = tk.Frame(self)
        frame.configure(bg=theme.background_colour)

        random.shuffle(answers)
        # self.configure(bg=theme.background_colour)

        style = ttk.Style()
        style.configure("W.TButton", background=theme.background_colour, foreground=theme.font_primary_colour, font=("calibri", 15, "bold"))

        for answer in answers:
            button = ttk.Button(frame, text=answer["text"], style="W.TButton", command=lambda btext=answer["text"]: self.buttonPressed(btext))
            button.pack(expand=True, fill="both", pady=5)

        return frame

	# ---------------------------------------------------------------------------------------
	# 
	# ---------------------------------------------------------------------------------------
    def trueFalseFrame(self, answers: list, theme: QuizTheme):
        frame = tk.Frame(self)
        frame.configure(bg=theme.background_colour)

        style = ttk.Style()
        style.configure("W.TButton", background=theme.background_colour, foreground=theme.font_primary_colour, font=("calibri", 15, "bold"))

        for answer in answers:

            self.imageIcon = QuestionPanel.thumbsDownImage
            if answer["text"].lower() == "true" or answer["text"].lower() == "yes":
                self.imageIcon = QuestionPanel.thumbsUpImage
            else:
                self.imageIcon = QuestionPanel.thumbsDownImage

            if self.imageIcon is not None:
                button = ttk.Button(frame, text=answer["text"], style="W.TButton", image=self.imageIcon, compound="top",
                                    command=lambda btext=answer["text"]: self.buttonPressed(btext))
                button.pack(side="left", expand=True, fill="both", pady=5)

        return frame

# --------------------------------------------------------------------------------------------------
#
# --------------------------------------------------------------------------------------------------
class AnswerPanel(tk.Frame):

	DEFAULT_SIZE = (96,96)
	ANSWER_RIGHT_IMAGE = None
	ANSWER_WRONG_IMAGE = None

	# ---------------------------------------------------------------------------------------
	# 
	# ---------------------------------------------------------------------------------------
	def __init__(self, parent, question, chosenAnswer, theme: QuizTheme):
		super().__init__(parent)        
		self.configure(bg=theme.background_colour)
     	
		# tk.Frame.__init__(self, parent)
		# self.parent = parent
      
		assert question, "Answer Panel require a question to ask"
		assert chosenAnswer, "Answer Panel require a chosen answer(s) to check"

		self.question = question
		self.chosenAnswer = chosenAnswer

		# ------------------------------------------------------------------------------------
		# Statically load the images...
		# ------------------------------------------------------------------------------------
		if AnswerPanel.ANSWER_RIGHT_IMAGE is None:
			AnswerPanel.ANSWER_RIGHT_IMAGE = ImageTk.PhotoImage(Image.open(theme.tick_file).resize(AnswerPanel.DEFAULT_SIZE))
   
		if AnswerPanel.ANSWER_WRONG_IMAGE is None:
			AnswerPanel.ANSWER_WRONG_IMAGE = ImageTk.PhotoImage(Image.open(theme.cross_file).resize(AnswerPanel.DEFAULT_SIZE))

		# ------------------------------------------------------------------------------------
		# Check the validity of the answer...
		# ------------------------------------------------------------------------------------
		iconLabel = None
		self.answerCorrect = False
		if "isCorrect" in chosenAnswer and chosenAnswer["isCorrect"] == True:          
			iconLabel = ttk.Label(self, image=AnswerPanel.ANSWER_RIGHT_IMAGE,anchor="center", background=theme.background_colour)
			self.answerCorrect = True
		else:
			iconLabel = ttk.Label(self, image=AnswerPanel.ANSWER_WRONG_IMAGE,anchor="center", background=theme.background_colour)
   
		iconLabel.pack(side='top', anchor='center', padx=10, pady=10)
      
		if "answerPicture" in self.question:
			pic_resized = ImageOps.contain(Image.open(self.question["answerPicture"]), size=(250, 250))
			self.picture = ImageTk.PhotoImage(pic_resized)
			iconLabel = ttk.Label(self, image=self.picture)
			iconLabel.pack(pady=10)
   
		# ------------------------------------------------------------------------------------
		# If there is a Comment display the comment...
		# ------------------------------------------------------------------------------------
		if "comment" in chosenAnswer:
			style = ttk.Style()
			style.configure("W.TLabel", background=theme.background_secondary_colour, foreground=theme.font_primary_colour, font=("Helvetica", 16, "bold"))								
			answerTextLabel = ttk.Label(self, text=chosenAnswer["comment"], style="W.TLabel", wraplength=375, anchor="center", justify="center")
			answerTextLabel.pack(expand=True, fill="both", padx=10)
   
		# ------------------------------------------------------------------------------------
		# If the answer is incorrect, display the right answer...
		# ------------------------------------------------------------------------------------
		if not self.answerCorrect:
			correctAnswer = {"text":"NOT DEFINED"}

			for answer in self.question["answers"]:
				if "isCorrect" in answer and answer["isCorrect"] == True:
					correctAnswer = answer
					break

			correctAnswerLabel = ttk.Label(self, text=f"The correct answer is :\n {correctAnswer['text']}", style="W.TLabel",
							wraplength=375, anchor="center", justify="center")
			correctAnswerLabel.pack(expand=True, fill="both", padx=10)

	# ----------------------------------------------------------------------------------------
	#
	# ----------------------------------------------------------------------------------------         
	def getScore(self):
		return self.question["score"] if self.answerCorrect else 0

                  
# --------------------------------------------------------------------------------------------------
#
# --------------------------------------------------------------------------------------------------
class QuizResultsPage(tk.Frame):

    def __init__(self, parent, controller, theme: QuizTheme, score, quiz):
        super().__init__(parent)
        self.controller = controller
        self.theme = theme
        
        self.configure(bg = theme.background_colour)
  
        self.quiz = quiz
        self.ratings = quiz.ratings

        maximumScore = sum(question['score'] for question in quiz.questions)
        percentageRating = (score / maximumScore) * 100.0
        scoreText = f"{score} / {maximumScore} ({percentageRating:.1f}%)"

        self.scoreLabel = tk.Label(self, text="Score", font=theme.large_font, bg=theme.background_colour, fg=theme.font_primary_colour)
        self.scoreLabel.pack(padx=10)

        self.textLabel = tk.Label(self, text=scoreText, font=theme.large_font, bg=theme.background_colour, fg=theme.font_primary_colour)
        self.textLabel.pack(pady=20, padx=10)

        ratingText = ""
        for rating in self.ratings:
            if percentageRating > self.ratings[rating]:
                ratingText = rating
                break

        self.ratingLabel = tk.Label(self, text=ratingText, font=theme.medium_font, bg=theme.background_colour, fg=theme.font_primary_colour)
        self.ratingLabel.pack(pady=40, padx=40)
       			      
        self.pack(expand=True, fill="both", pady=30)

# --------------------------------------------------------------------------------------------------
#
# --------------------------------------------------------------------------------------------------
class NavigationPanel(tk.Frame):

	def __init__(self, parent, callback, theme: QuizTheme, text: str):	
		super().__init__(parent)        
		self.configure(bg=theme.background_colour)

		self.callback = callback

		style = ttk.Style()
		style.configure("W.TButton", background=theme.background_colour, foreground=theme.font_primary_colour, font=("calibri", 15, "bold"))

		nextButton = ttk.Button(self, text=text, style="W.TButton", command=self.callback)
		nextButton.pack(side="right", padx=10, pady=10)

		self.pack(fill="x")
