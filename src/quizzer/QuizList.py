import sys
import tkinter as tk
from tkinter import ttk
from typing import Callable, List

from quizzer.QuizRepository import Questions
from quizzer.QuizCard import QuizCard
from quizzer.QuizTheme import QuizTheme

# ---------------------------------------------------------------------------
# Reusable scrolling container
# Developed by CLAUDE AI - and pretty much works.
# ---------------------------------------------------------------------------
class ScrollableFrame(ttk.Frame):
    """A frame whose contents scroll vertically when they are too tall.

    Put child widgets inside ``self.interior`` (not in the ScrollableFrame
    itself).  Scrolling works with the scrollbar AND the mouse wheel.
    """
    
    def __init__(self, parent: tk.Misc, background: str ) -> None:
        super().__init__(parent)

        self._canvas = tk.Canvas(self, background=background, highlightthickness=0)
        self._scrollbar = ttk.Scrollbar(
            self, orient="vertical", command=self._canvas.yview
        )
        self._canvas.configure(yscrollcommand=self._scrollbar.set)

        self._scrollbar.pack(side="right", fill="y")
        self._canvas.pack(side="left", fill="both", expand=True)

        # The real content lives in a frame embedded inside the canvas.
        self.interior = tk.Frame(self._canvas, background=background)
        self._window_id = self._canvas.create_window(
            (0, 0), window=self.interior, anchor="nw"
        )

        # Keep the scroll region in step with the content size, and keep the
        # content as wide as the visible canvas.
        self.interior.bind("<Configure>", self._on_interior_resize)
        self._canvas.bind("<Configure>", self._on_canvas_resize)

        # Mouse-wheel is only captured while the pointer is over this widget,
        # so several scrollable areas could coexist.
        self.bind("<Enter>", self._bind_mousewheel)
        self.bind("<Leave>", self._unbind_mousewheel)

    # -- layout callbacks -------------------------------------------------
    def _on_interior_resize(self, _event: tk.Event) -> None:
        self._canvas.configure(scrollregion=self._canvas.bbox("all"))
        self._update_scrollbar_visibility()

    def _on_canvas_resize(self, event: tk.Event) -> None:
        self._canvas.itemconfigure(self._window_id, width=event.width)
        self._update_scrollbar_visibility()

    def _content_fits(self) -> bool:
        return self.interior.winfo_reqheight() <= self._canvas.winfo_height()

    def _update_scrollbar_visibility(self) -> None:
        """Hide the scrollbar when everything already fits on screen."""
        if self._content_fits():
            self._scrollbar.pack_forget()
            self._canvas.yview_moveto(0)
        elif not self._scrollbar.winfo_ismapped():
            # Re-pack on the right, before the canvas, to keep the layout.
            self._scrollbar.pack(side="right", fill="y", before=self._canvas)

    # -- mouse wheel ------------------------------------------------------
    def _bind_mousewheel(self, _event: tk.Event) -> None:
        # Windows & macOS send <MouseWheel>; X11/Linux sends Button-4/5.
        self.bind_all("<MouseWheel>", self._on_mousewheel)
        self.bind_all("<Button-4>", self._on_mousewheel)
        self.bind_all("<Button-5>", self._on_mousewheel)

    def _unbind_mousewheel(self, _event: tk.Event) -> None:
        self.unbind_all("<MouseWheel>")
        self.unbind_all("<Button-4>")
        self.unbind_all("<Button-5>")

    def _on_mousewheel(self, event: tk.Event) -> None:
        if self._content_fits():            # nothing to scroll
            return
        if event.num == 4:                       # Linux: wheel up
            step = -1
        elif event.num == 5:                     # Linux: wheel down
            step = 1
        elif sys.platform == "darwin":           # macOS: small deltas
            step = -event.delta
        else:                                    # Windows: multiples of 120
            step = -event.delta // 120
        self._canvas.yview_scroll(step, "units")


# ---------------------------------------------------------------------------
# The scrolling list of cards
# ---------------------------------------------------------------------------
class QuizListView(ScrollableFrame):
    """
    A scrollable column of :class:`QuizCard` widgets.
    """

    def __init__(self, parent: tk.Misc, theme: QuizTheme, on_select: Callable[[Questions], None],) -> None:
        
        self.theme = theme
        self.background_colour = theme.background_colour
        self.card_background_colour = theme.background_secondary_colour
        self.font_colour = theme.font_primary_colour
        self.subtext_colour = theme.font_secondary_colour
                            
        super().__init__(parent, background=self.background_colour)
        self._on_select = on_select

    def show(self, quizzes: List[Questions]) -> None:
        """
        Replace the current contents with one card per quiz.
        """
        for child in self.interior.winfo_children():
            child.destroy()

        if not quizzes:
            tk.Label(self.interior, text="No quizzes found.", font=("Segoe UI", 10), background=self.background_colour, foreground=self.subtext_colour).pack(pady=40)
            return

        for quiz in quizzes:
            card = QuizCard(self.interior, theme=self.theme, quiz=quiz, on_select=self._on_select)
            card.pack(fill="x", padx=16, pady=6)

            

# def do_something(questions: Questions):
#     print(f"--> done something - selected {questions.name}")

# if __name__ == "__main__":
#     from quizzer.QuizRepository import QuizRepository
#     from quizzer.QuizUtils import QuizUtils
    
#     theme = QuizUtils.load_theme()
#     print(f"loaded theme: {theme["name"]}")
    
#     repo = QuizRepository()
    
    
#     root = tk.Tk()
    
#     root.title("quiz cards")
#     # root.minsize = (300, 400)
#     # root.maxsize = (800, 1000)
#     root.geometry("600x800")

#     qv = QuizListView(root, theme, on_select=do_something)
#     qv.pack(expand=True, fill="both", padx=10, pady=10)
#     qv.show(repo.quizzes)
# #    qc = QuizCard(root, theme, repo.quizzes[0]).pack(fill="x", padx=10, pady=10)
    
# #    qc.pack(expand=True, fill=tk.BOTH, padx=10, pady=10)
#     root.mainloop()
    


# #on_select=self.open_quiz