##################################################################
# FILE : ship.py
# WRITERS : Evyatar Cohan,Evyatar100,206121543 | Lior Paz,lioraryepaz,206240996
# EXERCISE : intro2cs ex9 2017-2018
# DESCRIPTION : contains class Ship
##################################################################

from math import *


class Ship:
    """
    A class that represent Ship object in the game.
    combined from location & speed, life amount, head angle - per moment.
    The ship can move, rotate accelerate draw itself on the screen, and die.
    """
    SHIP_START_ANGLE = 0
    INIT_SPEED = 0
    ACCELERATION_FACTOR = 0.4  # added to slow down the acceleration factor
    ROTATE_RIGHT = -7
    ROTATE_LEFT = 7
    MAX_SPEED = 10
    START_LIFE = 3
    SHIP_RADIUS = 1

    def __init__(self, screen, location):
        """
        Constructor
        :param screen: The screen object of the game
        :param location: start location - tuple (x,y)
        """
        self.__screen = screen
        self.__x = location[0]
        self.__y = location[1]
        self.__x_speed = Ship.INIT_SPEED
        self.__y_speed = Ship.INIT_SPEED
        self.__angle = Ship.SHIP_START_ANGLE
        self.__life = Ship.START_LIFE

    def move(self):
        """
        update the ship location, according to screen size sand
        given speed.
        """
        min_x = self.__screen.SCREEN_MIN_X
        min_y = self.__screen.SCREEN_MIN_Y
        delta_x = self.__screen.SCREEN_MAX_X - min_x
        delta_y = self.__screen.SCREEN_MAX_Y - min_y

        new_x = (self.__x_speed + self.__x - min_x) % delta_x + min_x
        new_y = (self.__y_speed + self.__y - min_y) % delta_y + min_y
        self.__x, self.__y = new_x, new_y

    def draw(self):
        """
        Draw the ship on the screen.
        """
        self.__screen.draw_ship(self.__x, self.__y, self.__angle)

    def rotate(self):
        """
        rotate the ship head ange if the user has pressed the button.
        """
        if self.__screen.is_left_pressed():
            self.__angle += Ship.ROTATE_LEFT
        if self.__screen.is_right_pressed():
            self.__angle += Ship.ROTATE_RIGHT

    def accelerate(self):
        """
        accelerate the ship speed if the user has pressed the button
        """
        if self.__screen.is_up_pressed():
            rad = radians(self.__angle)
            temp_x = self.__x_speed + Ship.ACCELERATION_FACTOR * cos(rad)
            temp_y = self.__y_speed + Ship.ACCELERATION_FACTOR * sin(rad)
            self.__x_speed = temp_x
            self.__y_speed = temp_y

    def get_location(self):
        """
        A Method for Ship object
        :return: tuple (x,y)
        """
        return self.__x, self.__y

    def get_speed(self):
        """
        A Method for Ship object
        :return: tuple (x_speed, y_speed)
        """
        return self.__x_speed, self.__y_speed

    def get_radius(self):
        """
        A Method for Ship object
        :return: ship radius
        """
        return Ship.SHIP_RADIUS

    def get_angle(self):
        """
        A Method for Ship object
        :return: current ship head angle
        """
        return self.__angle

    def hit(self):
        """
        handles with the ship life in case of crash
        :return: True in case of death, False otherwise
        """
        self.__screen.remove_life()
        self.__life -= 1
        if self.__life <= 0:
            return True
        return False
