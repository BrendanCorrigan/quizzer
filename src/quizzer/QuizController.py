import tkinter as tk
import random
from quizzer.QuestionPanels import QuestionPanel, QuizResultsPage, AnswerPanel, NavigationPanel
from quizzer.QuizTheme import QuizTheme



class QuizController(tk.Frame):

    def __init__(self, parent, quiz, theme: QuizTheme):     
        super().__init__(parent)        
        self.configure(bg=theme.background_colour)
        self.parent = parent
        
        self.quiz = quiz
        self.theme = theme
        self.questions = quiz.questions
        self.score = 0
        self.startQuiz()
        
	# -------------------------------------------------------
	# Display the first question...
	# -------------------------------------------------------		   
    def startQuiz(self):
        random.shuffle(self.questions)
        self.questionNumber = 0
        self.displayQuestion(self.questions[self.questionNumber])

	# -------------------------------------------------------
	# Display next question until no more questions to ask :)
	# -------------------------------------------------------		   
    def nextQuestion(self):
        self.questionNumber += 1
        self.answerPanel.pack_forget()
        self.navigationPanel.pack_forget()
        
        if self.questionNumber < len(self.questions):        
            self.displayQuestion(self.questions[self.questionNumber])
        else:
            self.displayResults()
    
	# -------------------------------------------------------
	# 
	# -------------------------------------------------------		   
    def displayQuestion(self, question):
        self.questionPanel = QuestionPanel(self, theme=self.theme, question=question, callback=self.displayAnswer)
        self.questionPanel.pack()        
        
	# -------------------------------------------------------
	# 
	# -------------------------------------------------------		   
    def displayAnswer(self, answer):        
        self.questionPanel.pack_forget()
        self.answerPanel = AnswerPanel(self, self.questions[self.questionNumber], chosenAnswer=answer, theme=self.theme)
        self.answerPanel.pack(side=tk.TOP, expand=True, fill="both")
        self.navigationPanel = NavigationPanel(self, callback = self.nextQuestion, theme=self.theme, text="Next Question")
        self.navigationPanel.pack(side="bottom")
        self.score += self.answerPanel.getScore()

	# -------------------------------------------------------
	# 
	# -------------------------------------------------------		   
    def select_quiz(self):
        self.resultsPanel.pack_forget()
        self.navigationPanel.pack_forget()
        self.parent.select_quiz()
        
	# -------------------------------------------------------
	# 
	# -------------------------------------------------------		   
    def displayResults(self):
        self.answerPanel.pack_forget()
        self.navigationPanel.pack_forget()
        self.resultsPanel = QuizResultsPage(self, self, self.theme, self.score, self.quiz)
        self.resultsPanel.pack(side=tk.TOP, expand=True, fill="both")
        self.navigationPanel = NavigationPanel(self, callback = self.select_quiz, theme=self.theme, text="Back to quiz selection...")
        self.navigationPanel.pack(side="bottom")
        