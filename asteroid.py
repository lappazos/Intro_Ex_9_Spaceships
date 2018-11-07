##################################################################
# FILE : asteroid.py
# WRITERS : Evyatar Cohan,Evyatar100,206121543 | Lior Paz,lioraryepaz,206240996
# EXERCISE : intro2cs ex9 2017-2018
# DESCRIPTION : contains class Asteroid
##################################################################

from random import *
from math import *


class Asteroid:
    """
    A class that represent Asteroid object in the game.
    combined from size, location & speed.
    The asteroids can move, draw itself on the screen, encounter other
    objects and disappear.
    """
    MAX_SPEED = 3  # we added a speed limit
    SIZE_FACTOR = 10
    NORMAL_FACTOR = -5

    def __init__(self, screen, location, size, speed=None):
        """
        Constructor
        :param screen: The screen object of the game
        :param location: start location - tuple (x,y)
        :param size: integer 1-3
        :param speed: a given speed to the object (optional - if none is
        given, random speed will be defined) tuple - (speed_x, speed_y)
        """
        self.__screen = screen
        self.__x = location[0]
        self.__y = location[1]
        if speed is None:
            self.__x_speed = uniform(-Asteroid.MAX_SPEED, Asteroid.MAX_SPEED)
            self.__y_speed = uniform(-Asteroid.MAX_SPEED, Asteroid.MAX_SPEED)
        else:
            self.__x_speed = speed[0]
            self.__y_speed = speed[1]
        self.__size = size

        self.__radius = self.__size * Asteroid.SIZE_FACTOR + \
                        Asteroid.NORMAL_FACTOR

        self.__screen.register_asteroid(self, self.__size)  # auto register to
        # the screen when created

    def move(self):
        """
        update the asteroid location, according to screen size sand
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

    def draw(self):
        """
        Draw the asteroid on the screen.
        """
        self.__screen.draw_asteroid(self, self.__x, self.__y)

    def get_size(self):
        """
        A Method for Asteroid object
        :return: the size of the asteroid
        """
        return self.__size

    def get_location(self):
        """
        A Method for Asteroid object
        :return: the location of the asteroid (tuple (x,y))
        """
        return self.__x, self.__y

    def get_speed(self):
        """
        A Method for Asteroid object
        :return: the speed of the asteroid (tuple (x,y))
        """
        return self.__x_speed, self.__y_speed

    def has_intersection(self, obj):
        """
        checks if the asteroid has encountered with another object
        :param obj: the other object  (Ship or Torpedo)
        :return: True if an intersection has accord, False otherwise.
        """
        obj_x, obj_y = obj.get_location()
        x = self.__x
        y = self.__y
        # Distance formula
        distance = sqrt((obj_x - x) ** 2 + (obj_y - y) ** 2)
        if distance <= obj.get_radius() + self.__radius:
            return True
        return False

    def unregister(self):
        """
        unregister the asteroid from the screen.
        """
        self.__screen.unregister_asteroid(self)
