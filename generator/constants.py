import pygame

WIDTH, HEIGHT = 1100, 700
COL, ROW = 22, 14
SQUARE_SIZE = WIDTH/COL
FPS = 60

TREASURE_ROOMS = 2
BOSS_ROOMS = 2
SHOP_ROOMS = 1
TOTAL_ROOMS = 50
SECRET_ROOMS = 2
SPECIAL_ROOMS = TREASURE_ROOMS + BOSS_ROOMS 

P_ONE = (0, 0.9)
P_TWO = (0.9, 0.95)
P_THREE = (0.95, 1)
P_FOUR  = (1.1, 1.2)
ROOM_WEIGHTS: dict[int, int] = {1: P_ONE,
                                2: P_TWO,
                                3: P_THREE,
                                4: P_FOUR}

RED = (255, 0, 0)   # Boss room
WHITE = (255, 255, 255) # regular room
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)  # secret room
GREY = (128, 128, 128)  # starting room
GREEN = (0, 255, 0) # shop room
YELLOW = (255, 255, 0)

STARTING = 'starting'
BOSS = 'boss'
TREASURE = 'treasure'
SHOP = 'shop'
SECRET = 'secret'
COMMON = 'common'
SPECIAL = [BOSS, TREASURE]
SEMI_SPECIAL = [SHOP, SECRET]
ROOM_TYPES = [STARTING, BOSS, TREASURE, SHOP, SECRET, COMMON]

rooms_by_type: dict[str, int] = {BOSS:BOSS_ROOMS,
                                 TREASURE:TREASURE_ROOMS,
                                 SHOP:SHOP_ROOMS,
                                 SECRET:SECRET_ROOMS,
                                 COMMON:TOTAL_ROOMS - BOSS_ROOMS - TREASURE_ROOMS - SHOP_ROOMS - SECRET_ROOMS}