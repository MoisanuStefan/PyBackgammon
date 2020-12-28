import arcade

RED_CHECKER = "resources/sg_red_checker.png"
WHITE_CHECKER = "resources/sg_white_checker.png"


class Checker(arcade.Sprite):
    def __init__(self, color, scale):
        if color == 1:
            super().__init__(RED_CHECKER, scale=scale)
        if color == 0:
            super().__init__(WHITE_CHECKER, scale=scale)
