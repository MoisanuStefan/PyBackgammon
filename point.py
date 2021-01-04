import arcade

GRAY = "resources/gray_point.png"
BLACK = "resources/black_point.png"

CHECKER_PILE_OFFSET = 50
FIRST_CHECKER_Y = 70

SCREEN_HEIGHT = 753


class Point(arcade.Sprite):
    def __init__(self, color, idd, flipped=False):
        if color == 1:
            super().__init__(GRAY, flipped_vertically=flipped)
        if color == 0:
            super().__init__(BLACK, flipped_vertically=flipped)
        self.direction = -1 if flipped else 1
        self.checker_color = None
        self.checker_pile = arcade.SpriteList()
        self.id = idd

    def get_top_checker(self):
        for checker in self.checker_pile:
            if checker.is_selectable:
                return checker
        return None

    def add_checker(self, checker,rolls, used_rolls):
        dead_checker = None
        move_value = (self.id if checker.colorr == 0 else 25 - self.id) if checker.point is None else abs(
            checker.point.id - self.id)

        # if move_value not in rolls:
        #     return False, None, None
        # if len(rolls) == 2 and move_value in used_rolls:
        #     return False, None, None

        # if checker is in play (not dead) => verify if move is valid
        if checker.point is not None:
            move_value = abs(checker.point.id - self.id)

            if checker.colorr == 0 and self.id - checker.point.id < 0:
                return False, None, None
            if checker.colorr == 1 and self.id - checker.point.id > 0:
                return False, None, None
        # if checker is dead
        else:
            # if dead checker placed outside house
            if move_value > 6:
                return False, None, None

        if len(self.checker_pile) == 1 and self.checker_pile[0].colorr != checker.colorr:
            dead_checker = self.get_top_checker()
            dead_checker.point = None
            self.checker_pile.pop()
            self.checker_color = None

        # if checker moved to empty pile
        if self.checker_color is None:
            self.checker_color = checker.colorr
            if self.direction == 1:
                checker.position = self.center_x, FIRST_CHECKER_Y
            else:
                checker.position = self.center_x, SCREEN_HEIGHT - FIRST_CHECKER_Y
            checker.set_point(self)
            self.checker_pile.append(checker)
            return checker, move_value, dead_checker
        # if selected checker matches landing checker pile color
        elif checker.colorr == self.checker_color:
            # get top checker and make it unselectable
            top_checker = self.get_top_checker()
            top_checker.is_selectable = False
            # put new top checker in place
            checker.center_x = top_checker.center_x
            checker.center_y = top_checker.center_y + self.direction * CHECKER_PILE_OFFSET
            # add it to point checker pile
            checker.set_point(self)
            self.checker_pile.append(checker)
            return checker, move_value, dead_checker

        return False, None, None

    def remove_checker(self, checker, turn):
        if not checker.is_selectable or checker.colorr != turn:
            return False
        tangent_checker = arcade.check_for_collision_with_list(checker, self.checker_pile)
        if len(tangent_checker) != 0:  # make tangent checker selectable
            tangent_checker[0].is_selectable = True
        else:  # pile will be empty
            self.checker_color = None
        self.checker_pile.remove(checker)
        return True


