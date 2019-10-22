"""Definition of Grid class"""

import os
import object as ob
import interaction as it
import utility as ut

class Grid:
    """Class gathering main methods
    """

    def __init__(self, path: str) -> None:
        self.obj_list = ut.Array()
        self.character_list, self.height, self.width = self.obj_list.create_from_template(path)
        self.nb_player = len(self.character_list)
        self.win = False
        self.message_for_player = ""
        self.character_just_died = False

    def get_character(self) -> int:
        """Function asking for a
        valid number of character to
        move
        """
        valid_name = False
        while not valid_name:
            index_character = str(input('Who should move ?\n'))
            try:
                moving_character = self.character_list[int(index_character)]
                valid_name = True
            except KeyError:
                names = ""
                for character in self.character_list:
                    names += str(character) + ", "
                names = names[:-2] + "."
                message = "character(s) still alive is(are): " + names
                print(message)
        return int(index_character), moving_character

    def move(self, index_character: int, moving_character: ob.Character, action: str) -> None:
        """Displace moving_character
        according to action
        """
        str_to_displacement = {'z': (0, 1), '^': (0, 1), 'q': (-1, 0), '<': (-1, 0),
                               's': (0, -1), 'v': (0, -1), 'd': (1, 0), '>': (1, 0)}
        for char in action: #Browsing string
            (d_x, d_y) = str_to_displacement[char]
            inter = it.Interaction(self, index_character,
                                   moving_character, d_x, d_y)
            inter.interaction()
            # if a character dies, we do not execute the end of the action
            if self.character_just_died:
                break

    def wincheck(self) -> int:
        """Returns 1 if the player wins, -1
        if he loses, 0 else.
        """
        if self.win:
            self.message_for_player = "You win :)"
            return 1
        if len(self.character_list) == 0:  # No more character alive
            self.message_for_player = "You lose :("
            return -1
        return 0

def display(self) -> None:
        """Displays grid and clear terminal
        (in linux)
        """
        text = ""
        for _y in range(self.height-1, -1, -1):
            for _x in range(self.width):
                objtmp = self.obj_list[_x, _y]
                text += objtmp.representation
            text += '\n'
        os.system("clear")
        print(text)
        print(self.message_for_player)

    def play(self) -> None:
        """Function structuring the
        game
        """
        self.character_just_died = False
        index_character, moving_character = self.get_character()
        action = ut.get_action()
        while action != "c":  # while not changing character:
            self.message_for_player = ""
            self.move(index_character, moving_character, action)
            self.display()
            if self.wincheck() != 0:
                self.display()  # To see "You win/ You lose" message
                break
            if self.character_just_died:
                break  # It is necessary to change character
            action = ut.get_action()

# Last functions are useful for game version in accordance with the exercise.

    def basic_wincheck(self) -> int:
        """Returns 1 if the player wins, -1
        if he loses, 0 else.
        """
        if self.win:
            return 1
        if self.character_just_died:
            return -1
        return 0

    def basic_get_action(self) -> str:
        """Function asking for a valid
        action to do
        """
        valid_action = False
        character_numbers = [str(i+1) for i in range(self.nb_player)]
        while not valid_action:
            action = str(
                input('use ^<v> to move and numbers to select characters\n'))
            if len(action) == 0:
                return ""
            valid_action = True
            if action[0] not in character_numbers:
                valid_action = False
            for char in action:
                if char not in ["^", "<", "v", ">"] + character_numbers:
                    valid_action = False
                if not valid_action:
                    print('enter a valid action !')
        return action

    def basic_move(self, action: str) -> None:
        """Interpretes order given by
        the player and move characters.
        """
        move_dict = {'^': (0, 1), '<': (-1, 0), 'v': (0, -1),
                     '>': (1, 0)}
        for i in range(self.nb_player):
            move_dict[str(i)] = i
        for char in action:
            if isinstance(move_dict[char], tuple):
                (d_x, d_y) = move_dict[char]
                inter = it.Interaction(
                    self, index_character, moving_character, d_x, d_y)
                inter.interaction()
            if isinstance(move_dict[char], int):
                moving_character = self.character_list[move_dict[char]]
                index_character = move_dict[char]
            if self.character_just_died:
                break

    def basic_play(self) -> None:
        """Function structuring the game
        """
        action = self.basic_get_action()
        self.message_for_player = ""
        self.basic_move(action)
        self.display()
