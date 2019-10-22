"""Contains Array, a class managing objects in the grid"""

import object as ob

class Array:
    """2D array with adapted methods
    for objects

    """

    def __init__(self) -> None:
        # List of objects
        self.list = []
        # keys = objects coordinates. values = index of objects in list
        self.coord_to_index = {}

    def add_obj(self, obj) -> None:
        """Add obj in object list and
        in dictionnary
        """
        if (obj.x_obj, obj.y_obj) in self.coord_to_index.keys():
            # If there is already an object at this position:
            raise NameError("Object overlap")
        self.list.append(obj)
        index = len(self.list) - 1
        self.coord_to_index[obj.x_obj, obj.y_obj] = index

    def __setitem__(self, obj1: ob.Object, obj2: ob.Object) -> None:
        """Change type of obj1 to type of obj2
        """
        index1 = self.coord_to_index[obj1.x_obj, obj1.y_obj]
        self.list[index1] = obj2

    def __getitem__(self, key) -> ob.Object:
        """Return object having key for
        coordinates
        """
        (x_obj, y_obj) = key
        index = self.coord_to_index[(x_obj, y_obj)]
        return self.list[index]

    def swap_obj(self, obj1: ob.Object, obj2: ob.Object) -> None:
        """Saps positions of obj1 and obj2 and
        updates dictionnary
        """
        # Collecting information
        index1 = self.coord_to_index[obj1.x_obj, obj1.y_obj]
        index2 = self.coord_to_index[obj2.x_obj, obj2.y_obj]
        # Swapping coordinates
        x_obj1, y_obj1 = obj1.x_obj, obj1.y_obj
        x_obj2, y_obj2 = obj2.x_obj, obj2.y_obj
        obj1.x_obj, obj1.y_obj = x_obj2, y_obj2
        obj2.x_obj, obj2.y_obj = x_obj1, y_obj1
        # Updating dictionnary
        self.coord_to_index[x_obj1, y_obj1] = index2
        self.coord_to_index[x_obj2, y_obj2] = index1

    def create_from_template(self, path: str) -> dict:
        """Creates a grid based on
        path, a txt file"""
        lvlfile = open(path, 'r')
        # These two lines represent grid size
        width = int(lvlfile.readline())
        height = int(lvlfile.readline())
        # Third line represent the number of players
        nb_player = int(lvlfile.readline())
        check_char = 0  # To count number of characters
        check_door = False
        character_representation = [
            str(x) for x in range(nb_player+1)]
        character_list = {}
        # Browsing file from bottom to top  and from left to right
        for _y in range(height-1, -1, -1):
            line = str(lvlfile.readline())
            for _x in range(width):
                if line[_x] in character_representation:
                    # Creating character
                    character = ob.Character(_x, _y, line[_x])
                    # Adding character to object list
                    self.add_obj(character)
                    # Then adding it to character list
                    character_list[int(line[_x])] = character
                    check_char += 1
                if line[_x] == "*":
                    self.add_obj(ob.Box(_x, _y))
                if line[_x] == "o":
                    self.add_obj(ob.Hole(_x, _y, 1))
                if line[_x] == "O":
                    self.add_obj(ob.Hole(_x, _y, 2))
                if line[_x] == "#":
                    self.add_obj(ob.Wall(_x, _y))
                if line[_x] == "@":
                    self.add_obj(ob.Door(_x, _y))
                    check_door = True
                if line[_x] == " ":
                    self.add_obj(ob.Void(_x, _y))
                if line[_x] == "%":
                    self.add_obj(ob.TurnstileAxis(_x, _y))
                if line[_x] == "°":
                    self.add_obj(ob.TurnstileBloc(_x, _y))
        # Checking the presence of a door
        if not check_door:
            raise NameError("Missing door")
        # Checking the number of characters
        if not check_char == nb_player:
            raise NameError("Missing character")
        # Checking that turnstiles are well defined
        directions = [(0, 1), (1, 0), (0, -1), (-1, 0),
                      (1, 1), (-1, 1), (1, -1), (-1, -1)]
        for _x in range(width):
            for _y in range(height):
                obj = self[_x, _y]
                if isinstance(obj, ob.TurnstileBloc):
                    nb_axis = 0
                    for dire in directions:
                        x_neighbour = obj.x_obj + dire[0]
                        y_neighbour = obj.y_obj + dire[1]
                        neighbour = self[x_neighbour, y_neighbour]
                        if isinstance(neighbour, ob.TurnstileAxis):
                            nb_axis += 1
                    if nb_axis != 1:
                        raise NameError('Ambiguous definition of turnstile')
        return character_list, height, width

def get_action() -> str:
    """Function asking for a valid action to do:
    moving character of changing selected
    character.
    """
    valid_action = False
    while not valid_action:
        action = str(
            input('use zqsd or ^<v> to move or type (only) c to change moving character \n'))
        valid_action = True
        for char in action:
            if char not in ["z", "q", "s", "d", "^", "<", "v", ">", "c"]:
                valid_action = False
            if "c" in action and len(action) > 1:
                valid_action = False
            if not valid_action:
                print('enter a valid action !')
    return action
