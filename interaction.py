"""Definition of Interaction class"""

import numpy as np
import object as ob


class Interaction:
    """Class managing characters evolution
    in grid.
    """

    def __init__(self, grid, index: int, character: ob.Character, d_x: int, d_y: int) -> None:
        self.grid = grid
        self.index_character = index
        self.moving_character = character
        self.d_x = d_x
        self.d_y = d_y
        self.target = self.grid.obj_list[
            self.moving_character.x_obj+d_x, self.moving_character.y_obj+d_y]

    def interaction_void(self) -> None:
        """Character interaction with a
        Void
        """
        self.grid.obj_list.swap_obj(self.moving_character, self.target)

    def interaction_hole(self) -> None:
        """Character interaction with a
        Hole
        """
        self.grid.message_for_player = "rip"
        x_dead_char = self.moving_character.x_obj
        y_dead_char = self.moving_character.y_obj
        void = ob.Void(x_dead_char, y_dead_char)
        # Replacing character by a Void
        self.grid.obj_list[self.moving_character] = void
        del self.grid.character_list[self.index_character]
        self.grid.character_just_died = True

    def interaction_door(self) -> None:
        """Character interaction with a
        Door"""
        self.grid.win = True

    def interaction_wall(self) -> None:
        """Character interaction with a
        Wall
        """
        self.grid.message_for_player = "I am too weak"

    def interaction_player(self) -> None:
        """Character interaction with another
        character
        """
        self.grid.message_for_player = "Outch !"

    def interaction_box(self) -> None:
        """Character interaction with a
        Box
        """
        assert(0 <= self.target.x_obj+self.d_x <= self.grid.width and 0 <=
               self.target.y_obj+self.d_y <= self.grid.height)
        x_beyond_target = self.target.x_obj + self.d_x
        y_beyond_target = self.target.y_obj + self.d_y
        beyond_target = self.grid.obj_list[  # Object on which we could push the box
            x_beyond_target, y_beyond_target]
        if isinstance(beyond_target, ob.Void):  # Simply pushing the box
            self.grid.obj_list.swap_obj(beyond_target, self.target)
            self.grid.obj_list.swap_obj(beyond_target, self.moving_character)
        elif isinstance(beyond_target, ob.Hole):
            if beyond_target.depth == 1:
                # Destroying box and hole
                void1 = ob.Void(self.target.x_obj, self.target.y_obj)
                void2 = ob.Void(x_beyond_target, y_beyond_target)
                self.grid.obj_list[self.target] = void1
                self.grid.obj_list[beyond_target] = void2
                # Then moving character
                self.grid.obj_list.swap_obj(void1, self.moving_character)
            else:
                # Reducing depth of the hole
                beyond_target.reduce_depth()
                # Destructing the box
                void = ob.Void(self.target.x_obj, self.target.y_obj)
                self.grid.obj_list[self.target] = void
        elif isinstance(beyond_target, ob.Box):
            # Impossible to push two boxes
            self.grid.message_for_player = "I am too weak"

    def get_arms(self) -> (list, ob.TurnstileAxis):
        """Function returning the turnstile
        which self.target belongs"""
        directions = [(0, 1), (1, 0), (0, -1), (-1, 0),
                      (1, 1), (-1, 1), (1, -1), (-1, -1)]
        for dire in directions:
            x_neighbour = self.target.x_obj + dire[0]
            y_neighbour = self.target.y_obj + dire[1]
            neighbour = self.grid.obj_list[x_neighbour, y_neighbour]
            if isinstance(neighbour, ob.TurnstileAxis):
                axis = neighbour
        arms = []
        for dire in directions[:4]:
            x_potential_arm = axis.x_obj + dire[0]
            y_potential_arm = axis.y_obj + dire[1]
            potential_arm = self.grid.obj_list[
                x_potential_arm, y_potential_arm]
            if isinstance(potential_arm, ob.TurnstileBloc):
                arms.append(potential_arm)
        return arms, axis

    def get_rotation(self) -> np.array:
        """Function returning the right
        rotation matrix"""
        axis = self.get_arms()[1]
        force = [self.d_x, self.d_y]  # "Force applied on the arm"
        o_m = [self.target.x_obj - axis.x_obj, self.target.y_obj - axis.y_obj]
        torque = o_m[0]*force[1] - o_m[1] * force[0]  # OM vectorial F
        if torque == 1:  # Anti clockwise rotation
            rotation = np.array([[0, -1], [1, 0]])
        if torque == -1:  # Clockwise rotation
            rotation = np.array([[0, 1], [-1, 0]])
        if torque == 0:  # No rotation
            rotation = np.array([[0, 0], [0, 0]])
        return rotation

    def can_rotate(self) -> (bool, list, list):
        """Function determining whether turnstile
        can rotate
        """
        arms, axis = self.get_arms()
        rotation = self.get_rotation()
        if rotation[1][0] == 0:
            return False
        coord_axis = np.array([[axis.x_obj], [axis.y_obj]])
        coord_arms = [np.array([[arm.x_obj], [arm.y_obj]])
                      for arm in arms]
        coord_new_arms = []
        # Collecting arm coordinates in the situation there turnstile rotates
        for i in range(len(arms)):
            coord_arm = coord_arms[i]
            coord_new_arms.append(
                np.dot(rotation, coord_arm - coord_axis) + coord_axis)
        can_rotate = True
        for i in range(len(arms)):
            coord_arm = coord_arms[i]
            coord_new_arm = coord_new_arms[i]
            # Object turnstile should push
            coord_front = coord_arm + coord_new_arm - coord_axis
            coord_character = np.array(
                [[self.moving_character.x_obj], [self.moving_character.y_obj]])
            obj_front = self.grid.obj_list[
                coord_front[0][0], coord_front[1][0]]
            if not (isinstance(obj_front, ob.Void) or (coord_front == coord_character).all()):
                can_rotate = False
            # Object being at the destination of the arm
            obj_target = self.grid.obj_list[
                coord_new_arm[0][0], coord_new_arm[1][0]]
            if not isinstance(obj_target, (ob.Void, ob.TurnstileBloc)):
                can_rotate = False
        return can_rotate, coord_arms, coord_new_arms

    def rotate(self) -> None:
        """Function rotating turnstile
        arms that should rotate
        """
        arms = self.get_arms()[0]
        coord_arms, coord_new_arms = self.can_rotate()[1:]
        nb_arm = len(coord_arms)
        for i in range(nb_arm):
            coord_arm = coord_arms[i]
            void = ob.Void(coord_arm[0][0], coord_arm[1][0])
            self.grid.obj_list[arms[i]] = void
        for i in range(nb_arm):
            coord_arm = coord_arms[i]
            coord_new_arm = coord_new_arms[i]
            x_new_arm = coord_new_arm[0][0]
            y_new_arm = coord_new_arm[1][0]
            void = self.grid.obj_list[x_new_arm, y_new_arm]
            arm = ob.TurnstileBloc(x_new_arm, y_new_arm)
            self.grid.obj_list[void] = arm
        x_new_target = self.moving_character.x_obj + 2*self.d_x
        y_new_target = self.moving_character.y_obj + 2*self.d_y
        new_target = self.grid.obj_list[x_new_target, y_new_target]
        self.grid.obj_list.swap_obj(self.moving_character, new_target)

    def interaction_turnstile(self) -> None:
        """Character interaction with a
        turnstile
        """
        if self.get_rotation()[1][0] != 0:
            condition = self.can_rotate()[0]
            if condition:
                self.rotate()
            else:
                self.grid.message_for_player = "Turnstile cannot move !"

    def interaction(self) -> None:
        """Function calling the right
        interaction function
        """
        if isinstance(self.target, ob.Void):
            self.interaction_void()
        elif isinstance(self.target, ob.Door):
            self.interaction_door()
        elif isinstance(self.target, ob.Hole):
            self.interaction_hole()
        elif isinstance(self.target, ob.Wall):
            self.interaction_wall()
        elif isinstance(self.target, ob.Character):
            self.interaction_player()
        elif isinstance(self.target, ob.Box):
            self.interaction_box()
        elif isinstance(self.target, ob.TurnstileBloc):
            self.interaction_turnstile()
