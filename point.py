import arcade

GRAY = "resources/gray_point.png"
BLACK = "resources/black_point.png"


class Point(arcade.Sprite):
    def __init__(self, color, flipped=False):
        if color == 1:
            super().__init__(GRAY, flipped_vertically=flipped)
        if color == 0:
            super().__init__(BLACK, flipped_vertically=flipped)
