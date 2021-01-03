import arcade

RED_CHECKER = "resources/sg_red_checker.png"
WHITE_CHECKER = "resources/sg_white_checker.png"

POINT_Y_OFFSET = 150
CHECKER_PILE_OFFSET = 50
CHECKER_RADIUS = 40

class Checker(arcade.Sprite):
    def __init__(self, color, scale):
        if color == 1:
            super().__init__(RED_CHECKER, scale=scale)
        if color == 0:
            super().__init__(WHITE_CHECKER, scale=scale)
        self.is_selectable = False
        self.colorr = color
        self.point = None

    def set_point(self, point):
        self.point = point

    def get_point(self):
        return self.point

    def remove(self, turn):
        return self.point.remove_checker(self, turn)

    def add(self, rolls, used_rolls):
        return self.point.add_checker(self, rolls, used_rolls)

    def place_back_to_origin(self):
        # get top checker and make it unselectable
        top_checker = self.point.get_top_checker()
        if top_checker:
            top_checker.is_selectable = False
            # put new top checker in place
        self.center_x = self.point.center_x
        self.center_y = self.point.center_y - self.point.direction * POINT_Y_OFFSET + self.point.direction * (CHECKER_RADIUS + CHECKER_PILE_OFFSET * len(self.point.checker_pile))
        # add it back to point checker pile
        self.point.checker_pile.append(self)
