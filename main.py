"""
Main file for Magma Boy and Hydro Girl game.
"""

# import pygame and orther needed libraries
import sys
import pygame
from pygame.locals import *

# import classes
from game import Game
from board import Board
from character import MagmaBoy, HydroGirl
from controller import ArrowsController, WASDController, GeneralController
from gates import Gates
from doors import FireDoor, WaterDoor
from level_select import LevelSelect
from gesture_controller import GestureController


def main():
    pygame.init()
    controller = GeneralController()
    game = Game()
    show_intro_screen(game, controller)


def show_intro_screen(game, controller):
    intro_screen = pygame.image.load('data/screens/intro_screen.png')
    game.display.blit(intro_screen, (0, 0))
    while True:
        game.refresh_window()
        if controller.press_key(pygame.event.get(), K_RETURN):
            show_level_screen(game, controller)


def show_level_screen(game, controller):
    level_select = LevelSelect()
    level = game.user_select_level(level_select, controller)
    run_game(game, controller, level)


def show_win_screen(game, controller):
    win_screen = pygame.image.load('data/screens/win_screen.png')
    win_screen.set_colorkey((255, 0, 255))
    game.display.blit(win_screen, (0, 0))

    while True:
        game.refresh_window()
        if controller.press_key(pygame.event.get(), K_RETURN):
            show_level_screen(game, controller)


def show_death_screen(game, controller, level):
    death_screen = pygame.image.load('data/screens/death_screen.png')
    death_screen.set_colorkey((255, 0, 255))
    game.display.blit(death_screen, (0, 0))
    while True:
        game.refresh_window()
        events = pygame.event.get()
        if controller.press_key(events, K_RETURN):
            run_game(game, controller, level)
        if controller.press_key(events, K_ESCAPE):
            show_level_screen(game, controller)


def run_game(game, controller, level="level1"):
    # load level data
    if level == "level1":
        board = Board('data/level0.txt')
        gates = []

        fire_door_location = (5 * 16, 4 * 16)
        fire_door = FireDoor(fire_door_location)
        water_door_location = (28 * 16, 4 * 16)
        water_door = WaterDoor(water_door_location)
        doors = [fire_door, water_door]

        magma_boy_location = (28 * 16, 4 * 16)
        magma_boy = MagmaBoy(magma_boy_location)
        hydro_girl_location = (5 * 16, 4 * 16)
        hydro_girl = HydroGirl(hydro_girl_location)

    if level == "level2":
        board = Board('data/level1.txt')
        gate_location = (285, 128)
        plate_locations = [(190, 168), (390, 168)]
        gate = Gates(gate_location, plate_locations)
        gates = [gate]

        fire_door_location = (64, 48)
        fire_door = FireDoor(fire_door_location)
        water_door_location = (128, 48)
        water_door = WaterDoor(water_door_location)
        doors = [fire_door, water_door]

        magma_boy_location = (16, 336)
        magma_boy = MagmaBoy(magma_boy_location)
        hydro_girl_location = (35, 336)
        hydro_girl = HydroGirl(hydro_girl_location)

    if level == "level3":
        board = Board('data/level2.txt')
        gates = []

        fire_door_location = (390, 48)
        fire_door = FireDoor(fire_door_location)
        water_door_location = (330, 48)
        water_door = WaterDoor(water_door_location)
        doors = [fire_door, water_door]

        magma_boy_location = (16, 336)
        magma_boy = MagmaBoy(magma_boy_location)
        hydro_girl_location = (35, 336)
        hydro_girl = HydroGirl(hydro_girl_location)

    if level == "level4":
        board = Board('data/level3.txt')
        gates = []

        fire_door_location = (5 * 16, 4 * 16)
        fire_door = FireDoor(fire_door_location)
        water_door_location = (28 * 16, 4 * 16)
        water_door = WaterDoor(water_door_location)
        doors = [fire_door, water_door]

        magma_boy_location = (28 * 16, 4 * 16)
        magma_boy = MagmaBoy(magma_boy_location)
        hydro_girl_location = (5 * 16, 4 * 16)
        hydro_girl = HydroGirl(hydro_girl_location)
    
    if level == "level5":
        board = Board('data/level4.txt')
        gates = []

        fire_door_location = (390, 48)
        fire_door = FireDoor(fire_door_location)
        water_door_location = (330, 48)
        water_door = WaterDoor(water_door_location)
        doors = [fire_door, water_door]

        magma_boy_location = (16, 336)
        magma_boy = MagmaBoy(magma_boy_location)
        hydro_girl_location = (35, 336)
        hydro_girl = HydroGirl(hydro_girl_location)

    # initialize needed classes

    arrows_controller = ArrowsController()
    wasd_controller = WASDController()

    clock = pygame.time.Clock()

    gesture_controller = GestureController()
    prev_x = 0.5  # center

    # main game loop
    while True:
        # pygame management
        clock.tick(60)
        events = pygame.event.get()

        # draw features of level
        game.draw_level_background(board)
        game.draw_board(board)
        if gates:
            game.draw_gates(gates)
        game.draw_doors(doors)

        # draw player
        game.draw_player([magma_boy, hydro_girl])

        ########################
        #  move player (arrows and wasd)
        # arrows_controller.control_player(events, magma_boy)
        # wasd_controller.control_player(events, hydro_girl)

        #################
        # move player (hand gestures & just one player, no split screen)
        '''
        
        gesture_move_right, gesture_move_left, gesture_jump = gesture_controller.get_controls(prev_x)

        # Apply to MagmaBoy
        magma_boy.moving_right = gesture_move_right
        magma_boy.moving_left = gesture_move_left

        if gesture_jump and magma_boy.air_timer < 6:
            magma_boy.jumping = True

        prev_x = gesture_controller.hand_x if gesture_controller.hand_x else prev_x


        magma_controls, hydro_controls = gesture_controller.get_controls()
        '''


        #####################

        # move players at the same time with split screen:

        # move players based on gesture controls
        magma_controls, hydro_controls = gesture_controller.get_controls()

        # MagmaBoy (right side of camera)
        magma_boy.moving_right = magma_controls[0]
        magma_boy.moving_left = magma_controls[1]

        # HydroGirl (left side of camera)
        hydro_girl.moving_right = hydro_controls[0]
        hydro_girl.moving_left = hydro_controls[1]


        game.move_player(board, gates, [magma_boy, hydro_girl])

        # check for player at special location
        game.check_for_death(board, [magma_boy, hydro_girl])

        game.check_for_gate_press(gates, [magma_boy, hydro_girl])

        game.check_for_door_open(fire_door, magma_boy)
        game.check_for_door_open(water_door, hydro_girl)

        # refresh window
        game.refresh_window()

        # special events
        if hydro_girl.is_dead() or magma_boy.is_dead():
            show_death_screen(game, controller, level)

        if game.level_is_done(doors):
            show_win_screen(game, controller)

        if controller.press_key(events, K_ESCAPE):
            show_level_screen(game, controller)

        # close window is player clicks on [x]
        for event in events:
            if event.type == QUIT:
                gesture_controller.stop()
                pygame.quit()
                sys.exit()


if __name__ == '__main__':
    main()
