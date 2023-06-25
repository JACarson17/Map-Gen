import pygame
from .constants import *
from .room import Room

class Map():
    def __init__(self) -> None:
        self.rooms: dict[int, dict[int, Room]] = {}
        for col in range(COL):  # dict of  col, row, room
            self.rooms[col] = {}
            for row in range(ROW):
                self.rooms[col][row] = None

    def drawMap(self, win:pygame.Surface):
        win.fill(BLACK)
        for col in self.rooms.values():
            for row in col.values():
                if row is not None: row.draw(win)

    def get_room(self, col: int, row: int):
        return self.rooms[col][row]

    def add_room(self, room: Room):
        r = room.get_row()
        c = room.get_col()
        col = self.rooms.get(c)
        col.update({r:room})
        pass

    def get_rooms(self) -> list[Room]:
        rooms: list[Room] = []
        for col in self.rooms.values():
            for room in col.values():
                if room is not None: rooms.append(room)
        return(rooms)

    def get_size(self) -> int:
        rooms = self.get_rooms()
        return len(rooms)
    def get_all_rooms_by_type(self):
        rooms: dict[str, list[Room]] = {}
        for type in ROOM_TYPES:
            rooms.update({type:[]})
        for col in self.rooms.values():
            for room in col.values():
                if room is not None: rooms[room.type].append(room)
        return rooms
    
    def get_room_by_type(self, type: str) -> list[Room]:
        rooms = []
        for col in self.rooms.values():
            for room in col.values():
                if room and room.type == type:
                    rooms.append(room)
        return rooms

    def is_adjacent(self, coord1:tuple[int, int], coord2: tuple[int, int]):
        opperations:list[tuple[int, int]] = [(1, 0), (0, 1), (-1, 0), (0, -1)]
        c1 = coord1[0]
        r1 = coord1[1]

        for tc, tr in opperations:
            nc, nr = c1 + tc, r1 + tr
            if (nc, nr) == coord2:
                return True
        return False

    def inbounds(self, coord:tuple[int, int]):
        c, r = coord[0], coord[1]
        if 0 <= r < ROW and 0 <= c < COL:
            return True 
        else: 
            return False
        
    def clear(self):
        for col in range(COL):  # dict of  col, row, room
            self.rooms[col] = {}
            for row in range(ROW):
                self.rooms[col][row] = None

    def get_new_adjacent(self, type:str) -> set[tuple[int, int]]:
        opperations:list[tuple[int, int]] = [(0,0), (1, 0), (0, 1), (-1, 0), (0, -1)]
        rooms = self.get_all_rooms_by_type()
        
        used_coords: set[tuple[int, int]] = set()
        for room_list in rooms.values():
            for room in room_list:
                used_coords.add(room.get_coords())
        
        special = True if type in SPECIAL else False
        secret = True if type == SECRET else False
        special_rooms:list[Room] = []
        for s_tag in SPECIAL:
            s_rooms = rooms[s_tag]
            special_rooms.extend(s_rooms)
        special_coords: set[tuple[int, int]] = set()    # coords of special rooms, i.e. coords that can only have 1 adjacent each and already do
        
        for special_room in special_rooms:
            coords = special_room.get_coords()
            special_coords.add(coords)

        potential_coords: set[tuple[int, int], int] = set()
        for used_c, used_r in used_coords:
            if secret and (used_c, used_r) not in [r.get_coords() for r in rooms[COMMON]]:
                continue
            for new_c, new_r in opperations:
                c, r = used_c + new_c, used_r + new_r
                coord = (c, r)
                potential_coords.add(coord)
        
        if special:
            to_remove = []
            for coord_c, coord_r in potential_coords:
                adjacencies = 0
                for tc, tr in opperations:
                    check_c, check_r = coord_c + tc, coord_r + tr
                    if self.inbounds((check_c, check_r)) and self.get_room(check_c, check_r) is not None:
                        adjacencies += 1
                if adjacencies > 1:
                    to_remove.append((coord_c, coord_r))

            for coord in to_remove:
                potential_coords.discard(coord)

        
        useable_coords: set[tuple(int, int)] = set()
        
        for potential_coord in potential_coords:
            special_adjacent = False
            if potential_coord not in used_coords and self.inbounds(potential_coord):   # unused and inbounds
                for special_coord in special_coords:
                    if self.is_adjacent(potential_coord, special_coord) and not secret: special_adjacent = True
                if not special_adjacent: useable_coords.add(potential_coord)

        return(useable_coords)