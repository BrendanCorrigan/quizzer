# Quizzer
## A python application for displaying a quiz.

### How to run
The easiest way is to install uv and type command
```
uv run quizzer
```

instructions for installing uv are [here](https://docs.astral.sh/uv/getting-started/installation/) 

### Alternatively...
you need to install the following libraries..
```
pip install pillow
```
and then the quiz programme can be run from a windows batch command:
```
Quizzer.bat
```

## The Quiz
If it works you should be presented with a screen as follows:
![image of main screen](images/main_screen.png)

Choose a quiz and get quizzing!
(note - high score has not been implemented yet - there is still a lot to do!)

## How the quiz works
The Marvel_Movies and Solar_System quizzes have been hand written, the Pop_Music and Popular_Science quizzers were written by ChatGPT as an experiment.

To get get ChatGPT to write a quiz, give it the following prompt:
```
Create a quiz using the following template. The topic of the quiz should be <topic> and there should be <n> questions of varying difficulty on the topic. The Hint and Explanation elements within a question are optional.
{
	"name": "Name of the quiz goes here",
	"description": "A brief description of the quiz",
	"icon": "images/<create a logo for the quiz>.png",
	"category": "quiz category",
	"difficulty": "difficulty of the quiz",
	
	"ratings": {
		"A humerous message for top score":90,
		"A relevant message based on the quiz category":70,
		"Another message based on quiz category":50,
		"A mildly insulting message on lack of topic knowledge":30,
		"Another mildly insulting message":0
	},
	
	"questions":[
	
		{
			"id": 1,
			"tags": ["Marvel", "Movies", "Iron Man"],
			"difficulty": "easy",
			"score": 10,
			"type": "multiplechoice",
			"question": "Question to be asked goes here",
			"hint": "if the question is difficult include a hint",
			"explanation": "If the answer needs an explanation that can go here",
			"answers" :
			[
				{"text": "Answer 1", "comment": "Reason why this answer is not correct"},
				{"text": "Answer 2", "comment": "Correct, Reason why this answer is correct", "isCorrect": true},
				{"text": "Answer 3", "comment": "Reason why this answer is not correct"},
				{"text": "Answer 4", "comment": "Reason why this answer is not correct"}
			]
		}
	]
}
```
for example asking ChatGPT to create a geography quiz with 10 questions produced the following questions:
```
    "questions": [
        {
            "id": 1,
            "tags": ["Geography", "Capitals", "Europe"],
            "difficulty": "easy",
            "score": 10,
            "type": "multiplechoice",
            "question": "What is the capital city of France?",
            "answers": [
                {
                    "text": "Madrid",
                    "comment": "Madrid is the capital of Spain."
                },
                {
                    "text": "Paris",
                    "comment": "Correct! Paris is the capital and largest city of France.",
                    "isCorrect": true
                },
                {
                    "text": "Rome",
                    "comment": "Rome is the capital of Italy."
                },
                {
                    "text": "Berlin",
                    "comment": "Berlin is the capital of Germany."
                }
            ]
        },
```

To make the quiz more visual you can add images using the "picture" and "answerPicture" tags. The "picture" is displayed on the question panel, the "answerPicture" is displayed on the answer panel.
```
    "picture":"quizzes/Solar_System/images/lunarLander_700x700.jpg",
    "answerPicture": "quizzes/Solar_System/images/mars.png",
```

