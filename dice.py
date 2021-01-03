import random
import arcade


class Dice:
    def __init__(self):
        self.faces = []

    def load_textures(self):
        self.faces.append(None)
        for i in range(1,7):
            self.faces.append(arcade.load_texture("resources/dice-" + str(i) + ".png"))

    def get_face(self, value):
        return self.faces[value]

    def roll(self):
        return random.randint(1, 6)

    def double_roll(self):
        return random.randint(1, 6), random.randint(1, 6)
