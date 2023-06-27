opperations:list[tuple[int, int]] = [(0,0), (1, 0), (0, 1), (-1, 0), (0, -1)]   # common transformation opperations

class Coord():
    def __init__(self, x: int, y: int) -> None:
        self.x = x
        self.y = y
        self.value = (self.x, self.y)

    def is_equal(self, comparison: tuple[int, int]):
        """Checks to see if self is equal to a given coord value (can't have own class type in args)

        Args:
            comparison (tuple[int, int]): Coord value to be compared

        Returns:
            bool: True if they are equal
        """
        if self.value == comparison:
            return True
        else:
            return False

    def is_adjacent(self, comparison):
        """Checks to see if adjacent to another Coord

        Args:
            comparison (Coord): Coord to check if adjacent
        """
        if comparison in self.get_adjacent():
            return True
        else:
            return False

    def __str__(self) -> str:
        return(f'{self.value}')

    def get_adjacent(self):
        """returns all adjacent coords

        Returns:
            list[Coord]: All adjacent coords
        """
        adjacent: list[Coord] = []
        for tx, ty in opperations:
            adj = Coord(self.x + tx, self.y + ty)
            if not self.is_equal(adj.value):
                adjacent.append(adj)
        return(adjacent)