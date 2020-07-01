"""Definition of Grid class"""

import os
import object as ob
import interaction as it
import utility as ut


class Grid:
    """Class gathering main methods"""

    def __init__(self, path: str) -> None:
        self.obj_list = ut.Array()
        self.character_list, self.height, self.width = self.obj_list.create_from_template(
            path)
        self.nb_player = len(self.character_list)
        self.win = False
        self.moving_character = "1"
        self.message_for_player = ""
        self.character_just_died = False

    def wincheck(self) -> None:
        """Returns 1 if player
        has won, -1 if he lost,
        else 0
        """
        if self.win:
            self.message_for_player = "You win :)"
            return 1
        if len(self.character_list) == 0:  # No more character alive
            self.message_for_player = "You lose :("
            return -1
        return 0

    def get_action(self, char: str) -> str:
        """Function switching character
        or calling move fonction
        """
        if char == "c":
            remaining_characters = list(self.character_list.keys())
            if int(self.moving_character) >= max(remaining_characters):
                self.moving_character = str(remaining_characters[0])
            else:
                self.moving_character = str(int(self.moving_character) + 1)
        else:
            action = char
            self.move(action)

    def move(self, action: str) -> None:
        """Interpretes order given by
        get_action and move character.
        """
        move_dict = {'^': (0, 1), '<': (-1, 0), 'v': (0, -1),
                     '>': (1, 0)}
        for i in range(self.nb_player):
            move_dict[str(i+1)] = i+1
        for char in action:
            if isinstance(move_dict[char], tuple):
                (d_x, d_y) = move_dict[char]
                inter = it.Interaction(
                    self, index_character, moving_character, d_x, d_y)
                inter.interaction()
            if isinstance(move_dict[char], int):
                moving_character = self.character_list[move_dict[char]]
                index_character = move_dict[char]
        self.wincheck()
