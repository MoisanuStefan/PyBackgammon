import arcade
from menu_view import MenuView

SCREEN_WIDTH = 1452
SCREEN_HEIGHT = 753
SCREEN_TITLE = "StefGammon"

if __name__ == "__main__":
    window = arcade.Window(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    window.set_location(-1500, -50)
    start_view = MenuView()
    window.show_view(start_view)
    arcade.run()
