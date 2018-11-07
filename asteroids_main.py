##################################################################
# FILE : asteroids_main.py
# WRITERS : Evyatar Cohan,Evyatar100,206121543 | Lior Paz,lioraryepaz,206240996
# EXERCISE : intro2cs ex9 2017-2018
# DESCRIPTION : contains class GameRunner and and main of the game
##################################################################

from screen import Screen
import sys
from ship import Ship
from asteroid import Asteroid
from torpedo import Torpedo
from random import randint  # in order to choose random locations
from math import *

DEFAULT_ASTEROIDS_NUM = 5


class GameRunner:
    """
    This class manage the game
    """
    # in our implementation we used only 1 object of this kind
    START_AST_SIZE = 3
    HIGH_SCORE = 100
    MED_SCORE = 50
    LOW_SCORE = 20
    MAX_TORPEDO_NUM = 15
    WIN_MSG = ('MAZAL TOV!!!', "You managed to destroy the planet of death, "
                               "and took us another step towards defeating "
                               "the Empire! ")
    LOSS_MSG = ("The ship has CRASHED...", "Another Jedi will save us...")
    EXIT_MSG = ("QUIETER!", "How could you ??")
    HIT_MSG = ('Hit', 'Your ship has been hit - May the force be with you')

    def __init__(self, asteroids_amnt):
        """
        Constructor
        :param asteroids_amnt: The amount of asteroids the game will start with
        """
        self.__screen = Screen()
        # every game has one screen object he works with

        self.screen_max_x = Screen.SCREEN_MAX_X
        self.screen_max_y = Screen.SCREEN_MAX_Y
        self.screen_min_x = Screen.SCREEN_MIN_X
        self.screen_min_y = Screen.SCREEN_MIN_Y

        self.__ship = Ship(self.__screen, self.get_rand_location())
        # every game contains only one ship object

        # initiation of asteroids objects
        self.__asteroids = []
        for asteroid in range(asteroids_amnt):
            while True:
                # this loop makes sure that the asteroid is not generated
                # at the current location of the ship
                asteroid = Asteroid(self.__screen, self.get_rand_location(),
                                    GameRunner.START_AST_SIZE)
                if not asteroid.has_intersection(self.__ship):
                    break
            self.__asteroids.append(asteroid)

        self.__torpedos = []

        self.__score = 0

    def get_rand_location(self):
        """
        :return: a random location on the screen (tuple - (x,y))
        """
        x = randint(self.screen_min_x, self.screen_max_x)
        y = randint(self.screen_min_y, self.screen_max_y)
        return x, y

    def run(self):
        """
        start the game
        """
        self._do_loop()
        self.__screen.start_screen()

    def _do_loop(self):
        """
        runs game loop constantly.
        """
        self._game_loop()

        # Set the timer to go off again
        self.__screen.update()
        self.__screen.ontimer(self._do_loop, 5)

    def _game_loop(self):
        """
        The main function of the game - update the status of all objects at
        the screen in every single loop, according to the different
        applications.
        """
        self.__try_generate_torpedo()  # this function generates a torpedo if
        # needed
        self.__crash_loop()  # manage encounters between objects
        # Exit button check

        # the following lines update the status of all objects, monitor their
        #  progress and draw them.
        self.__ship_loop()
        self.__torpedo_loop()
        self.__asteroids_loop()

        if self.__screen.should_end():
            self.__exit_game(GameRunner.EXIT_MSG)

    def __exit_game(self, msg):
        """
        pop the given message and exit the game.
        :param msg: tuple contains strings (title, message)
        """
        self.__screen.show_message(msg[0], msg[1])
        self.__screen.end_game()
        sys.exit(0)

    def __ship_loop(self):
        """
        updates the location, speed and position of the ship and draw it.
        """
        self.__ship.rotate()
        self.__ship.accelerate()
        self.__ship.move()
        self.__ship.draw()

    def __torpedo_loop(self):
        """
        updates the locations of all torpedoes ,draw them, & remove the needed
        torpedoes.
        """
        for torpedo in self.__torpedos:
            if torpedo.get_life_time() < 0:
                self.remove_torpedo(torpedo)
                continue
            torpedo.move()
            torpedo.draw()

    def __asteroids_loop(self):
        """
        updates the locations of all asteroids and draw them. exit the game
        in case of no asteroids left.
        """
        if len(self.__asteroids) <= 0:
            self.__exit_game(GameRunner.WIN_MSG)
        for asteroid in self.__asteroids:
            asteroid.move()
            asteroid.draw()

    def __try_generate_torpedo(self):
        """
        generate new torpedo object if space was pressed, only if max
        capacity hasn't filled yet.
        """
        if self.__screen.is_space_pressed() and (len(self.__torpedos) <= \
                GameRunner.MAX_TORPEDO_NUM):
            self.__torpedos.append(Torpedo(self.__screen, self.__ship))

    def __change_score(self, asteroid):
        """
        updates the game score according to the destroyed asteroid size.
        :param asteroid: The destroyed asteroid
        """
        if asteroid.get_size() is 3:
            self.__score += GameRunner.HIGH_SCORE
        elif asteroid.get_size() is 2:
            self.__score += GameRunner.MED_SCORE
        elif asteroid.get_size() is 1:
            self.__score += GameRunner.LOW_SCORE
        self.__screen.set_score(self.__score)

    def __calc_new_ast_speed(self, asteroid, torpedo):
        """
        calculate the speed of new asteroid objects that were generated
        post-hit.
        :param asteroid: the 'dead' asteroid
        :param torpedo: the hit torpedo
        :return: the speed of the new asteroid (tuple (speed_x,speed_y))
        """
        tor_x_s, tor_y_s = torpedo.get_speed()
        ast_x_s, ast_y_s = asteroid.get_speed()
        speed_x = (tor_x_s + ast_x_s) / sqrt(ast_x_s ** 2 + ast_y_s ** 2)
        speed_y = (tor_y_s + ast_y_s) / sqrt(ast_x_s ** 2 + ast_y_s ** 2)
        return speed_x, speed_y

    def __crash_loop(self):
        """
        for a given loop in the game, manage the possible outcomes of a
        crash between an Asteroid object to Torpedo/Ship:
        Asteroid & Ship - deduction of life, Asteroid Removal, Screen msg.
        Asteroid & Torpedo - Asteroid split, Torpedo Removal, Score addition.
        """
        for asteroid in self.__asteroids:
            if self.__try_ship_hit(asteroid):
                continue
            for torpedo in self.__torpedos:
                if asteroid.has_intersection(torpedo):
                    self.__change_score(asteroid)

                    # split the Asteroid or remove it
                    self.__try_split_ast(asteroid, torpedo)

                    self.remove_asteroid(asteroid)
                    self.remove_torpedo(torpedo)
                    break

    def __try_split_ast(self, asteroid, torpedo):
        """
        generates two new small asteroid if needed, according to the 'father'
        asteroid speed & size, and the hit torpedo speed.
        :param asteroid: The 'father' asteroid
        :param torpedo: the hit torpedo
        """
        if asteroid.get_size() > 1:
            new_speed = self.__calc_new_ast_speed(asteroid, torpedo)
            # we would like each asteroid to move in opposite directions -
            # that the (-1)
            new_speed_2 = (-new_speed[0], -new_speed[1])
            # creating the new objects
            sub_asterois_1 = Asteroid(self.__screen, asteroid.get_location(),
                                      asteroid.get_size() - 1, new_speed)
            sub_asterois_2 = Asteroid(self.__screen, asteroid.get_location(),
                                      asteroid.get_size() - 1, new_speed_2)
            self.__asteroids.append(sub_asterois_1)
            self.__asteroids.append(sub_asterois_2)

    def __try_ship_hit(self, asteroid):
        """
        for a given loop in the game, manage the crash between an Asteroid
        object & the Ship, if happened.
        Exit the game if no life have remained.
        :param asteroid: a given asteroid to check
        :return: True if indeed an encounter has happened, False otherwise.
        """
        if asteroid.has_intersection(self.__ship):
            # self.__ship.hit() returns True if the ship is dead,
            # in addition to other actions
            is_dead = self.__ship.hit()
            self.remove_asteroid(asteroid)
            if is_dead:
                self.__exit_game(GameRunner.LOSS_MSG)
            else:
                self.__screen.show_message(GameRunner.HIT_MSG[0],
                                           GameRunner.HIT_MSG[1])
            return True
        return False

    def remove_asteroid(self, asteroid):
        """
        remove an asteroid.
        :param asteroid: the asteroid to be removed.
        """
        asteroid.unregister()  # screen removal
        self.__asteroids.remove(asteroid)  # self removal

    def remove_torpedo(self, torpedo):
        """
        remove an torpedo.
        :param torpedo:  the torpedo to be removed.
        """
        torpedo.unregister()
        self.__torpedos.remove(torpedo)


def main(amnt):
    """
    generates GameRunner object and runs it
    :param amnt: amount of asteroids to start with
    """
    runner = GameRunner(amnt)
    runner.run()


if __name__ == "__main__":
    if len(sys.argv) > 1:
        main(int(sys.argv[1]))
    else:
        main(DEFAULT_ASTEROIDS_NUM)
