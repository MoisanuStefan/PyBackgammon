import arcade

GRAY = "resources/gray_point.png"
BLACK = "resources/black_point.png"

CHECKER_PILE_OFFSET = [60, 60, 60, 60, 60, 50, 45, 40, 35, 30, 25, 25, 25, 25, 25, 25, 25, 25]
SCREEN_HEIGHT = 753

FIRST_CHECKER_Y = [SCREEN_HEIGHT - 70, None, 70]


class Point(arcade.Sprite):
    """
    Point is a sprite that represents the triangles on which checkers sit

    ...
    Attributes
    ----------
    direction: int
        orientation of the point
    checker_color: int
        color of checkers on the point
    checker_pile: list()
        list of checkers on point
    id: int
        unique id


    Methods
    ----------
    get_top_checker()
        Returns checker on top of pile that can be moved
    add_checker()
        Adds a checker to the point and updates states of changed attributes
    remove_checker()
        Removes a checker from pile and updates states of changed attributes
    get_checker_destination()
        Returns the position where the next checker can be placed
    arrange_pile()
        Rearranges distance between checkers in a pile according to the number of checkers
      """

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
        """Returns checker on top of pile that can be moved"""
        for checker in self.checker_pile:
            if checker.is_selectable:
                return checker
        return None

    def add_checker(self, checker, cpu_move=False):
        """Adds a checker to the point and updates states of changed attributes"""
        dead_checker = None
        move_value = (self.id if checker.colorr == 0 else 25 - self.id) if checker.point is None else abs(
            checker.point.id - self.id)

        # if a checker gets killed
        if len(self.checker_pile) == 1 and self.checker_pile[0].colorr != checker.colorr:
            dead_checker = self.get_top_checker()
            dead_checker.point = None
            dead_checker.is_dead = True
            self.checker_pile.pop()
            self.checker_color = None

        # if checker moved to empty pile
        if self.checker_color is None:
            self.checker_color = checker.colorr
            # checker.position = self.center_x, FIRST_CHECKER_Y[self.direction + 1]
            checker.set_point(self)
            self.checker_pile.append(checker)
            checker.is_dead = False
        # if selected checker matches landing checker pile color
        else:
            # get top checker and make it unselectable
            top_checker = self.get_top_checker()
            top_checker.is_selectable = False
            self.checker_pile.append(checker)
            checker.set_point(self)
            checker.is_dead = False

        return checker, move_value, dead_checker

    def remove_checker(self, checker):
        """Removes a checker from pile and updates states of changed attributes"""
        tangent_checker = arcade.check_for_collision_with_list(checker, self.checker_pile)
        if len(tangent_checker) != 0:  # make tangent checker selectable
            tangent_checker[-1].is_selectable = True
        else:  # pile will be empty
            self.checker_color = None
        self.checker_pile.remove(checker)

    def get_checker_destination(self, checker):
        """Returns the position where the next checker can be placed"""
        # checker will be placed on empty point (initially or after it kills opponent checker)
        if self.checker_color is None or checker.colorr is not self.checker_color:
            position = self.center_x, FIRST_CHECKER_Y[self.direction + 1]
        else:
            position = list(self.get_top_checker().position)
            position[1] += self.direction * CHECKER_PILE_OFFSET[len(self.checker_pile) + 1]
        return position

    def arrange_pile(self, for_what):
        """Rearranges distance between checkers in a pile according to the number of checkers"""
        checker_count = len(self.checker_pile) + 1 if for_what == "add" else len(self.checker_pile) - 1
        for index, checker in enumerate(self.checker_pile):
            checker.position = self.center_x, FIRST_CHECKER_Y[self.direction + 1] + self.direction * index * \
                               CHECKER_PILE_OFFSET[checker_count]

