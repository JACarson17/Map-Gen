import pygame
from .constants import *
from .Coord import Coord
type_lut = {COMMON: WHITE,
                BOSS: RED,
                TREASURE: YELLOW,
                SHOP: GREEN,
                SECRET: BLUE,
                STARTING: GREY}

class Room():

    def __init__(self, coord: Coord, type: str = COMMON) -> None:
        self.coord: Coord = coord
        self.type: str = type
        self.color: tuple[int, int, int] = type_lut[type]

        
    def make_type(self, type: str):
        self.type = type
        self.color = type_lut[type]

    def change_coords(self, new_coord):
        self.coord = new_coord
    
    def get_coord(self) -> Coord:
        return(self.coord)

    def draw(self, win):
        pygame.draw.rect(win, self.color, (self.coord.x*SQUARE_SIZE, self.coord.y*SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))