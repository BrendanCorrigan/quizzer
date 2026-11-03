import tkinter as tk
from typing import Callable, Optional
from quizzer.QuizRepository import Questions
from utils.drawing_utils import DrawingUtils
from quizzer.QuizUtils import QuizUtils
from quizzer.QuizTheme import QuizTheme


    # BG = "#f2f4f8"             # window / list background
    # CARD_BG = "#ffffff"
    # CARD_HOVER_BG = "#eaf1ff"
    # CARD_BORDER = "#1f2933"    # dark outline like the mock-up
    # CARD_BORDER_WIDTH = 2
    # TEXT = "#1f2933"
    # SUBTEXT = "#5f6c7b"

    # FONT_TITLE = ("Segoe UI", 15, "bold")
    # FONT_BODY = ("Segoe UI", 10)
    # FONT_SMALL = ("Segoe UI", 9)
    # FONT_HEADER = ("Segoe UI", 20, "bold")
    # FONT_SCORE_LABEL = ("Segoe UI", 13)
    # FONT_SCORE_VALUE = ("Segoe UI", 32)

    # ICON_SIZE = 90             # icons are scaled to fit a square this big (px)
    # CARD_PADDING = 18          # space between the rounded border and content
    # CARD_RADIUS = 20           # corner radius of the rounded border

    # # Colour of the difficulty text.
    # DIFFICULTY_COLOURS: Dict[str, str] = {
    #     "easy": "#2e9e5b",
    #     "medium": "#c58a0a",
    #     "hard": "#d64545",
    # }
    # DEFAULT_DIFFICULTY_COLOUR = "#7b8794"

    # @classmethod
    # def difficulty_colour(cls, difficulty: str) -> str:
    #     return cls.DIFFICULTY_COLOURS.get(
    #         difficulty.strip().lower(), cls.DEFAULT_DIFFICULTY_COLOUR
    #     )


# ---------------------------------------------------------------------------
# One quiz "card" (the mock-up)
# ---------------------------------------------------------------------------
class QuizCard(tk.Canvas):
    """The rounded selection box for a single quiz::

        +--------------------------------------------------------+
        |  +------+   Name of the quiz                           |
        |  | icon |   Topic  -  N questions        High Score    |
        |  |      |   Difficulty                      78%        |
        |  +------+   About the quiz...                          |
        +--------------------------------------------------------+

    tkinter has no rounded-rectangle widget, so the card is a Canvas: the
    rounded border is a smoothed polygon drawn on it, and the real widgets
    (icon, labels) live in a Frame embedded on top.

    ``on_select`` is called with the :class:`Quiz` when the card is clicked,
    keeping this widget ignorant of what "opening" a quiz actually does.
    """
    
    ICON_SIZE = 90             # icons are scaled to fit a square this big (px)
    CARD_PADDING = 18          # space between the rounded border and content
    
    CARD_RADIUS = 20           # corner radius of the rounded border
    CARD_BORDER = "#1f2933"    # dark outline like the mock-up
    CARD_BORDER_WIDTH = 2
    CARD_HOVER_BG = "#eaf1ff"

    FONT_TITLE = ("Segoe UI", 15, "bold")
    FONT_BODY = ("Segoe UI", 10)
    FONT_SMALL = ("Segoe UI", 9)
    FONT_HEADER = ("Segoe UI", 20, "bold")
    FONT_SCORE_LABEL = ("Segoe UI", 13)
    FONT_SCORE_VALUE = ("Segoe UI", 32)
    
    # Colour of the difficulty text.
    DIFFICULTY_COLOURS: dict[str, str] = {
        "easy": "#2e9e5b",
        "medium": "#c58a0a",
        "hard": "#d64545",
    }
    DEFAULT_DIFFICULTY_COLOUR = "#7b8794"
    
    # Space (px) the icon + score columns take, used to size text wrapping.
    _SCORE_COLUMN_WIDTH = 150

    # -----------------------------------------------------------------------------------------------------------------
    #
    # -----------------------------------------------------------------------------------------------------------------

#    def __init__(self, parent, quiz: Questions, icon: tk.PhotoImage, on_select: Callable[[Questions], None]) -> None:
#    def __init__(self, parent, theme, quiz: Questions) -> None:
    def __init__(self, parent, theme: QuizTheme, quiz: Questions, on_select: Callable[[Questions], None]) -> None:
        
        self.background_colour = theme.background_colour
        self.card_background_colour = theme.background_secondary_colour
        self.font_colour = theme.font_primary_colour
        
        # if "config" in theme.keys():
        #     self.background_colour = theme["config"].get("theme_primary_colour", DEFAULT_THEME_PRIMARY_COLOUR)
        #     self.card_background_colour = theme["config"].get("theme_secondary_colour", DEFAULT_THEME_PRIMARY_COLOUR)
        #     self.font_colour = theme["config"].get("font_primary_colour", DEFAULT_THEME_PRIMARY_COLOUR)
                    
        super().__init__(parent, background=theme.background_colour, highlightthickness=0, cursor="hand2")
        self.configure(bg=theme.background_colour)
        
        self.quiz = quiz                
        self._on_select = on_select

        self._icon = None                
        if quiz.icon_path:
            self._icon = QuizUtils.load_photoimage(quiz.icon_path, 90)
                
        self._shape_id: Optional[int] = None
        self._fill = self.card_background_colour

        # Frame holding the card's real widgets, embedded in the canvas.
        self._inner = tk.Frame(self, background=self.card_background_colour)
        self._window_id = self.create_window(QuizCard.CARD_PADDING, QuizCard.CARD_PADDING, window=self._inner, anchor="nw")


        self._redraw_pending = False
        self._description_label: Optional[tk.Label] = None
        self._build_widgets()
        self._inner.update_idletasks()   # safe here: we're not in an event handler
        self._fit_height()

        self._bind_interaction(self)
#        self.bind("<Configure>", self._on_resize)
        self.bind("<Configure>", self._schedule_redraw)
        self._inner.bind("<Configure>", self._schedule_redraw, add="+")

    # -----------------------------------------------------------------------------------------------------------------
    #
    # -----------------------------------------------------------------------------------------------------------------
    @classmethod
    def difficulty_colour(cls, difficulty: str) -> str:
        return QuizCard.DIFFICULTY_COLOURS.get(
            difficulty.strip().lower(), cls.DEFAULT_DIFFICULTY_COLOUR
        )

    # -----------------------------------------------------------------------------------------------------------------
    #
    # -----------------------------------------------------------------------------------------------------------------
    def _build_widgets(self) -> None:
        """Three columns: icon | text details (stretches) | high score."""
        inner = self._inner
        inner.columnconfigure(1, weight=1)

        if self._icon:
        # Column 0: the quiz logo, with a dark outline like the mock-up.
            tk.Label(inner, image=self._icon, background=self.card_background_colour, highlightthickness=2, highlightbackground=QuizCard.CARD_BORDER,
                    highlightcolor=QuizCard.CARD_BORDER,borderwidth=0).grid(row=0, column=0, padx=(0, 20), sticky="n")

        # Column 1: four lines of text, as in the mock-up.
        details = tk.Frame(inner, background=self.card_background_colour)
        details.grid(row=0, column=1, sticky="nsew")

        self._text_label(details, self.quiz.name, QuizCard.FONT_TITLE, self.font_colour, self.card_background_colour).pack(fill="x")
        self._text_label(details, f"Topic: {self.quiz.topic}  •  {self._question_text()}", QuizCard.FONT_BODY, self.font_colour, self.card_background_colour).pack(fill="x", pady=(2, 0))
        self._text_label(details, f"Difficulty: {self.quiz.difficulty}", QuizCard.FONT_BODY, QuizCard.difficulty_colour(self.quiz.difficulty), self.card_background_colour).pack(fill="x")
        
        if self.quiz.description:
            self._description_label = self._text_label(details, self.quiz.description, QuizCard.FONT_SMALL, self.font_colour, self.card_background_colour)
            self._description_label.configure(justify="left", wraplength=400)
            self._description_label.pack(fill="x", pady=(4, 0))

        # Column 2: the high score, centred.
        score = tk.Frame(inner, background=self.card_background_colour)
        score.grid(row=0, column=2, padx=(20, 4))
        tk.Label(score, text="High Score", font=QuizCard.FONT_SCORE_LABEL, background=self.card_background_colour, foreground=self.font_colour).pack()
        tk.Label(score, text=self.quiz.high_score_text, font=QuizCard.FONT_SCORE_VALUE, background=self.card_background_colour, foreground=self.font_colour).pack()

    # -----------------------------------------------------------------------------------------------------------------
    #
    # -----------------------------------------------------------------------------------------------------------------
    def _question_text(self) -> str:
        n = self.quiz.question_count
        return f"{n} question{'' if n == 1 else 's'}"

    # -----------------------------------------------------------------------------------------------------------------
    #
    # -----------------------------------------------------------------------------------------------------------------
    @staticmethod
    def _text_label(parent: tk.Misc, text: str, font: tuple, colour: str, bacground_colour: str) -> tk.Label:
        """
        Left-aligned label on the card background.
        """
        return tk.Label(parent, text=text, font=font, foreground=colour, background=bacground_colour, anchor="w")

    # -----------------------------------------------------------------------------------------------------------------
    #
    # -----------------------------------------------------------------------------------------------------------------
    def _fit_height(self) -> None:
        """Make the canvas exactly tall enough for its content + padding."""
#        self._inner.update_idletasks()
        wanted = self._inner.winfo_reqheight() + 2 * QuizCard.CARD_PADDING
        if int(self.cget("height")) != wanted:
            self.configure(height=wanted)

    # -----------------------------------------------------------------------------------------------------------------
    #
    # -----------------------------------------------------------------------------------------------------------------
    def _schedule_redraw(self, _event: Optional[tk.Event] = None) -> None:
        """Ask for ONE redraw once tkinter is idle.

        Resize events can arrive several times in a burst, and out of date
        ones must not overwrite newer ones.  So the handler never draws from
        the event's size; it just books a redraw, and the redraw reads the
        widget's *current* size.  (Calling update_idletasks() inside the
        <Configure> handler, as an earlier version did, caused a stale event
        to draw a too-narrow border on top of the correct one.)
        """
        if self._redraw_pending:
            return
        self._redraw_pending = True
        self.after_idle(self._redraw)


    def _redraw(self) -> None:
        """Resize the content, re-wrap the text and redraw the border."""
        self._redraw_pending = False
        width = self.winfo_width()
        if width <= 1:               # not laid out yet; a later event will retry
            return

        self.itemconfigure(self._window_id, width=max(1, width - 2 * QuizCard.CARD_PADDING))

        # Let the description use whatever width the icon and score leave.
        if self._description_label is not None:
            available = (
                width - 2 * QuizCard.CARD_PADDING - QuizCard.ICON_SIZE
                - self._SCORE_COLUMN_WIDTH
            )
            self._description_label.configure(wraplength=max(120, available))

        self._fit_height()           # a height change triggers another redraw
        self._draw_border(width, max(self.winfo_height(), 2))


    # -----------------------------------------------------------------------------------------------------------------
    #
    # -----------------------------------------------------------------------------------------------------------------
    # def _on_resize(self, event: tk.Event) -> None:
    #     """Redraw the border and re-wrap the description for the new width."""
    #     width = event.width
    #     self.itemconfigure(self._window_id, width=max(1, width - 2 * QuizCard.CARD_PADDING))

    #     # Let the description use whatever width the icon and score leave.
    #     if self._description_label is not None:
    #         available = (
    #             width - 2 * QuizCard.CARD_PADDING - QuizCard.ICON_SIZE
    #             - self._SCORE_COLUMN_WIDTH
    #         )
    #         self._description_label.configure(wraplength=max(120, available))

    #     self._fit_height()
    #     self._draw_border(width, max(event.height, 2))

    # -----------------------------------------------------------------------------------------------------------------
    #
    # -----------------------------------------------------------------------------------------------------------------
    def _draw_border(self, width: int, height: int) -> None:
        """(Re)draw the rounded rectangle behind the content."""
        if self._shape_id is not None:
            self.delete(self._shape_id)
        inset = QuizCard.CARD_BORDER_WIDTH
        self._shape_id = self._rounded_rect(
            inset, inset, width - inset, height - inset, QuizCard.CARD_RADIUS
        )
        self.tag_lower(self._shape_id)     # keep it behind the embedded frame

    # -----------------------------------------------------------------------------------------------------------------
    #
    # -----------------------------------------------------------------------------------------------------------------
    def _rounded_rect(self, x1: int, y1: int, x2: int, y2: int, r: int) -> int:
        """Draw a rounded rectangle.

        Trick: a polygon with ``smooth=True`` rounds off its corners; listing
        each corner point twice makes the curves tight instead of bulging.
        """
        points = DrawingUtils.rounded_rect_points(x1, y1, x2, y2, r)                
        return self.create_polygon(points, smooth=True, fill=self._fill, outline=QuizCard.CARD_BORDER, width=QuizCard.CARD_BORDER_WIDTH)

    # -----------------------------------------------------------------------------------------------------------------
    #
    # -----------------------------------------------------------------------------------------------------------------
    def _bind_interaction(self, widget: tk.Misc) -> None:
        """Recursively add hover + click behaviour to the card and children."""
        widget.bind("<Button-1>", lambda _e: self._on_select(self.quiz))
        widget.bind("<Enter>", lambda _e: self._set_background(QuizCard.CARD_HOVER_BG))
        widget.bind("<Leave>", self._on_leave)
        for child in widget.winfo_children():
            self._bind_interaction(child)

    # -----------------------------------------------------------------------------------------------------------------
    #
    # -----------------------------------------------------------------------------------------------------------------
    def _on_leave(self, _event: tk.Event) -> None:
        """Only un-highlight when the pointer has really left the whole card
        (moving between child widgets also fires <Leave>)."""
        x, y = self.winfo_pointerxy()
        if self.winfo_containing(x, y) not in self._all_descendants(self):
            self._set_background(self.card_background_colour)

    # -----------------------------------------------------------------------------------------------------------------
    #
    # -----------------------------------------------------------------------------------------------------------------
    def _all_descendants(self, widget: tk.Misc) -> list[tk.Misc]:
        found = [widget]
        for child in widget.winfo_children():
            found.extend(self._all_descendants(child))
        return found

    # -----------------------------------------------------------------------------------------------------------------
    #
    # -----------------------------------------------------------------------------------------------------------------
    def _set_background(self, colour: str) -> None:
        """
        Recolour the rounded shape and every Frame/Label inside it.
        """
        self._fill = colour
        if self._shape_id is not None:
            self.itemconfigure(self._shape_id, fill=colour)
        for widget in self._all_descendants(self._inner):
            if isinstance(widget, (tk.Frame, tk.Label)):
                widget.configure(background=colour)
        # The icon's outline sits on the label; keep its dark border colour.

