class DrawingUtils:
    
    
    @staticmethod
    def rounded_rect_points(x1: int, y1: int, x2: int, y2: int, r: int) -> list[int]:
        """Draw a rounded rectangle.

        Trick: a polygon with ``smooth=True`` rounds off its corners; listing
        each corner point twice makes the curves tight instead of bulging.
        """
        r = min(r, (x2 - x1) // 2, (y2 - y1) // 2)
        return [
            x1 + r, y1,  x1 + r, y1,  x2 - r, y1,  x2 - r, y1,
            x2, y1,      x2, y1 + r,  x2, y1 + r,  x2, y2 - r,
            x2, y2 - r,  x2, y2,      x2 - r, y2,  x2 - r, y2,
            x1 + r, y2,  x1 + r, y2,  x1, y2,      x1, y2 - r,
            x1, y2 - r,  x1, y1 + r,  x1, y1 + r,  x1, y1,
        ]

        # return self.create_polygon(
        #     points,
        #     smooth=True,
        #     fill=self._fill,
        #     outline=Theme.CARD_BORDER,
        #     width=Theme.CARD_BORDER_WIDTH,
        # )
