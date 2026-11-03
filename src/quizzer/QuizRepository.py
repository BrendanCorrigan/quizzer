from pathlib import Path
from dataclasses import dataclass
from typing import Optional
from quizzer.QuizUtils import QuizUtils
import json

# ---------------------------------------------------------------------------
# Data model
# ---------------------------------------------------------------------------
@dataclass
class Questions:
    """
    Everything the browser needs to know about a single quiz.
    """
    folder: Path     
    name: str        
    topic: str = "General"
    difficulty: str = "Unknown"
    description: str = ""
    question_count: int = 0
    icon_path: Optional[str] = None
    high_score: Optional[float] = None
    ratings: Optional[dict] = None
    questions: Optional[list[dict]] = None

    @property
    def questions_file(self) -> Path:
        return self.folder / QuizRepository.QUESTIONS_FILENAME

    @property
    def high_score_text(self) -> str:
        """
        High score formatted for display, e.g. '78%' (or '--').
        """
        if self.high_score is None:
            return "--"
        return f"{self.high_score:g}%"


# ---------------------------------------------------------------------------
# Repository of quizzes...
# ---------------------------------------------------------------------------
class QuizRepository:
    """
    Scans the quizzes directory and turns each questions.json (plus the
    optional quizscore.json) into a Questions class 
    """
    QUESTIONS_FILENAME = "questions.json"
    SCORES_FILENAME = "quizscore.json"

    # -------------------------------------------------------------------------------
    #
    # -------------------------------------------------------------------------------
    def __init__(self, quizzes_dir: str = "quizzes") -> None:

        if not Path(quizzes_dir).is_dir():
            raise ValueError(f"--> Quiz folder not found: {quizzes_dir}")

        self.quizzes_dir = Path(quizzes_dir)
        self.errors: list[str] = []
        self.quizzes: list[Questions] = []
        
        self.quizzes = self.load_all()
        
    # -------------------------------------------------------------------------------
    #
    # -------------------------------------------------------------------------------
    def load_all(self) -> list[Questions]:
        """
        Return every valid quiz, sorted alphabetically by name.
        """
        self.errors.clear()
        quizzes: list[Questions] = []

        for folder in sorted(p for p in self.quizzes_dir.iterdir() if p.is_dir()):
            questions_file = folder / self.QUESTIONS_FILENAME
            if not questions_file.is_file():
                continue  # not a quiz folder - quietly ignore it
            try:
                quizzes.append(self._parse(folder, questions_file))
            except (OSError, ValueError) as exc:  # JSONDecodeError is a ValueError
                self.errors.append(f"{folder.name}: {exc}")

        quizzes.sort(key=lambda q: q.name.lower())
        return quizzes

    # -------------------------------------------------------------------------------
    #
    # -------------------------------------------------------------------------------
    def _parse(self, folder: Path, questions_file: Path) -> Questions:
        """
        load a questions file to get the meta data
        """
        with questions_file.open(encoding="utf-8") as file:
            data = json.load(file)

        if isinstance(data, dict):
            questions = data.get("questions", [])
        else:
            raise ValueError("unexpected JSON structure")

        icon_value = data.get("icon")
        icon_path = (folder / icon_value) if icon_value else None

        return Questions(
            folder=folder,
            name=str(data.get("name", "Add a Name for this Quiz!") ),
            topic=str(data.get("category", "General")),
            difficulty=str(data.get("difficulty", "Unknown")),
            description=str(data.get("description", "")),
            question_count=len(questions),
            icon_path=icon_path,
            high_score=self._load_high_score(folder),
            ratings=data.get("ratings", {}),
            questions = data.get("questions", [])
        )

    # -------------------------------------------------------------------------------
    #
    # -------------------------------------------------------------------------------
    def _load_high_score(self, folder: Path) -> Optional[float]:
        """Best score (0-100) from ``quizscore.json``, or None if unavailable.
        """
        score_file = folder / self.SCORES_FILENAME
        if not score_file.is_file():
            return None
        try:
            with score_file.open(encoding="utf-8") as fh:
                data = json.load(fh)
        except (OSError, ValueError):
            return None

        # A dict may hold the high score directly...
        if isinstance(data, dict):
            for key in ("high_score", "highscore", "best", "best_score"):
                if key in data:
                    return QuizUtils.as_number(data[key])
            data = data.get("scores", [])      # ...or a list of attempts.

        if isinstance(data, list):
            values = [
                QuizUtils.as_number(item.get("score") if isinstance(item, dict) else item)
                for item in data
            ]
            values = [v for v in values if v is not None]
            return max(values) if values else None
        return QuizUtils.as_number(data)

    def get_quizzes(self) -> list[Questions]:
        return self.quizzes


if __name__ == "__main__":
#    repo = QuizRepository(quizzes_dir="quizzes")
    repo = QuizRepository()
    for quiz in repo.quizzes:
        print(quiz)
    
