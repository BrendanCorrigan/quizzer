import tkinter as tk
from quizzer.QuizPanels import ImagePanel
from quizzer.QuizList import QuizListView
from quizzer.QuizRepository import Questions
from quizzer.QuizController import QuizController
from quizzer.QuizTheme import QuizTheme


# --------------------------------------------------------------------------------------------------
#
# --------------------------------------------------------------------------------------------------
class TitlePage(tk.Frame):
        
    def __init__(self, parent, controller, theme: QuizTheme):
        super().__init__(parent)
        self.controller = controller
        self.theme = theme        
        self.configure(bg=theme.background_colour)
        
        if theme.hasLogo:
            self.image_panel = ImagePanel(self, theme.logo, background=theme.background_colour).pack()    
            self.logo_duration: int = theme.logo_duration
            
        self.after(self.logo_duration, lambda:self.controller.show_frame(QuizSelectionPage))

# --------------------------------------------------------------------------------------------------
#
# --------------------------------------------------------------------------------------------------
class QuizSelectionPage(tk.Frame):
    def __init__(self, parent, controller, theme: QuizTheme):
        super().__init__(parent)
        self.controller = controller
        self.theme = theme
        self.configure(bg=theme.background_colour)
                
        quizList = QuizListView(self, theme, on_select=self.do_something)
        quizList.pack(side="top", expand=True, fill="both", padx=10, pady=10)
        quizList.show(controller.get_quizzes())
        
    def do_something(self, questions: Questions):
        self.controller.start_quiz(questions)
                     
# --------------------------------------------------------------------------------------------------
#
# --------------------------------------------------------------------------------------------------
class QuizStartPage(tk.Frame):
    def __init__(self, parent, controller, theme: QuizTheme, questions: Questions):
        super().__init__(parent)
        self.controller = controller        
        self.configure(bg=theme.background_colour)

        self.quiz_controller = QuizController(self, theme=theme, quiz=questions)
        self.quiz_controller.pack(side="top", expand=True, fill="both", padx=0, pady=0)
    
    def select_quiz(self):
        self.controller.show_frame(QuizSelectionPage)
        
        