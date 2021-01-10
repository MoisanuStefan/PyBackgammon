import random
import arcade


class Dice:
    """
    Dice is used to mimic a dice that generates random rolls from 1 to 6

    ...
    Attributes
    ----------
    faces(): List
        List containing the textures for dice faces
    roll()
        Returns random number in [1,6]
    double_roll()
        Return 2 random numbers in [1,6]
        Duplicates each roll if they coincide




    Methods
    ----------
    place_back_to_origin()
    Puts checker back if user moves it to an invalid destination
            """
    def __init__(self):
        self.faces = []

    def load_textures(self):
        self.faces.append(None)
        for i in range(1,7):
            self.faces.append(arcade.load_texture("resources/dice-" + str(i) + ".png"))

    def get_face(self, value):
        return self.faces[value]

    def roll(self):
        """Returns random number in [1,6]"""
        return random.randint(1, 6)

    def double_roll(self):
        """ Return 2 random numbers in [1,6]
        Duplicates each roll if they coincide
        """
        roll1 = random.randint(1, 6)
        roll2 = random.randint(1, 6)
        if roll1 == roll2:
            return roll1, roll1, roll1, roll1
        return roll1, roll2
