"""Definition of all the objects in the game"""

class Object:
    """An object has coordinates
    and symbol for representation
    """

    def __init__(self, x_obj: int, y_obj: int, representation: str) -> None:
        self.x_obj = x_obj
        self.y_obj = y_obj
        self.representation = representation


class Character(Object):
    """Object character, represented
    by a figure
    """

    def __init__(self, x_character: int, y_character: int, representation: str) -> None:
        Object.__init__(self, x_character, y_character, representation)


class Box(Object):
    """Object Box, represented
    by a *
    """

    def __init__(self, x_box: int, y_box: int) -> None:
        Object.__init__(self, x_box, y_box, "*")


class Hole(Object):
    """Object Hole, represented
    by a o
    """

    def __init__(self, x_hole: int, y_hole: int, depth: int) -> None:
        Object.__init__(self, x_hole, y_hole, None)
        self.depth = depth
        self.representations = {1 : "o", 2: "O"}
        self.representation = self.representations[self.depth]

    def reduce_depth(self):
        """Reduces depth of
        the hole by one"""
        self.depth = self.depth - 1
        self.representation = self.representations[self.depth]


class Wall(Object):
    """Object Wall, represented
    by a  #
    """

    def __init__(self, x_wall: int, y_wall: int) -> None:
        Object.__init__(self, x_wall, y_wall, "#")


class Door(Object):
    """Object Door, represented
    by a @
    """

    def __init__(self, x_door: int, y_door: int) -> None:
        Object.__init__(self, x_door, y_door, "@")


class Void(Object):
    """Object Void, represented
    by a space
    """

    def __init__(self, x_void: int, y_void: int) -> None:
        Object.__init__(self, x_void, y_void, " ")


class TurnstileAxis(Object):
    """Object TurnstileAxis, represented
    by a %
    """

    def __init__(self, x_turn_axis: int, y_turn_axis: int) -> None:
        Object.__init__(self, x_turn_axis, y_turn_axis, "%")


class TurnstileBloc(Object):
    """Object TurnstileBloc, represented
    by a °
    """

    def __init__(self, x_turn_bloc: int, y_turn_bloc: int) -> None:
        Object.__init__(self, x_turn_bloc, y_turn_bloc, "°")
