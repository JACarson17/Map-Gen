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

    def used_coords(self):
        used: set[Coord] = set()
        for room in self.rooms.values():
            if room: used.add(room.coord)
        return used

    def get_new_adjacent(self) -> set[Coord]:
        """returns a set of all coords adjacent to used coords

        Returns:
            set[Coord]: coords adjacent to used coords
        """

        potential_coords: set[Coord] = set()
        for used_coord in self.used_coords():
            # if special and used_coord not in [r.coord for r in rooms[COMMON]]:
            #     continue
            for adj in used_coord.get_adjacent():
                if not adj.value in [used.value for used in self.used_coords()] and self.inbounds(adj):
                    potential_coords.add(adj)
        
        return potential_coords