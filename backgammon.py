import arcade
from checker import Checker
from point import Point

SCREEN_WIDTH = 1452
SCREEN_HEIGHT = 753
BOARD_WIDTH = 1052
SCREEN_TITLE = "StefGammon"
CHECKER_RADIUS = 35


POINT_Y_OFFSET = 150
POINT_X_OFFSET = 35
POINTS_POSITIONS = [[30, 219], [30, 301], [30, 387], [30, 470], [30, 556], [30, 641],
                    [30, 737], [30, 821], [30, 905], [30, 987], [30, 1073], [30, 1160]]
CHECKER_POSITIONS = [[70, 254], [70,590], [70,772], [70,1192]]
CHECKER_COLORS = (1,0,0,1)
CHECKER_PILES = (6,3,6,2)
CHECKER_PILE_OFFSET = 50



# transform point lower_left corner position to point center position by adding offset
def offset_points_positions(points_positions):
    for index in range(len(points_positions)):
        points_positions[index][1] += POINT_X_OFFSET
        points_positions[index][0] += POINT_Y_OFFSET


# to do: set points in their position, set checkers in position
class StefGammon(arcade.Window):
    def __init__(self):
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
        self.set_location(30, 30)
        self.background_image = None
        self.background_left = None
        self.background_right = None
        self.checker_list = arcade.SpriteList()
        self.point_list = arcade.SpriteList()

    def setup(self):
        """ Set up the game here. Call this function to restart the game. """

        self.background_image = arcade.load_texture("resources/sg_board.png")
        self.background_left = arcade.load_texture("resources/sg_side_l.png")
        self.background_right = arcade.load_texture("resources/sg_side_r.png")
        self.set_points()
        self.set_checkers()



    def on_draw(self):
        """ Render the screen. """
        # Clear the screen
        arcade.start_render()
        arcade.draw_lrwh_rectangle_textured(200, 0, BOARD_WIDTH, SCREEN_HEIGHT, self.background_image)
        arcade.draw_lrwh_rectangle_textured(0, 0, 200, SCREEN_HEIGHT, self.background_left)

        arcade.draw_lrwh_rectangle_textured(1252, 0, 200, SCREEN_HEIGHT, self.background_right)
        self.checker_list.draw()
        # self.point_list.draw()

    def on_mouse_press(self, x, y, button, key_modifiers):
        """ Called when the user presses a mouse button. """
        print("x: ", x, "\ny: ", y)
        if arcade.check_for_collision_with_list(self.point_list[0], self.checker_list):
            print(True)

    def on_mouse_release(self, x: float, y: float, button: int,
                         modifiers: int):
        """ Called when the user presses a mouse button. """
        pass

    def on_mouse_motion(self, x: float, y: float, dx: float, dy: float):
        """ User moves mouse """
        pass

    def set_points(self):
        offset_points_positions(POINTS_POSITIONS)
        color = 1  # gray
        for y, x in POINTS_POSITIONS:
            point = Point(color)
            point.position = x, y
            self.point_list.append(point)
            point = Point(1 - color, True)
            point.position = x, SCREEN_HEIGHT - y
            self.point_list.append(point)
            color = 1 - color
    def set_checkers(self):
        for index, (y, x) in enumerate(CHECKER_POSITIONS):
            for checker_count in range(CHECKER_PILES[index]):
                checker = Checker(CHECKER_COLORS[index], 1)
                checker.position = x, y + checker_count * CHECKER_PILE_OFFSET
                self.checker_list.append(checker)
                checker = Checker(1 - CHECKER_COLORS[index], 1)
                checker.position = x, SCREEN_HEIGHT - y - checker_count * CHECKER_PILE_OFFSET
                self.checker_list.append(checker)

def main():
    game = StefGammon()
    game.setup()
    arcade.run()


if __name__ == "__main__":
    main()
