##################################################################
# FILE : torpedo.py
# WRITERS : Evyatar Cohan,Evyatar100,206121543 | Lior Paz,lioraryepaz,206240996
# EXERCISE : intro2cs ex9 2017-2018
# DESCRIPTION : contains class Torpedo
##################################################################

from random import *
from math import *


class Torpedo:
    """
    A class that represent Torpedo object in the game.
    combined from size, location & speed, angle, life-time.
    The torpedo is an object associated with Ship object - it gets it
    initial speed location & angle from a given ship object.
    every torpedo has life time, which kills him when ended.
    can move, draw itself on the screen, and disappear.
    """
    RADIUS = 4
    ACCELERATION_FACTOR = 2
    LIFE_TIME = 200

    def __set_speed(self, speed, angle):
        """
        sets the torpedo speed according to 'mother' ship.
        :param speed: speed of 'mother' ship
        :param angle: head angle of 'mother' ship
        """
        rad = radians(angle)
        # a formula for torpedo speed from pdf
        self.__x_speed = speed[0] + Torpedo.ACCELERATION_FACTOR * cos(rad)
        self.__y_speed = speed[1] + Torpedo.ACCELERATION_FACTOR * sin(rad)

    def __init__(self, screen, ship):
        """
        Constructor
        :param screen: The screen object of the game
        :param ship: the ship that shoots the Torpedo
        """
        self.__screen = screen
        self.__angle = ship.get_angle()
        self.__x, self.__y = ship.get_location()
        self.__set_speed(ship.get_speed(), self.__angle)
        self.__screen.register_torpedo(self)  # auto register to the screen
        # when created
        self.__life_time = Torpedo.LIFE_TIME

    def move(self):
        """
        update the torpedo location, according to screen size sand
        given speed.
        """
        min_x = self.__screen.SCREEN_MIN_X
        min_y = self.__screen.SCREEN_MIN_Y
        delta_x = self.__screen.SCREEN_MAX_X - min_x
        delta_y = self.__screen.SCREEN_MAX_Y - min_y
        #  new location formula according to pdf.
        new_x = (self.__x_speed + self.__x - min_x) % delta_x + min_x
        new_y = (self.__y_speed + self.__y - min_y) % delta_y + min_y
        self.__x, self.__y = new_x, new_y

        self.__life_time -= 1  # life decrease in every movement

    def draw(self):
        """
        Draw the ship on the screen.
        """
        self.__screen.draw_torpedo(self, self.__x, self.__y, self.__angle)

    def get_life_time(self):
        """
        A Method for Torpedo object
        :return: The correct life time of the torpedo.
        """
        return self.__life_time

    def get_location(self):
        """
        A Method for Torpedo object
        :return: the location of the torpedo (tuple (x,y))
        """
        return self.__x, self.__y

    def get_radius(self):
        """
        A Method for Torpedo object
        :return: the radius of the torpedo
        """
        return Torpedo.RADIUS

    def get_speed(self):
        """
        A Method for Ship object
        :return: the speed of the torpedo (x_speed, y_speed)
        """
        return self.__x_speed, self.__y_speed

    def unregister(self):
        """
        unregister the torpedo from the screen.
        """
        self.__screen.unregister_torpedo(self)
