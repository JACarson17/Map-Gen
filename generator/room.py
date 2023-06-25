import pygame
from .constants import *

type_lut = {COMMON: WHITE,
                BOSS: RED,
                TREASURE: YELLOW,
                SHOP: GREEN,
                SECRET: BLUE,
                STARTING: GREY}

class Room():

    def __init__(self, col:int = 0, row:int = 0, type: str = COMMON) -> None:
        self.col: int = col
        self.row: int = row
        self.type: str = type
        self.color: tuple[int, int, int] = type_lut[type]

        
    def make_type(self, type: str):
        self.type = type
        self.color = type_lut[type]

    def change_coors(self, col: int, row: int):
        self.col = col
        self.row = row

    def get_row(self):
        return self.row
    
    def get_col(self):
        return self.col
    
    def get_coords(self) -> tuple[int, int]:
        return((self.get_col(), self.get_row()))

    def draw(self, win):
        pygame.draw.rect(win, self.color, (self.col*SQUARE_SIZE, self.row*SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))