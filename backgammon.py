import arcade
from checker import Checker
from point import Point
from dice import Dice
from arcade.gui import UIManager

DICE_WIDTH = 50
SCREEN_WIDTH = 1452
SCREEN_HEIGHT = 753
BOARD_WIDTH = 1052
PLAYER_STAT_WIDTH = (SCREEN_WIDTH - BOARD_WIDTH) / 2
SCREEN_TITLE = "StefGammon"
CHECKER_RADIUS = 35

POINT_Y_OFFSET = 150
POINT_X_OFFSET = 35
POINTS_POSITIONS = [[30, 219], [30, 301], [30, 387], [30, 470], [30, 556], [30, 641],
                    [30, 737], [30, 821], [30, 905], [30, 987], [30, 1073], [30, 1160]]
CHECKER_POSITIONS = [[70, 254], [70, 590], [70, 772], [70, 1192]]
CHECKER_COLORS = (1, 0, 0, 1)
CHECKER_PILES = (6, 3, 6, 2)
CHECKER_PILE_OFFSET = 50


# transform point lower_left corner position to point center position by adding offset
def offset_points_positions(points_positions):
    for index in range(len(points_positions)):
        points_positions[index][1] += POINT_X_OFFSET
        points_positions[index][0] += POINT_Y_OFFSET


# to do: set points in their position, set checkers in position
class StefGammon(arcade.View):
    def __init__(self):
        super().__init__()
        self.ui_manager = UIManager()
        self.background_image = None
        self.background_left = None
        self.background_right = None
        self.checker_list = arcade.SpriteList()
        self.point_list = arcade.SpriteList()
        self.selected_checker = None
        self.selected_checker_origin = None
        self.turn = None
        self.dice = Dice()
        self.game_state = "before_choose_turns"
        self.dice_rolled_for_turns = False
        self.white_roll = None
        self.red_roll = None
        self.turn = None
        self.rolls = []
        self.used_rolls = []
        self.tick_pressed = None

        self.choose_turns_button = None
        self.dice_faces = []
        self.red_begins_button = None
        self.white_begins_button = None
        self.roll_again_button = None
        self.ok_button = None
        self.tick_button = None

    def setup(self):
        """ Set up the game here. Call this function to restart the game. """

        self.background_image = arcade.load_texture("resources/sg_board.png")
        self.background_left = arcade.load_texture("resources/sg_side_l.png")
        self.background_right = arcade.load_texture("resources/sg_side_r.png")
        self.dice.load_textures()

        self.choose_turns_button = arcade.load_texture("resources/choose_turns_button.png")
        self.white_begins_button = arcade.load_texture("resources/white_begins_button.png")
        self.red_begins_button = arcade.load_texture("resources/red_begins_button.png")
        self.roll_again_button = arcade.load_texture("resources/roll_again_button.png")
        self.tick_button = arcade.load_texture("resources/tick_button.png")

        self.tick_pressed = False
        POINTS_POSITIONS.reverse()
        self.set_points()
        self.set_checkers()
        # right side elements
        # button = MyFlatButton('choose_turns', 'Choose Turns', 726, 376, 250, self.game, self.ui_manager)
        # self.ui_manager.add_ui_element(button)

    def on_draw(self):
        """ Render the screen. """
        # Clear the screen
        arcade.start_render()
        arcade.draw_lrwh_rectangle_textured(200, 0, BOARD_WIDTH, SCREEN_HEIGHT, self.background_image)
        arcade.draw_lrwh_rectangle_textured(0, 0, 200, SCREEN_HEIGHT, self.background_left)

        arcade.draw_lrwh_rectangle_textured(1252, 0, 200, SCREEN_HEIGHT, self.background_right)
        self.checker_list.draw()
        if self.game_state == "before_choose_turns":
            arcade.draw_texture_rectangle(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2, 200, 50, self.choose_turns_button)
        elif self.game_state == "choosing_turns":
            arcade.draw_texture_rectangle(SCREEN_WIDTH / 2 - BOARD_WIDTH / 4, SCREEN_HEIGHT / 2, 50, 50,
                                          self.dice.get_face(self.red_roll))
            arcade.draw_texture_rectangle(SCREEN_WIDTH / 2 + BOARD_WIDTH / 4, SCREEN_HEIGHT / 2, 50, 50,
                                          self.dice.get_face(self.white_roll))
            if self.white_roll == self.red_roll:
                arcade.draw_texture_rectangle(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2, 200, 50, self.roll_again_button)
            elif self.white_roll > self.red_roll:
                arcade.draw_texture_rectangle(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2, 200, 50, self.white_begins_button)
            else:
                arcade.draw_texture_rectangle(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2, 200, 50, self.red_begins_button)
        elif self.game_state == "started":
            if self.turn == 0:
                arcade.draw_texture_rectangle(SCREEN_WIDTH - PLAYER_STAT_WIDTH / 2, SCREEN_HEIGHT / 2, 70, 70, self.tick_button)
                arcade.draw_texture_rectangle(
                    SCREEN_WIDTH - PLAYER_STAT_WIDTH - BOARD_WIDTH / 4 - DICE_WIDTH / 2 - 5,
                    SCREEN_HEIGHT / 2, 50, 50, self.dice.get_face(self.rolls[0]))
                arcade.draw_texture_rectangle(
                    SCREEN_WIDTH - PLAYER_STAT_WIDTH - BOARD_WIDTH / 4 + DICE_WIDTH / 2 + 5,
                    SCREEN_HEIGHT / 2, 50, 50, self.dice.get_face(self.rolls[1]))
            else:
                arcade.draw_texture_rectangle(PLAYER_STAT_WIDTH / 2, SCREEN_HEIGHT / 2, 70, 70, self.tick_button)
                arcade.draw_texture_rectangle(
                    PLAYER_STAT_WIDTH + BOARD_WIDTH / 4 - DICE_WIDTH / 2 - 5,
                    SCREEN_HEIGHT / 2, 50, 50, self.dice.get_face(self.rolls[0]))
                arcade.draw_texture_rectangle(
                    PLAYER_STAT_WIDTH + BOARD_WIDTH / 4 + DICE_WIDTH / 2 + 5,
                    SCREEN_HEIGHT / 2, 50, 50, self.dice.get_face(self.rolls[1]))


    def on_mouse_press(self, x, y, button, key_modifiers):
        """ Called when the user presses a mouse button. """
        print("x: ", x, "\ny: ", y)
        if self.game_state == "before_choose_turns":
            if SCREEN_WIDTH / 2 - 100 <= x <= SCREEN_WIDTH / 2 + 100 and SCREEN_HEIGHT / 2 - 25 <= y <= SCREEN_HEIGHT / 2 + 25:
                self.game_state = "choosing_turns"
                self.white_roll = self.dice.roll()
                self.red_roll = self.dice.roll()

        elif self.game_state == "choosing_turns":
            if SCREEN_WIDTH / 2 - 100 <= x <= SCREEN_WIDTH / 2 + 100 and SCREEN_HEIGHT / 2 - 25 <= y <= SCREEN_HEIGHT / 2 + 25:
                if self.white_roll != self.red_roll:
                    self.game_state = "started"
                    self.rolls = self.dice.double_roll()
                    if self.white_roll > self.red_roll:
                        self.turn = 0
                    else:
                        self.turn = 1
                else:
                    self.white_roll = self.dice.roll()
                    self.red_roll = self.dice.roll()

        elif self.game_state == "started":
            if len(self.used_rolls) == 2:
            # press on tick button at white turn
                if 0 <= SCREEN_WIDTH / 2 + BOARD_WIDTH / 2 + PLAYER_STAT_WIDTH / 2 + 35 - x <= 70 and 0 <= SCREEN_HEIGHT / 2 + 35 - y <= 70 and self.turn == 0:
                    self.rolls = self.dice.double_roll()
                    self.turn = 1 - self.turn
                if 0 <= PLAYER_STAT_WIDTH / 2 + 35 - x <= 70 and 0 <= SCREEN_HEIGHT / 2 + 35 - y <= 70 and self.turn == 1:
                    self.rolls = self.dice.double_roll()
                    self.turn = 1 - self.turn

            clicked_checkers = arcade.get_sprites_at_point((x, y), self.checker_list)
            for checker in clicked_checkers:
                self.selected_checker_origin = checker.remove(self.turn)
                if self.selected_checker_origin:
                    self.bring_sprite_to_front(checker)
                    self.selected_checker = checker
                    break

    def on_mouse_release(self, x: float, y: float, button: int,
                         modifiers: int):
        """ Called when the user presses a mouse button. """
        if self.game_state == "started":
            if self.selected_checker is not None:
                closest_point, dist = arcade.get_closest_sprite(self.selected_checker, self.point_list)
                # if self.is_valid_move(self.selected_checker, closest_point):
                placed_checker, used_roll = closest_point.add_checker(self.selected_checker, self.rolls, self.used_rolls)
                if placed_checker:
                    self.selected_checker.position = placed_checker.position
                    self.used_rolls.append(used_roll)
                    self.selected_checker = None
                else:
                    self.selected_checker.place_back_to_origin()
                    self.selected_checker = None

    def on_mouse_motion(self, x: float, y: float, dx: float, dy: float):
        """ User moves mouse """
        if self.game_state == "started":
            if self.selected_checker is not None:
                self.selected_checker.center_x += dx
                self.selected_checker.center_y += dy

    def set_points(self):
        offset_points_positions(POINTS_POSITIONS)
        color = 1  # red
        id = 1
        for y, x in POINTS_POSITIONS:
            point = Point(color, 25-id)
            point.position = x, y
            point.direction = 1
            self.point_list.append(point)
            point = Point(1 - color, id, True)
            id += 1
            point.position = x, SCREEN_HEIGHT - y
            point.direction = -1
            self.point_list.append(point)
            color = 1 - color

    def set_checkers(self):
        for index, (y, x) in enumerate(CHECKER_POSITIONS):
            point_low = arcade.get_sprites_at_point((x, y), self.point_list)[0]
            point_low.checker_color = CHECKER_COLORS[index]
            point_top = arcade.get_sprites_at_point((x, SCREEN_HEIGHT - y), self.point_list)[0]
            point_top.checker_color = 1 - CHECKER_COLORS[index]
            for checker_count in range(CHECKER_PILES[index]):
                checker = Checker(CHECKER_COLORS[index], 1)
                checker.position = x, y + checker_count * CHECKER_PILE_OFFSET
                checker.point = point_low
                if CHECKER_PILES[index] == checker_count + 1:
                    checker.is_selectable = True
                point_low.checker_pile.append(checker)
                self.checker_list.append(checker)
                checker = Checker(1 - CHECKER_COLORS[index], 1)
                checker.position = x, SCREEN_HEIGHT - y - checker_count * CHECKER_PILE_OFFSET
                checker.point = point_top
                if CHECKER_PILES[index] == checker_count + 1:
                    checker.is_selectable = True
                point_top.checker_pile.append(checker)
                self.checker_list.append(checker)

    def bring_sprite_to_front(self, sprite):
        if isinstance(sprite, Checker):
            self.checker_list.remove(sprite)
            self.checker_list.append(sprite)
            self.checker_list.draw()

    def checker_moved_forward(self, checker, point):
        pass

    def is_valid_move(self, checker, point):
        if not checker.is_selectable:
            return 'not_selectable'


def main():
    window = arcade.Window(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    window.set_location(30, 30)
    start_view = StefGammon()
    window.show_view(start_view)
    start_view.setup()
    arcade.run()


if __name__ == "__main__":
    main()
