import arcade
from game_view import StefGammon

SCREEN_WIDTH = 1452
SCREEN_HEIGHT = 753
BOARD_WIDTH = 1052
PLAYER_STAT_WIDTH = (SCREEN_WIDTH - BOARD_WIDTH) / 2


class PlayerView(arcade.View):
    """
    View in which user chooses an avatar

    ...
    Attributes
    ----------
    is_cpu_game: bool
        If game is played against cpu
    red_avatar: Sprite
        Avatar of red player
    white_avatar Sprite
        Avatar of white player
    player_avatars: List
        List of available avatars

    """
    def __init__(self, is_cpu_game):
        super().__init__()
        # if is_CPU_game:
        self.is_cpu_game = is_cpu_game
        if not self.is_cpu_game:
            self.avatar_images = [
                ["resources/avatar_r_stef.png", "resources/avatar_r_cos.png", "resources/avatar_r_carol.png"],
                ["resources/avatar_w_stef.png", "resources/avatar_w_cos.png", "resources/avatar_w_carol.png"]]
        else:
            self.avatar_images = [[], ["resources/avatar_w_stef.png", "resources/avatar_w_cos.png",
                                       "resources/avatar_w_carol.png"]]
        self.red_avatar = None
        self.white_avatar = None
        self.player_avatars = arcade.SpriteList()

    def on_show(self):
        if self.is_cpu_game:
            avatar = arcade.Sprite("resources/avatar_cpu.png")
            avatar.position = PLAYER_STAT_WIDTH / 2, SCREEN_HEIGHT / 2
            self.player_avatars.append(avatar)
        else:
            for index, player_image in enumerate(self.avatar_images[0]):
                avatar = arcade.Sprite(player_image)
                avatar.position = PLAYER_STAT_WIDTH / 2, (index + 1) * SCREEN_HEIGHT / 4
                self.player_avatars.append(avatar)

        for index, player_image in enumerate(self.avatar_images[1]):
            avatar = arcade.Sprite(player_image)
            avatar.position = SCREEN_WIDTH - PLAYER_STAT_WIDTH / 2, (index + 1) * SCREEN_HEIGHT / 4
            self.player_avatars.append(avatar)

    def on_draw(self):
        """ Draw the menu """
        arcade.start_render()
        arcade.draw_lrwh_rectangle_textured(200, 0, BOARD_WIDTH, SCREEN_HEIGHT,
                                            arcade.load_texture("resources/sg_board.png"))
        arcade.draw_lrwh_rectangle_textured(0, 0, 200, SCREEN_HEIGHT, arcade.load_texture("resources/sg_side_l.png"))
        arcade.draw_lrwh_rectangle_textured(1252, 0, 200, SCREEN_HEIGHT, arcade.load_texture("resources/sg_side_r.png"))
        arcade.draw_line(SCREEN_WIDTH / 2, SCREEN_HEIGHT, SCREEN_WIDTH / 2, 0, arcade.color.BLACK, 1)
        self.player_avatars.draw()
        arcade.draw_text("Choose player avatar", SCREEN_WIDTH / 2, 17, color=arcade.color.WHITE, font_size=20,
                         anchor_x="center",
                         anchor_y="center")

    def on_mouse_press(self, x, y, button, modifiers):
        """ Use a mouse press to advance to the 'game' view. """
        avatar = arcade.get_sprites_at_point((x, y), self.player_avatars)[0]
        if not self.is_cpu_game:
            if avatar.center_x == PLAYER_STAT_WIDTH / 2:
                self.red_avatar = avatar
            if avatar.center_x == SCREEN_WIDTH - PLAYER_STAT_WIDTH / 2:
                self.white_avatar = avatar
        else:
            self.red_avatar = self.player_avatars[0]
            if avatar.center_x == SCREEN_WIDTH - PLAYER_STAT_WIDTH / 2:
                self.white_avatar = avatar

        if self.red_avatar is not None and self.white_avatar is not None:
            stef_gammon = StefGammon(self.is_cpu_game, self.red_avatar, self.white_avatar)
            self.window.show_view(stef_gammon)
            stef_gammon.setup()