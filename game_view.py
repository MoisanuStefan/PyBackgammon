import random
from time import sleep
from menu_view import MenuView
import arcade
from checker import Checker
from point import Point
from dice import Dice

DICE_WIDTH = 50
SCREEN_WIDTH = 1452
SCREEN_HEIGHT = 753
BOARD_WIDTH = 1052
PLAYER_STAT_WIDTH = (SCREEN_WIDTH - BOARD_WIDTH) / 2
SCREEN_TITLE = "StefGammon"
CHECKER_RADIUS = 35
CHECKER_SPEED = 1
FIRST_CHECKER_Y = [SCREEN_HEIGHT - 70, None, 70]

BEAR_OFF_BEGIN_Y = 20
BEAR_OFF_CHECKER_HEIGHT = 15
DICE_X = [-DICE_WIDTH / 2 - 5, DICE_WIDTH / 2 + 5, - 3 * DICE_WIDTH / 2 - 15, 3 * DICE_WIDTH / 2 + 15]
POINTS_POSITIONS = [[180, 1195], [180, 1108], [180, 1022], [180, 940], [180, 856], [180, 772], [180, 676], [180, 591],
                    [180, 505], [180, 422], [180, 336], [180, 254]]
CHECKER_POSITIONS = [[70, 254], [70, 590], [70, 772], [70, 1192]]
CHECKER_COLORS = (1, 0, 0, 1)
CHECKER_PILES = (6, 3, 6, 2)
CHECKER_PILE_OFFSET = [0, 60, 60, 60, 60, 50, 45, 40, 35, 30, 25]

DEAD_CHECKER_PILE_DIRECTION = [1, -1]
BOTTOM_MSG_TIME = 100


def list_difference(li1, li2):
    """Returns the elements in first list that are not in second list"""
    list = []
    if len(li1) == 4:
        for count in range(4 - len(li2)):
            list.append(li1[0])
        return list
    else:
        return [i for i in li1 if i not in li2]


# to do: set points in their position, set checkers in position
class StefGammon(arcade.View):
    """

    ...
    Atributes
    ---------
    animation_iteration: int
        Keeps track of checker movement animation frames
    is_cpu_game: bool
        Informs if the game is played against cpu
    background_image: str
        Image resource for play board
    background_left:
        Image resource for left player stats background
    background_right:
        Image resource for right player stats background
    red_begins_button:
        Image resource for button displayed when red begins
    white_begins_button:
        Image resource for button displayed when white begins
    roll_again_button:
        Image resource for button displayed when rolls coincide
    tick_button:
        Image resource for button that ends player turn
    bear_off_table:
        Image resource for the place where beard off checkers go
    main_menu:
        Image resource for button that loads menu view
    play_again:
        Image resource for button that resets the game
    choose_turns_button: str
        Image resource for button that initiates turn choosing
    checker_list:
        List with all checkers in play
    point_list:
        List of all points on table
    dead_checker_list:
        List of checkers that have been removed from play and wait to be reentered
    selected_checker:
        Checker currently being interacted with
    selected_checker_origin:
        Position of selected_checker
    turn:
        Player id of who is moving
    dice: Dice
        Object that simulates a dice
    game_state: str
        A string that defines the state of the game
    white_roll: int
        Beginning roll for white player
    red_roll: int
        Beginning roll for red player
    rolls: List
        List of all rolls for current turn
    used_rolls: List
        List of all rolls that were previously used in the current turn
    beared_off_white: str
        Image resource for checker in beared off pile
    beared_off_red: str
        Image resource for checker in beared off pile
    nr_of_beared_off: List
        Number of beared off checkers for each player
    selected_checker_destination: List
        Position of selected checker destination
    checker_state: str
        String that informs what operation was performed on a checker: remove, add, missplaced
    dead_checker_origin: List
        Position of top checker of removed checker pile
    dead_rolls: List
        List of rolls that no checker can move
    current_roll:
        Roll that was used for current move
    winner: bool
        Id of winner
    player_can_move: bool
        Informs if a player has any moves left
    score: List
        Score of each player
    bottom_message: str
        Message to be displayed in the hint bar
    bottom_message_time:
        Duration of message in frames
    red_avatar: Sprite
        Image representing a player
    white_avatar: Sprite
        Image representing a player


    Methods
    -------
    setup():
        Called to set/reset the game
    on_draw():
        Renders the screen
    on_update():
        Called every frame
    on_mouse_press()
        Called when the user presses a mouse button
    on_mouse_release()
        Called when the user releases a mouse button
    place_selected_checker()
        Adds a checker to it's destination checker pile depending on it's state:
        moved, missplaced, bear off
    set_selected_checker()
        Removes a checker from it's pile and sets the selected checker attribute
    get_bear_off_destination()
        Returns position of next checker to be added to bear off pile
    valid_move_exists()
        Determines if a player still has available moves
    is_valid_move()
        Determines if a move is valid
    on_mouse_motion()
        Called when user moves mouse
    set_points()
        Creates all point objects and sets them to their positions
    set_checkers()
        Creates all checkers and places them in their initial positions
    bring_sprite_to front()
        Brings a sprite to the top of the list in order to be rendered on top
    ready_for_bearoff()
        Determines if a player is allowed to bear off checkers
    """

    def __init__(self, is_cpu_game, red_avatar, white_avatar):
        super().__init__()
        self.animation_iteration = None
        self.is_cpu_game = is_cpu_game
        self.background_image = None
        self.background_left = None
        self.background_right = None
        self.main_menu = None
        self.play_again = None
        self.checker_list = None
        self.point_list = None
        self.dead_checker_list = None
        self.selected_checker = None
        self.selected_checker_origin = None
        self.turn = None
        self.dice = Dice()
        self.game_state = None
        self.white_roll = None
        self.red_roll = None
        self.rolls = None
        self.used_rolls = None
        self.choose_turns_button = None
        self.red_begins_button = None
        self.white_begins_button = None
        self.roll_again_button = None
        self.tick_button = None
        self.beared_off_white = None
        self.beared_off_red = None
        self.nr_of_beared_off = None
        self.bear_off_table = None
        self.selected_checker_destination = None
        self.checker_state = None
        self.dead_checker_origin = None
        self.dead_rolls = None
        self.current_roll = None
        self.winner = None
        self.player_can_move = None
        self.score = [0, 0]
        self.bottom_message = None
        self.bottom_message_time = None
        self.red_avatar = red_avatar
        self.white_avatar = white_avatar

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
        self.beared_off_white = arcade.load_texture("resources/beared_off_white.png")
        self.beared_off_red = arcade.load_texture("resources/beared_off_red.png")
        self.bear_off_table = arcade.load_texture("resources/beare_off_table.png")
        self.main_menu = arcade.load_texture("resources/main_menu_button.png")
        self.play_again = arcade.load_texture("resources/play_again_button.png")

        self.checker_list = arcade.SpriteList()
        self.point_list = arcade.SpriteList()
        self.dead_checker_list = [arcade.SpriteList(), arcade.SpriteList()]
        self.dead_checker_list = [[], []]
        self.rolls = []
        self.used_rolls = []
        self.nr_of_beared_off = [0, 0]
        self.set_points()
        self.set_checkers()
        self.animation_iteration = 0
        self.selected_checker_destination = None
        self.selected_checker_origin = None
        self.checker_state = None
        self.dead_checker_origin = None
        self.dead_rolls = []
        self.winner = None
        self.selected_checker = None
        self.game_state = "before_choose_turns"
        self.player_can_move = True
        self.bottom_message = ""
        self.bottom_message_time = 0

        self.red_avatar.center_y = SCREEN_HEIGHT - 100
        self.white_avatar.center_y = SCREEN_HEIGHT - 100



    def on_draw(self):
        """ Render the screen. """
        arcade.start_render()
        arcade.draw_lrwh_rectangle_textured(200, 0, BOARD_WIDTH, SCREEN_HEIGHT, self.background_image)
        arcade.draw_lrwh_rectangle_textured(0, 0, 200, SCREEN_HEIGHT, self.background_left)

        arcade.draw_lrwh_rectangle_textured(1252, 0, 200, SCREEN_HEIGHT, self.background_right)
        arcade.draw_texture_rectangle(SCREEN_WIDTH - PLAYER_STAT_WIDTH / 4,
                                      BEAR_OFF_BEGIN_Y - BEAR_OFF_CHECKER_HEIGHT / 2 + 287 / 2, 90, 307,
                                      self.bear_off_table)
        arcade.draw_texture_rectangle(PLAYER_STAT_WIDTH / 4, BEAR_OFF_BEGIN_Y - BEAR_OFF_CHECKER_HEIGHT / 2 + 287 / 2,
                                      90, 307, self.bear_off_table)
        arcade.draw_text(str(self.score[0]), SCREEN_WIDTH - PLAYER_STAT_WIDTH / 2, 480, arcade.color.WHITE_SMOKE,
                         anchor_x="center", anchor_y="center", font_size=40)
        arcade.draw_text(str(self.score[1]), PLAYER_STAT_WIDTH / 2, 480, arcade.color.WHITE, anchor_x="center",
                         anchor_y="center", font_size=40)
        self.red_avatar.draw()
        self.white_avatar.draw()
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
            # tick buttons
            if self.turn == 0:
                arcade.draw_texture_rectangle(SCREEN_WIDTH - PLAYER_STAT_WIDTH / 2, SCREEN_HEIGHT / 2, 70, 70,
                                              self.tick_button)
            elif not self.is_cpu_game:
                arcade.draw_texture_rectangle(PLAYER_STAT_WIDTH / 2, SCREEN_HEIGHT / 2, 70, 70, self.tick_button)

            # dice
            sign = -1
            not_used_rolls = list_difference(self.rolls, self.used_rolls)
            for index, roll in enumerate(not_used_rolls):
                if self.turn == 0:
                    arcade.draw_texture_rectangle(
                        SCREEN_WIDTH - PLAYER_STAT_WIDTH - BOARD_WIDTH / 4 + DICE_X[index],
                        SCREEN_HEIGHT / 2, 50, 50, self.dice.get_face(roll))
                else:
                    arcade.draw_texture_rectangle(
                        PLAYER_STAT_WIDTH + BOARD_WIDTH / 4 + DICE_X[index],
                        SCREEN_HEIGHT / 2, 50, 50, self.dice.get_face(roll))
                sign = -sign

            # bear_off checkers
            for count in range(self.nr_of_beared_off[0]):
                arcade.draw_texture_rectangle(SCREEN_WIDTH - PLAYER_STAT_WIDTH / 4,
                                              BEAR_OFF_BEGIN_Y + count * (BEAR_OFF_CHECKER_HEIGHT + 2), 70, 15,
                                              self.beared_off_white)
            for count in range(self.nr_of_beared_off[1]):
                arcade.draw_texture_rectangle(PLAYER_STAT_WIDTH / 4,
                                              BEAR_OFF_BEGIN_Y + count * (BEAR_OFF_CHECKER_HEIGHT + 2), 70, 15,
                                              self.beared_off_red)

            # hint messages
            if self.bottom_message_time > 0:
                arcade.draw_text(self.bottom_message, SCREEN_WIDTH / 2, 17, color=arcade.color.WHITE, font_size=20,
                                 anchor_x="center",
                                 anchor_y="center")
                self.bottom_message_time -= 1

            # game over screen
            if self.winner is not None:
                arcade.draw_texture_rectangle(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 + 27, 200, 50, self.play_again)
                arcade.draw_texture_rectangle(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 - 27, 200, 50, self.main_menu)
                if self.winner == 1:
                    if self.is_cpu_game:
                        message = "CPU won"
                    else:
                        message = "Red won"
                else:
                    message = "You won"
                arcade.draw_text(message, SCREEN_WIDTH / 2, 17, color=arcade.color.WHITE, font_size=20,
                                 anchor_x="center",
                                 anchor_y="center")

    def on_update(self, delta_time):
        """Called every frame"""
        if self.is_cpu_game and self.turn == 1 and self.selected_checker_destination is None:
            if len(self.rolls) != len(self.used_rolls):
                # sleep(2)
                roll_index = random.randint(0, len(self.rolls) - 1)
                avalable_rolls = list_difference(self.rolls, self.used_rolls)
                while True:
                    if len(avalable_rolls) == 0:
                        break
                    self.current_roll = avalable_rolls[roll_index % len(avalable_rolls)]
                    if self.current_roll in self.dead_rolls:
                        break
                    if len(self.dead_checker_list[1]) == 0:
                        bear_off_point = self.get_point_by_id(self.current_roll)
                        if self.ready_for_bearoff(1) and bear_off_point.checker_color == 1:
                            self.set_selected_checker(bear_off_point.get_top_checker())
                            self.selected_checker_destination = self.get_bear_off_destination(1)
                            self.selected_checker_origin = self.selected_checker.position
                            self.checker_state = "bear_off"
                            break
                        else:
                            checker_index = random.randint(0, len(self.checker_list) - 1)
                            for index in range(checker_index, checker_index + len(self.checker_list)):
                                random_checker = self.checker_list[index % len(self.checker_list)]
                                if random_checker.colorr == 1 and random_checker.is_selectable:
                                    destination_point = self.get_point_by_id(
                                        random_checker.point.id - self.current_roll)
                                    if destination_point:
                                        if self.is_valid_move(random_checker, destination_point, self.rolls,
                                                              self.used_rolls):
                                            self.set_selected_checker(random_checker)
                                            destination_point.arrange_pile(for_what="add")
                                            self.selected_checker_origin = self.selected_checker.position
                                            self.selected_checker_destination = \
                                                destination_point.get_checker_destination(
                                                    self.selected_checker)
                                            self.checker_state = "valid_move"
                                            break
                            if self.selected_checker_destination:
                                break
                            else:
                                if self.ready_for_bearoff(1):
                                    for point_id in reversed(range(1, self.current_roll)):
                                        bear_off_point = self.get_point_by_id(point_id)
                                        if bear_off_point.checker_color == 1:
                                            self.set_selected_checker(bear_off_point.get_top_checker())
                                            self.selected_checker_destination = self.get_bear_off_destination(1)
                                            self.selected_checker_origin = self.selected_checker.position
                                            self.checker_state = "bear_off"
                                            break
                                    if self.selected_checker_destination:
                                        break
                                self.dead_rolls.append(self.current_roll)
                                if len(self.rolls) == 4:
                                    break


                    # cpu has to revive dead checkers
                    else:
                        for checker in self.dead_checker_list[1]:
                            if checker.is_selectable:
                                destination_point = self.get_point_by_id(25 - self.current_roll)
                                if self.is_valid_move(checker, destination_point, self.rolls, self.used_rolls):
                                    self.set_selected_checker(checker)
                                    destination_point.arrange_pile(for_what="add")
                                    self.selected_checker_origin = self.selected_checker.position
                                    self.selected_checker_destination = destination_point.get_checker_destination(
                                        self.selected_checker)
                                    self.checker_state = "valid_move"
                                    break
                        if self.selected_checker_destination:
                            break
                        else:
                            self.dead_rolls.append(self.current_roll)
                            if len(self.rolls) == 4:
                                break
                    roll_index += 1
                if len(self.dead_rolls) > 0:
                    self.bottom_message = "CPU is out of moves. Your turn."
                    self.bottom_message_time = BOTTOM_MSG_TIME
                    self.used_rolls = list(self.rolls)

            else:
                self.rolls = self.dice.double_roll()
                self.used_rolls.clear()
                self.dead_rolls.clear()
                self.turn = 1 - self.turn
                if self.winner is None:
                    self.player_can_move = self.valid_move_exists(self.turn)

        if self.selected_checker_destination is not None:

            if self.animation_iteration < CHECKER_SPEED:
                # self.last_x_distance = abs(self.animation_checker.center_x - self.selected_checker_destination[0])
                self.selected_checker.center_x += (self.selected_checker_destination[0] -
                                                   self.selected_checker_origin[0]) / CHECKER_SPEED
                self.selected_checker.center_y += (self.selected_checker_destination[1] -
                                                   self.selected_checker_origin[1]) / CHECKER_SPEED
                self.animation_iteration += 1

            else:
                self.place_selected_checker(self.current_roll)
                self.selected_checker.position = self.selected_checker_destination
                self.animation_iteration = 0
                self.selected_checker = None
                self.selected_checker_destination = None
                if self.nr_of_beared_off[self.turn] == 17:
                    self.used_rolls = list(self.rolls)
                    self.winner = self.turn
                    if self.nr_of_beared_off[1 - self.turn] == 0:
                        if len(self.dead_checker_list[1 - self.turn]) > 0:
                            self.score[self.winner] += 3
                        else:
                            self.score[self.winner] += 2
                    else:
                        self.score[self.winner] += 1

                if self.winner is None and (self.turn == 0 or (self.turn == 1 and not self.is_cpu_game)):
                    self.player_can_move = self.valid_move_exists(self.turn)

    def set_selected_checker(self, checker):
        """Removes a checker from it's pile and sets the selected checker attribute"""
        self.bring_sprite_to_front(checker)
        if checker.is_dead:
            self.dead_checker_list[checker.colorr].remove(checker)
            if len(self.dead_checker_list[checker.colorr]) > 0:
                self.dead_checker_list[checker.colorr][-1].is_selectable = True
            self.dead_checker_origin = checker.position
            self.selected_checker = checker

        elif len(self.dead_checker_list[self.turn]) == 0:
            checker.point.arrange_pile(for_what="remove")
            checker.remove()

            self.selected_checker = checker

    def on_mouse_press(self, x, y, button, key_modifiers):
        """ Called when the user presses a mouse button. """
        if self.game_state == "before_choose_turns":
            if SCREEN_WIDTH / 2 - 100 <= x <= SCREEN_WIDTH / 2 + 100 and \
                    SCREEN_HEIGHT / 2 - 25 <= y <= SCREEN_HEIGHT / 2 + 25:
                self.game_state = "choosing_turns"
                self.white_roll = self.dice.roll()
                self.red_roll = self.dice.roll()

        elif self.game_state == "choosing_turns":
            if SCREEN_WIDTH / 2 - 100 <= x <= SCREEN_WIDTH / 2 + 100 and \
                    SCREEN_HEIGHT / 2 - 25 <= y <= SCREEN_HEIGHT / 2 + 25:
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
            if self.selected_checker_destination is None:
                if self.winner is None:
                    # if len(self.used_rolls) == len(self.rolls):
                    if not self.player_can_move:
                        if 0 <= SCREEN_WIDTH / 2 + BOARD_WIDTH / 2 + PLAYER_STAT_WIDTH / 2 + 35 - x <= 70 and \
                                0 <= SCREEN_HEIGHT / 2 + 35 - y <= 70 and self.turn == 0:
                            self.rolls = self.dice.double_roll()
                            self.used_rolls.clear()
                            self.turn = 1 - self.turn
                            self.player_can_move = self.valid_move_exists(self.turn)

                        elif 0 <= PLAYER_STAT_WIDTH / 2 + 35 - x <= 70 and 0 <= SCREEN_HEIGHT / 2 + 35 - y <= 70 and \
                                self.turn == 1 and not self.is_cpu_game:
                            self.rolls = self.dice.double_roll()
                            self.turn = 1 - self.turn
                            self.used_rolls.clear()
                            self.player_can_move = self.valid_move_exists(self.turn)
                        else:
                            self.bottom_message = "Out of moves. You have to seize your turn."
                            self.bottom_message_time = BOTTOM_MSG_TIME

                    else:
                        clicked_checkers = arcade.get_sprites_at_point((x, y), self.checker_list)
                        for checker in clicked_checkers:
                            if checker.colorr == self.turn and checker.is_selectable:
                                self.set_selected_checker(checker)

                                if self.selected_checker:
                                    break



                else:
                    if SCREEN_WIDTH / 2 - 100 <= x <= SCREEN_WIDTH / 2 + 100 and \
                            SCREEN_HEIGHT / 2 + 2 <= y <= SCREEN_HEIGHT / 2 + 52:
                        self.setup()
                    if SCREEN_WIDTH / 2 - 100 <= x <= SCREEN_WIDTH / 2 + 100 and \
                            SCREEN_HEIGHT / 2 - 2 >= y >= SCREEN_HEIGHT / 2 - 52:
                        menu_view = MenuView()
                        self.window.show_view(menu_view)

    def place_selected_checker(self, bear_off_roll=None):
        """Adds a checker to it's destination checker pile depending on it's state:
        moved, missplaced, bear off
        """
        if self.checker_state == "valid_move":
            destination_point, dist = arcade.get_closest_sprite(self.selected_checker, self.point_list)
            placed_checker, used_roll, dead_checker = destination_point.add_checker(self.selected_checker)
            self.used_rolls.append(used_roll)
            if dead_checker is not None:
                self.bring_sprite_to_front(dead_checker)
                dead_checker.position = SCREEN_WIDTH / 2 + DEAD_CHECKER_PILE_DIRECTION[
                    dead_checker.colorr] * (BOARD_WIDTH / 2 + PLAYER_STAT_WIDTH / 4), CHECKER_RADIUS + 5 + 50 * len(
                    self.dead_checker_list[dead_checker.colorr])
                if len(self.dead_checker_list[dead_checker.colorr]) > 0:
                    self.dead_checker_list[dead_checker.colorr][-1].is_selectable = False
                self.dead_checker_list[dead_checker.colorr].append(dead_checker)

        elif self.checker_state == "missplaced":
            self.selected_checker.place_back_to_origin(self.dead_checker_list)
        elif self.checker_state == "bear_off":
            self.used_rolls.append(bear_off_roll)
            self.checker_list.remove(self.selected_checker)
            self.nr_of_beared_off[self.turn] += 1

    def get_bear_off_destination(self, turn):
        """Returns position of next checker to be added to bear off pile"""
        position = []
        if turn == 0:
            position.append(SCREEN_WIDTH - PLAYER_STAT_WIDTH / 4)
        else:
            position.append(PLAYER_STAT_WIDTH / 4)
        position.append(BEAR_OFF_BEGIN_Y + self.nr_of_beared_off[turn] * (BEAR_OFF_CHECKER_HEIGHT + 2))
        return position

    def on_mouse_release(self, x: float, y: float, button: int,
                         modifiers: int):
        """ Called when the user presses a mouse button. """
        if self.game_state == "started" and self.winner is None and self.selected_checker_destination is None:

            if self.selected_checker is not None and self.selected_checker_destination is None:
                if x > SCREEN_WIDTH - PLAYER_STAT_WIDTH and self.ready_for_bearoff(
                        0) or x < PLAYER_STAT_WIDTH and self.ready_for_bearoff(1):
                    if self.is_valid_move(self.selected_checker, None, self.rolls, self.used_rolls):
                        self.checker_state = "bear_off"
                        self.selected_checker_origin = x, y
                        self.selected_checker_destination = self.get_bear_off_destination(self.turn)
                    else:
                        self.selected_checker.point.arrange_pile(for_what="add")
                        self.selected_checker_destination = self.selected_checker.point.get_checker_destination(
                            self.selected_checker)
                        self.selected_checker_origin = x, y
                        self.checker_state = "missplaced"

                else:
                    closest_point, dist = arcade.get_closest_sprite(self.selected_checker, self.point_list)
                    if self.is_valid_move(self.selected_checker, closest_point, self.rolls, self.used_rolls):
                        closest_point.arrange_pile(for_what="add")
                        self.selected_checker_origin = x, y
                        self.selected_checker_destination = closest_point.get_checker_destination(
                            self.selected_checker)
                        self.checker_state = "valid_move"
                    # wrong move -> checker must be put back
                    else:
                        # checker is in play
                        if self.selected_checker.point is not None:
                            self.selected_checker.point.arrange_pile(for_what="add")
                            self.selected_checker_destination = self.selected_checker.point.get_checker_destination(
                                self.selected_checker)
                            self.selected_checker_origin = x, y
                            self.checker_state = "missplaced"
                        # checker is dead
                        else:
                            self.selected_checker_destination = self.dead_checker_origin
                            self.selected_checker_origin = x, y
                            self.checker_state = "missplaced"

    def valid_move_exists(self, turn):
        """Determines if a player still has available moves"""
        available_rolls = list_difference(self.rolls, self.used_rolls)
        if len(available_rolls) == 0:
            return False
        # if all checkers are in play
        if len(self.dead_checker_list[turn]) == 0:
            if self.ready_for_bearoff(turn):
                # if there is a checker on roll position it can be beared_off
                for roll in available_rolls:
                    point_id = 25 - roll if turn == 0 else roll
                    if self.get_point_by_id(point_id).checker_color == turn:
                        return True
                # if there is a roll bigger than the max checker position, that checker can be beared_off
                max_roll = max(available_rolls)
                low = 19 if self.turn == 0 else 7
                high = 25 if self.turn == 0 else 1
                step = 1 if self.turn == 0 else -1
                for point_id in range(low, high, step):
                    max_checker = self.get_point_by_id(point_id).get_top_checker()
                    if max_checker is not None:
                        if max_checker.colorr == self.turn:
                            break
                point_position = max_checker.point.id if self.turn == 1 else 25 - max_checker.point.id
                if max_roll > point_position:
                    return True

            # if a checker can be moved
            for point in self.point_list:
                top_checker = point.get_top_checker()
                if top_checker is not None and top_checker.colorr == turn:
                    for roll in available_rolls:
                        potential_destinations = [self.get_point_by_id(point.id + roll),
                                                  self.get_point_by_id(point.id - roll)]
                        for potential_destination in potential_destinations:
                            if potential_destination:
                                if self.is_valid_move(top_checker, potential_destination, self.rolls, self.used_rolls):
                                    return True
        # if there's a dead checker
        else:
            # find the selectable dead_checker
            for checker in self.dead_checker_list[turn]:
                if checker.is_selectable:
                    dead_checker = checker
                    break
            # check if it can be re-entered in play
            point_id = 1 if turn == 0 else 19
            while point_id != 7 and point_id != 25:
                point = self.get_point_by_id(point_id)
                if self.is_valid_move(dead_checker, point, self.rolls, self.used_rolls):
                    return True
                point_id += 1
        return False

    def is_valid_move(self, checker, point, rolls, used_rolls):
        """Determines if a move is valid"""
        # bear_off
        if point is None:
            self.current_roll = checker.point.id if checker.colorr == 1 else 25 - checker.point.id
        else:
            self.current_roll = (point.id if checker.colorr == 0 else 25 - point.id) if checker.point is None else abs(
                checker.point.id - point.id)
        available_rolls = list_difference(self.rolls, self.used_rolls)
        if self.current_roll not in available_rolls:
            if point is not None:
                # return False
                pass
            # checker can be beared_off is no checker can be moved and is on point with highest id
            else:
                max_roll = max(available_rolls)
                point_position = checker.point.id if self.turn == 1 else 25 - checker.point.id
                if max_roll > point_position:
                    low = 19 if self.turn == 0 else checker.point.id + 1
                    high = checker.point.id if self.turn == 0 else 7
                    for point_id in range(low, high):
                        if len(self.get_point_by_id(point_id).checker_pile) > 0:
                            return False
                else:
                    return False
                self.current_roll = max_roll
                return True

        if point is not None:
            if len(point.checker_pile) > 1 and checker.colorr == 1 - point.checker_color:
                return False
            # if checker is in play (not dead) => verify if move direction is valid
            if checker.point is not None:
                if checker.colorr == 0 and point.id - checker.point.id < 0:
                    return False
                if checker.colorr == 1 and point.id - checker.point.id > 0:
                    return False
            # if checker is dead
            else:
                # if dead checker placed outside house
                if self.current_roll > 6:
                    return False
        return True

    def on_mouse_motion(self, x: float, y: float, dx: float, dy: float):
        """ User moves mouse """
        if self.game_state == "started":
            if self.selected_checker is not None and self.selected_checker_destination is None:
                self.selected_checker.center_x += dx
                self.selected_checker.center_y += dy

    def set_points(self):
        """Creates all point objects and sets them to their positions"""
        color = 1  # red
        id = 1
        for y, x in POINTS_POSITIONS:
            point = Point(color, 25 - id)
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
        """Creates all checkers and places them in their initial positions"""
        for index, (y, x) in enumerate(CHECKER_POSITIONS):
            point_low = arcade.get_sprites_at_point((x, y), self.point_list)[0]
            point_low.checker_color = CHECKER_COLORS[index]
            point_top = arcade.get_sprites_at_point((x, SCREEN_HEIGHT - y), self.point_list)[0]
            point_top.checker_color = 1 - CHECKER_COLORS[index]
            for checker_count in range(CHECKER_PILES[index]):
                checker = Checker(CHECKER_COLORS[index], 1)
                checker.position = x, y + checker_count * CHECKER_PILE_OFFSET[CHECKER_PILES[index]]
                checker.point = point_low
                if CHECKER_PILES[index] == checker_count + 1:
                    checker.is_selectable = True
                point_low.checker_pile.append(checker)
                self.checker_list.append(checker)
                checker = Checker(1 - CHECKER_COLORS[index], 1)
                checker.position = x, SCREEN_HEIGHT - y - checker_count * CHECKER_PILE_OFFSET[CHECKER_PILES[index]]
                checker.point = point_top
                if CHECKER_PILES[index] == checker_count + 1:
                    checker.is_selectable = True
                point_top.checker_pile.append(checker)
                self.checker_list.append(checker)

    def bring_sprite_to_front(self, sprite):
        """Brings a sprite to the top of the list in order to be rendered on top"""
        if isinstance(sprite, Checker):
            self.checker_list.remove(sprite)
            self.checker_list.append(sprite)
            self.checker_list.draw()

    def ready_for_bearoff(self, player):
        """Determines if a player is allowed to bear off checkers"""
        if player == 0:
            for checker in self.checker_list:
                if checker.colorr == player and (checker.point is None or checker.point.id <= 18):
                    return False
        else:
            for checker in self.checker_list:
                if checker.colorr == player and (checker.point is None or checker.point.id > 6):
                    return False
        return True

    def get_point_by_id(self, idd):
        if idd < 1 or idd > 25:
            return None
        for point in self.point_list:
            if point.id == idd:
                return point

