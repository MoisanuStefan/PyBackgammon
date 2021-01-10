import arcade

SCREEN_WIDTH = 1452
SCREEN_HEIGHT = 753
BOARD_WIDTH = 1052


class MenuView(arcade.View):
    """
    View where user chooses game mode: PvP, or CPUvP

    """

    def on_draw(self):
        """ Draw the menu """
        arcade.start_render()
        arcade.draw_lrwh_rectangle_textured(200, 0, BOARD_WIDTH, SCREEN_HEIGHT,
                                            arcade.load_texture("resources/sg_board.png"))
        arcade.draw_lrwh_rectangle_textured(0, 0, 200, SCREEN_HEIGHT, arcade.load_texture("resources/sg_side_l.png"))
        arcade.draw_lrwh_rectangle_textured(1252, 0, 200, SCREEN_HEIGHT, arcade.load_texture("resources/sg_side_r.png"))
        arcade.draw_line(SCREEN_WIDTH / 2, SCREEN_HEIGHT, SCREEN_WIDTH / 2, 0, arcade.color.BLACK, 1)
        arcade.draw_text("Brain", SCREEN_WIDTH / 2 - BOARD_WIDTH / 4, SCREEN_HEIGHT / 2,
                         arcade.color.BLACK, font_size=30, anchor_x="center", )
        arcade.draw_text("CPU", SCREEN_WIDTH / 2 + BOARD_WIDTH / 4, SCREEN_HEIGHT / 2,
                         arcade.color.BLACK, font_size=30, anchor_x="center")
        arcade.draw_text("Choose opponent's processing unit", SCREEN_WIDTH / 2, 17, color=arcade.color.WHITE,
                         font_size=20,
                         anchor_x="center",
                         anchor_y="center")

    def on_mouse_press(self, x, y, button, modifiers):
        """ Use a mouse press to advance to the 'player' view. """
        from player_view import PlayerView
        if x < SCREEN_WIDTH / 2:
            player_view = PlayerView(False)
        else:
            player_view = PlayerView(True)
        self.window.show_view(player_view)
