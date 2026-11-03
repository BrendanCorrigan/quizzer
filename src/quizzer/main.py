
from quizzer.Quiz import Quiz
from quizzer.QuizTheme import QuizTheme

def main():
    theme = QuizTheme()
    quiz = Quiz(theme)
    quiz.start()

if __name__ == "__main__":
    main()
