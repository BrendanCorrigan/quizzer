import tkinter as tk
from quizzer.QuizPages import TitlePage, QuizSelectionPage, QuizStartPage
from quizzer.QuizRepository import QuizRepository, Questions
from quizzer.QuizPanels import FooterPanel
from typing import Optional
from quizzer.QuizTheme import QuizTheme


# -----------------------------------------------------------------------------------------------------
#
# -----------------------------------------------------------------------------------------------------
class Container(tk.Frame):

    def __init__(self, parent, theme: QuizTheme):
        super().__init__(parent)

        # self.background_colour = DEFAULT_THEME_PRIMARY_COLOUR
        # self.font_colour = DEFAULT_THEME_FONT_PRIMARY_COLOUR      
        # if "config" in theme.keys():
        #     self.background_colour = theme["config"].get("theme_primary_colour", DEFAULT_THEME_PRIMARY_COLOUR)
        #     self.font_colour = theme["config"].get("font_primary_colour", DEFAULT_THEME_FONT_PRIMARY_COLOUR)

        # configuring the location of the container using grid
        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=0)

        self.grid_columnconfigure(0, weight=1)
        self.configure(bg=theme.background_colour)

        if theme.show_footer:
            self.footer_image: str = theme.footer_image

            footer_panel = FooterPanel(self, text="This is the footer", footer_image_path=self.footer_image,
                                    background=theme.background_colour, foreground=theme.font_primary_colour, font=theme.small_font)
            footer_panel.grid(row=1, column=0, sticky="ew")
            
        self.pack(fill="both", expand=True)

# -------------------------------------------------------------------------------------------------------------
# 
# -------------------------------------------------------------------------------------------------------------
class Quiz(tk.Tk):
    
    def __init__(self, theme: QuizTheme, *args, **kwargs):
        super().__init__(*args, **kwargs)        

        
        self.theme = theme if theme is not None else QuizTheme()
        self.title(theme.name)

        self.window_width: int  = 600
        self.window_height: int = 600
        self.chosen_quiz: Optional[Questions] = None

        self.window_width = theme.window_width
        self.window_height = theme.window_height
        
        # if "window" in self.theme.keys():
        #     self.window_width  = self.theme["window"].get("width", 600)
        #     self.window_height = self.theme["window"].get("height", 900)
            
        self.geometry(f"{self.window_width}x{self.window_height}")
        
        # self.minsize(400, 600)
        # self.maxsize(600, 800)
        
        # self.background_colour = DEFAULT_THEME_PRIMARY_COLOUR        
        # if "config" in self.theme.keys():
        #     self.background_colour = self.theme["config"].get("theme_primary_colour", DEFAULT_THEME_PRIMARY_COLOUR)
                
        self.configure(bg=theme.background_colour)        
        self.container = Container(self, self.theme)

        # ------------------------------------------------------------------------------
        # Get repository of quizzes locally
        # ------------------------------------------------------------------------------
        self.quizRepository = QuizRepository(quizzes_dir=theme.quiz_directory)

        # ------------------------------------------------------------------------------        
        # We will now create a dictionary of frames
        # ------------------------------------------------------------------------------        
        self.frames = {}
        for page_class in (TitlePage, QuizSelectionPage):
            self.frames[page_class] = page_class(self.container, self, self.theme)
            self.frames[page_class].grid(row=0, column=0, sticky="nsew")

#         page_class = TitlePage
#         self.frames[page_class] = page_class(container, self, theme)
#         self.frames[page_class].grid(row=0, column=0, sticky="nsew")
            
        # for page_class in (HomePage, OptionsPage, CompletionPage, GovernedIntelligencePage, GridPage):
        #     self.frames[page_class] = page_class(container, self)
        #     self.frames[page_class].grid(row=0, column=0, sticky="nsew")

        # # ------------------------------------------------------------------------------        
        # # Add customer list seperately...
        # # ------------------------------------------------------------------------------
        # self.frames[CustomerListPage] = CustomerListPage(container, self, self.customers)
        # self.frames[CustomerListPage].grid(row=0, column=0, sticky="nsew")

        self.show_frame(TitlePage)


    def start_quiz(self, questions: Questions):
        quizStartPage = QuizStartPage(self.container, self, self.theme, questions=questions)
        quizStartPage.grid(row=0, column=0, sticky="nsew")
        quizStartPage.tkraise()
        
    def get_quizzes(self) -> list[Questions]:
        result = []
        if self.quizRepository:
            result = self.quizRepository.get_quizzes()
        return result

    def show_frame(self, page_class):
        frame = self.frames[page_class]
        frame.tkraise()        

    def show_frame_directly(self, frame):
        frame.tkraise()        

    def start(self):
        self.mainloop()
        