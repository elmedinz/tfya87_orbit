import arcade
import math

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
SCREEN_TITLE = "ORBIT"
TIME_PER_FRAME = 1/80

G_CONSTANT = 0.0000000000667 

class vector:
    x = 0
    y = 0

    def __init__(self, x, y):
        self.x = x
        self.y = y

class SpaceBody:
    x = 0
    y = 0
    r = 0
    m = 0 # mass in kg
    color = (0, 0, 0) # arcade.color

    vel = vector(0, 0)
    rotation_acc = vector(0, 0)

    def __init__(self, x, y, r, m, color):
        self.x = x
        self.y = y
        self.r = r
        self.m = m
        self.color = color

    def update_pos(self):
        self.x = self.x + self.vel.x*TIME_PER_FRAME + (1/2)*self.rotation_acc.x*TIME_PER_FRAME
        self.y = self.y + self.vel.y*TIME_PER_FRAME + (1/2)*self.rotation_acc.y*TIME_PER_FRAME
        pass


class MyGame(arcade.Window):
    """
    Main application class.

    NOTE: Go ahead and delete the methods you don't need.
    If you do need a method, delete the 'pass' and replace it
    with your own code. Don't leave 'pass' in this program.
    """

    def __init__(self, width, height, title):
        super().__init__(width, height, title)

        arcade.set_background_color(arcade.color.BLACK)

        # If you have sprite lists, you should create them here,
        # and set them to None

        self.space_body_list = []

    def setup(self):
        # Create your sprites and sprite lists here
        star = SpaceBody(SCREEN_WIDTH/2, SCREEN_HEIGHT/2, 15, 198900000000000, arcade.color.AMBER)

        earth = SpaceBody(star.x, star.y + 50, 5, 1000000, arcade.color.BLUE)
        earth.rotation_acc = vector(0, -self.newton_gravitational_law(earth, star)/earth.m)
        earth.vel = vector(math.sqrt(abs(earth.rotation_acc.y*self.distance(earth, star))), 0)

        self.space_body_list.append(star)
        self.space_body_list.append(earth)

    def on_draw(self):
        """
        Render the screen.
        """

        # This command should happen before we start drawing. It will clear
        # the screen to the background color, and erase what we drew last frame.
        arcade.start_render()

        for space_body in self.space_body_list:
            arcade.draw_circle_filled(space_body.x, space_body.y, space_body.r, space_body.color)

    def on_update(self, delta_time):
        """
        All the logic to move, and the game logic goes here.
        Normally, you'll call update() on the sprite lists that
        need it.
        """

        for space_body in self.space_body_list:
            space_body.update_pos()

    def on_key_press(self, key, key_modifiers):
        """
        Called whenever a key on the keyboard is pressed.

        For a full list of keys, see:
        http://arcade.academy/arcade.key.html
        """
        pass

    def on_key_release(self, key, key_modifiers):
        """
        Called whenever the user lets off a previously pressed key.
        """
        pass

    def on_mouse_motion(self, x, y, delta_x, delta_y):
        """
        Called whenever the mouse moves.
        """
        pass

    def on_mouse_press(self, x, y, button, key_modifiers):
        """
        Called when the user presses a mouse button.
        """
        pass

    def on_mouse_release(self, x, y, button, key_modifiers):
        """
        Called when a user releases a mouse button.
        """
        pass

    def distance(self, body1, body2):
        return math.sqrt(math.pow(body2.x - body1.x, 2) + math.pow(body2.y - body1.y, 2))

    def newton_gravitational_law(self, body1, body2):
        return G_CONSTANT*((body1.m*body2.m)/self.distance(body1, body2))


def main():
    """ Main method """
    game = MyGame(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    game.setup()  
    arcade.run()

if __name__ == "__main__":
    main()