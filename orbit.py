import arcade
import math

SCREEN_WIDTH = 600
SCREEN_HEIGHT = 600
SCREEN_TITLE = "ORBIT"
TIME_STEP = 1

STAR_CENTER_X = SCREEN_WIDTH/2
STAR_CENTER_Y = SCREEN_HEIGHT/2
STAR_MASS = 19890000000000
STAR_SIZE = 15

STAR_SIZE_INCREASE = 1
STAR_SIZE_DECREASE = 1

G_CONSTANT = 6.6674 * math.pow(10, -11)

def distance(body1, body2):
    return math.sqrt(math.pow(body2.x - body1.x, 2) + math.pow(body2.y - body1.y, 2))

def newton_gravitational_law(body1, body2):
    return G_CONSTANT*((body1.m*body2.m)/math.pow(distance(body1, body2), 2))

class Vector:
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
    
    grav_law = 0

    vel = Vector(0, 0)
    init_vel = Vector(0, 0)
    rotation_acc = Vector(0, 0)

    init_vel_size = 0

    rot_vel_ratio = 0

    const_dist = 0

    velocities_set = False

    def __init__(self, x, y, r, m, color):
        self.x = x
        self.y = y
        self.r = r
        self.m = m
        self.color = color

    def set_grav_law(self, val):
        self.grav_law = val
        self.init_vel_size = math.sqrt(abs((self.y - STAR_CENTER_Y)*self.grav_law))
        self.rot_vel_ratio = self.init_vel_size/self.grav_law

    def update_pos(self, star):
        acc_x = self.rotation_acc.x
        acc_y = self.rotation_acc.y

        dx = (self.x - STAR_CENTER_X)
        dy = (self.y - STAR_CENTER_Y)

        direction = 0
        
        # calclulate each component acceleration with constant gravity pull from star
        if dx != 0:
            direction = math.atan(abs(dy)/abs(dx))
            self.rotation_acc.x = math.cos(direction) * newton_gravitational_law(self, star)/self.m
            self.rotation_acc.y = math.sin(direction) * newton_gravitational_law(self, star)/self.m

            # determine direction of acceleration
            if dx > 0:
                self.rotation_acc.x *= -1
            if dy > 0:
                self.rotation_acc.y *= -1
        else:
            self.rotation_acc.y = newton_gravitational_law(self, star)/self.m
            self.rotation_acc.x = 0

            if dy > 0:
                self.rotation_acc.y *= -1


            self.vel = self.init_vel


        # calculate new component velocities from new acceleration
        if not self.velocities_set:
            # set direction of velocities before using leap frog
            self.vel.y = math.sqrt(abs(self.rotation_acc.x * dx))
            self.vel.x = math.sqrt(abs(self.rotation_acc.y * dy))
            self.velocities_set = True
        else: 
            # integer step leap frog algorithm
            self.vel.x = self.vel.x + 0.5 * (self.rotation_acc.x + acc_x) * TIME_STEP
            self.vel.y = self.vel.y + 0.5 * (self.rotation_acc.y + acc_y) * TIME_STEP

        # move the body
        self.x = self.x + self.vel.x * TIME_STEP + 0.5 * acc_x * TIME_STEP**2 
        self.y = self.y + self.vel.y * TIME_STEP + 0.5 * acc_y * TIME_STEP**2

class TextButton:
    """ Text-based button """

    def __init__(self,
                 center_x, center_y,
                 width, height,
                 text,
                 font_size=18,
                 font_face="Arial",
                 face_color=arcade.color.LIGHT_GRAY,
                 highlight_color=arcade.color.WHITE,
                 shadow_color=arcade.color.GRAY,
                 button_height=2):
        self.center_x = center_x
        self.center_y = center_y
        self.width = width
        self.height = height
        self.text = text
        self.font_size = font_size
        self.font_face = font_face
        self.pressed = False
        self.face_color = face_color
        self.highlight_color = highlight_color
        self.shadow_color = shadow_color
        self.button_height = button_height

    def draw(self):
        """ Draw the button """
        arcade.draw_rectangle_filled(self.center_x, self.center_y, self.width,
                                     self.height, self.face_color)

        if not self.pressed:
            color = self.shadow_color
        else:
            color = self.highlight_color

        # Bottom horizontal
        arcade.draw_line(self.center_x - self.width / 2, self.center_y - self.height / 2,
                         self.center_x + self.width / 2, self.center_y - self.height / 2,
                         color, self.button_height)

        # Right vertical
        arcade.draw_line(self.center_x + self.width / 2, self.center_y - self.height / 2,
                         self.center_x + self.width / 2, self.center_y + self.height / 2,
                         color, self.button_height)

        if not self.pressed:
            color = self.highlight_color
        else:
            color = self.shadow_color

        # Top horizontal
        arcade.draw_line(self.center_x - self.width / 2, self.center_y + self.height / 2,
                         self.center_x + self.width / 2, self.center_y + self.height / 2,
                         color, self.button_height)

        # Left vertical
        arcade.draw_line(self.center_x - self.width / 2, self.center_y - self.height / 2,
                         self.center_x - self.width / 2, self.center_y + self.height / 2,
                         color, self.button_height)

        x = self.center_x
        y = self.center_y
        if not self.pressed:
            x -= self.button_height
            y += self.button_height

        arcade.draw_text(self.text, x, y,
                         arcade.color.BLACK, font_size=self.font_size,
                         width=self.width, align="center",
                         anchor_x="center", anchor_y="center")

    def on_press(self):
        self.pressed = True

    def on_release(self):
        self.pressed = False


def check_mouse_press_for_buttons(x, y, button_list):
    """ Given an x, y, see if we need to register any button clicks. """
    for button in button_list:
        if x > button.center_x + button.width / 2:
            continue
        if x < button.center_x - button.width / 2:
            continue
        if y > button.center_y + button.height / 2:
            continue
        if y < button.center_y - button.height / 2:
            continue
        button.on_press()

def check_mouse_release_for_buttons(_x, _y, button_list):
    """ If a mouse button has been released, see if we need to process
        any release events. """
    for button in button_list:
        if button.pressed:
            button.on_release()

class ButtonIncreaseMassSun(TextButton):
    def __init__(self, center_x, center_y, action_function):
        # TODO: Change text size/font if necessary
        super().__init__(center_x, center_y, 100, 40, "Incr. Mass: Sun", 20, "Arial")
        self.action_function = action_function

    def on_release(self):
        super().on_release()
        self.action_function()

class ButtonDecreaseMassSun(TextButton):
    def __init__(self, center_x, center_y, action_function):
        # TODO: Change text size/font if necessary
        super().__init__(center_x, center_y, 100, 40, "Decr. Mass: Sun", 20, "Arial")
        self.action_function = action_function

    def on_release(self):
        super().on_release()
        self.action_function()



class MyGame(arcade.Window):
    """
    Main application class.

    NOTE: Go ahead and delete the methods you don't need.
    If you do need a method, delete the 'pass' and replace it
    with your own code. Don't leave 'pass' in this program.
    """

    star = SpaceBody(STAR_CENTER_X, STAR_CENTER_Y, STAR_SIZE, STAR_MASS, arcade.color.AMBER)

    def __init__(self, width, height, title):
        super().__init__(width, height, title)

        arcade.set_background_color(arcade.color.BLACK)

        # If you have sprite lists, you should create them here,
        # and set them to None

        self.space_body_list = None
        self.button_list = None
        self.draw_list = None

    def setup(self):
        # Create your sprites and sprite lists here
        self.space_body_list = []
        self.button_list = []
        self.draw_list = []

        earth = SpaceBody(self.star.x, self.star.y + 100, 5, 1000000000, arcade.color.BLUE)
        earth.set_grav_law(newton_gravitational_law(earth, self.star)/earth.m)
        earth.rotation_acc = Vector(0, earth.grav_law)
        earth.vel = Vector(math.sqrt(abs(earth.rotation_acc.y*distance(earth, self.star))), 0)

        self.draw_list.append(self.star)

        self.space_body_list.append(earth)
        self.draw_list.append(earth)

        # TODO: CHANGE THESE
        button_increase_sun_mass = ButtonIncreaseMassSun(60, 570, self.increase_sun_mass)
        self.button_list.append(button_increase_sun_mass)

        button_decrease_sun_mass = ButtonDecreaseMassSun(60, 515, self.decrease_sun_mass)
        self.button_list.append(button_decrease_sun_mass)


    def on_draw(self):
        """
        Render the screen.
        """

        # This command should happen before we start drawing. It will clear
        # the screen to the background color, and erase what we drew last frame.
        arcade.start_render()

        for space_body in self.draw_list:
            arcade.draw_circle_filled(space_body.x, space_body.y, space_body.r, space_body.color)

        for button in self.button_list:
            button.draw()

    def on_update(self, delta_time):
        """
        All the logic to move, and the game logic goes here.
        Normally, you'll call update() on the sprite lists that
        need it.
        """

        for space_body in self.space_body_list:
            space_body.update_pos(self.star)

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
        check_mouse_press_for_buttons(x, y, self.button_list)

    def on_mouse_release(self, x, y, button, key_modifiers):
        """
        Called when a user releases a mouse button.
        """
        check_mouse_release_for_buttons(x, y, self.button_list)

    # TODO: Does this work?
    def increase_sun_mass(self):
        self.star.m = self.star.m + (STAR_MASS * 0.1)
        self.star.r += STAR_SIZE_INCREASE

    # TODO: Does this work?
    def decrease_sun_mass(self):
        self.star.m = self.star.m - (STAR_MASS * 0.1)
        if self.star.m < 0:
            self.star.m = 0
            return
        
        self.star.r -= STAR_SIZE_DECREASE
        if self.star.r < STAR_SIZE_DECREASE:
            self.star.r = STAR_SIZE_DECREASE


def main():
    """ Main method """
    game = MyGame(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    game.setup()  
    arcade.run()

if __name__ == "__main__":
    main()