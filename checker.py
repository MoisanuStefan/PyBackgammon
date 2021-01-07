import arcade

RED_CHECKER = "resources/sg_red_checker.png"
WHITE_CHECKER = "resources/sg_white_checker.png"

POINT_Y_OFFSET = 150
CHECKER_PILE_OFFSET = 50
CHECKER_RADIUS = 40
SCREEN_HEIGHT = 753



class Checker(arcade.Sprite):
    def __init__(self, color, scale):
        if color == 1:
            super().__init__(RED_CHECKER, scale=scale)
        if color == 0:
            super().__init__(WHITE_CHECKER, scale=scale)
        self.is_selectable = False
        self.is_dead = False
        self.colorr = color
        self.point = None

    def set_point(self, point):
        self.point = point

    def get_point(self):
        return self.point

    def remove(self):
        return self.point.remove_checker(self)

    def add(self, rolls, used_rolls):
        return self.point.add_checker(self, rolls, used_rolls)

    def place_back_to_origin(self, dead_checker_list):
        # if checker is dead
        if not self.is_dead:
            # get top checker and make it unselectable
            top_checker = self.point.get_top_checker()
            if top_checker:
                top_checker.is_selectable = False
            # add it back to point checker pile
            self.point.checker_pile.append(self)
        else:
            if len(dead_checker_list[self.colorr]) > 0:
                dead_checker_list[self.colorr][-1].is_selectable = False
            dead_checker_list[self.colorr].append(self)

