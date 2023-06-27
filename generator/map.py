import pygame
from .constants import *
from .room import Room

from .Coord import Coord

class Map():
    def __init__(self) -> None:
        self.rooms: dict[Coord, Room] = {}
        for col in range(COL):  # dict of  col, row, room
            for row in range(ROW):
                coord = Coord(col, row)
                self.rooms[coord.value] = None

    def drawMap(self, win:pygame.Surface):
        """Draw the map, which is all tiles

        Args:
            win (pygame.Surface): the window to be drawn on
        """
        win.fill(BLACK)
        for room in self.rooms.values():
            if room is not None: room.draw(win)

    def get_room(self, coord: Coord):
        """Return a Room object if it exists at the given coordinates

        Args:
            col (int): what column is being checked for a room
            row (int): what row is being checked for a room

        Returns:
            Room|None: A Room object if it exists at the given location
        """
        return self.rooms[coord.value]

    def add_room(self, room: Room):
        """Add a Room object to the map

        Args:
            room (Room): the Room to be added
        """
        if self.rooms[room.coord.value] is None:
            self.rooms[room.coord.value] = room
        else:
            raise Exception(f'There is already a room at {room.coord}')

    def get_rooms(self) -> list[Room]:
        """Returns a list of all Room objects contained in the map

        Returns:
            list[Room]: All Room objects contained in the map
        """
        rooms: list[Room] = []
        for room in self.rooms.values():
            if room is not None: rooms.append(room)
        return(rooms)

    def get_size(self) -> int:
        """Returns how many Room objects currently occupy the map

        Returns:
            int: Amount of current Room objects currently occupy the map
        """
        rooms = self.get_rooms()
        return len(rooms)
    
    # def get_adjacent(self):
    
    def get_all_rooms_by_type(self) -> dict[str, list[Room]]:
        """Returns a dictionary of all room types

        Returns:
            dict[str, list[Room]]: A dictionary of all types of rooms as keys, and all rooms in the map are in a list of their type
        """
        rooms: dict[str, list[Room]] = {}
        for type in ROOM_TYPES:
            rooms.update({type:[]})
        for room in self.get_rooms():
            rooms[room.type].append(room)
        return rooms
    
    def get_room_by_type(self, type: str) -> list[Room]:
        """Returns all rooms of a given type

        Args:
            type (str): the type of room being searched for

        Returns:
            list[Room]: a list of all rooms of the given type
        """
        rooms = []
        for room in self.get_rooms():
            if room.type == type:
                    rooms.append(room)
        return rooms

    def inbounds(self, coord: Coord) -> bool:
        """Check if a given coordinate is in bounds of the map

        Args:
            coord (tuple[int, int]): the coord to be checked

        Returns:
            bool: True if the coordinate is inbounds
        """
        x, y = coord.x, coord.y
        if 0 <= x < COL and 0 <= y < ROW:
            return True 
        else: 
            return False
        
    def clear(self):
        """Removes all rooms from the map."""
        for col in range(COL):  # dict of  col, row, room
            for row in range(ROW):
                coord = Coord(col, row)
                self.rooms[coord.value] = None

    def get_new_adjacent(self, type:str) -> set[Coord]:
        """_summary_

        Args:
            type (str): _description_

        Returns:
            set[tuple[int, int]]: _description_
        """
        special = True if type in SPECIAL else False
        secret = True if type == SECRET else False

        rooms = self.get_all_rooms_by_type()
        
        used_coords: set[Coord] = set()
        for room_list in rooms.values():
            for room in room_list:
                used_coords.add(room.coord)
        
        special_rooms:list[Room] = []
        for s_tag in SPECIAL:
            s_rooms = rooms[s_tag]
            special_rooms.extend(s_rooms)
        
        special_coords: set[Coord] = set()    # coords of special rooms, i.e. coords that can only have 1 adjacent each and already do
        for special_room in special_rooms:
            coords = special_room.coord
            special_coords.add(coords)

        potential_coords: set[Coord] = set()
        for used_coord in used_coords:
            if secret and used_coord not in [r.coord for r in rooms[COMMON]]:
                continue
            for adj in used_coord.get_adjacent():
                if not adj.value in [used.value for used in used_coords]:
                    potential_coords.add(adj)
        
        if special: # remove rooms with more than 1 adjacency for special rooms
            to_remove = []
            for p_coord in potential_coords:
                adjacencies = 0
                for adj_coord in p_coord.get_adjacent():
                    if adj_coord in potential_coords:
                        adjacencies += 1
                    if adjacencies > 1: break
                if adjacencies > 1: to_remove.append(p_coord)

            for r_coord in to_remove:
                potential_coords.discard(r_coord)

        
        useable_coords: set[Coord] = set()
        
        for potential_coord in potential_coords:
            special_adjacent = False
            if potential_coord not in used_coords and self.inbounds(potential_coord):   # unused and inbounds
                for special_coord in special_coords:
                    if potential_coord.is_adjacent(special_coord) and not secret: special_adjacent = True
                if not special_adjacent: useable_coords.add(potential_coord)

        return(useable_coords)