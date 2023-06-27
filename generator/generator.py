import pygame
from .constants import *
from .room import Room
from .map import Map
from random import randint
from .Coord import Coord
class Generator():
    def __init__(self, win: pygame.Surface):
        self.map = Map()
        self.win = win

    def update(self):
        self.map.drawMap(self.win)
        pygame.display.update()
    
    def make_and_add_room(self, coord: Coord, type:str) -> Room:
        room = Room(coord, type)
        self.map.add_room(room)
        self.update()

    def determine_room_type(self, available: list[str], force_common: bool = True) -> str:
        # create lut
        room_lut:dict[int, str] = {}
        # look thru what type of rooms need to be added
        key = 0
        for i, type in enumerate(available):
            amount = self.map.get_all_rooms_by_type[type] - len(self.map.get_room_by_type(type))
            for room in range(amount):
                room_lut.update({key:type})
                key += 1
        # fill remaining spots with common rooms
        if COMMON not in available and force_common:
            while key < TOTAL_ROOMS - self.map.get_size():
                room_lut.update({key:COMMON})
                key += 1
        
        # select type of room randomly
        constructor_type = room_lut.get(randint(0, key-1))
        return constructor_type

    def reset(self):
        self.map.clear()

    def generate(self):
        self.reset()
        # how to generate a map
        # take total amount of tiles

        for tile in range(TOTAL_ROOMS - SPECIAL_ROOMS - len(SEMI_SPECIAL)):

        # start on origin, or close enough to it idk floor divide
            if tile == 0:
                self.make_and_add_room(Coord(COL//2, ROW//2), STARTING)
        # draw on random available side
            else:
                # check what special rooms have yet to be added
                # decide which type to add
                # type = self.determine_room_type(valid)
                type = COMMON
                # get map location 
                valid_coords = list(self.map.get_new_adjacent(type))
                coord = valid_coords[randint(0, len((valid_coords))-1)]
                self.make_and_add_room(coord, type)
        
        for tile, type in enumerate(SPECIAL + SEMI_SPECIAL):
            for i in range(rooms_by_type[type]):
                valid_coords = list(self.map.get_new_adjacent(type))
                coord = valid_coords[randint(0, len((valid_coords))-1)]
                self.make_and_add_room(coord, type)