"""Test module"""

import grid as gr
import object as ob
import interaction as it


def add_list(list_1: list, list_2: list) -> list:
    """A simple function returning
    the sum of two vectors seen as
    lists"""
    new_list = []
    assert len(list_1) == len(list_2)
    for i in range(len(list_1)):
        new_list.append(list_1[i] + list_2[i])
    return new_list


G_1 = gr.Grid("./level1.txt")

def test_level1():
    """Function testing if
    action_1 is a valid solution
    of level 1
    """
    action_1 = "1>>>>>>^>>>>>>>^^^^<<<<<<<<<<"
    G_1.basic_move(action_1)
    assert G_1.wincheck() == 1


G_2 = gr.Grid("./level2.txt")

def test_level2():
    """Function testing if
    action_2 is a valid solution
    of level 2"""
    action_2 = "3>vvv>v<<<<<<<^^>>v>v<<<<1vv>^^^<^^>vv<v>>>>>>>>>>>>>>>>>>>>>>>>>>^>vvv>2<<<v<<^<vvvvvvvvvvvvvvvvvvvvvvv<<<<<<<<<<^^^^^^^^<^^^^^^>"
    G_2.basic_move(action_2)
    assert G_2.wincheck() == 1


G_TEST = gr.Grid("./level3.txt") # Test level


def test_move():
    """Function testing if
    a character moves as the
    player wishes
    """
    character_0 = G_TEST.character_list[0]
    action = ["0^", "0<", "0v", "0>"]
    check_action = [(0, 1), (-1, 0), (0, -1), (1, 0)]
    for i in range(4):
        old_position = (character_0.x_obj, character_0.y_obj)
        G_TEST.basic_move(action[i])
        new_position = [character_0.x_obj, character_0.y_obj]
        assert add_list(old_position, check_action[i]) == new_position


def test_push_box():
    """Function testing if
    a character heading towards
    a box pushes the box
    """
    character_1 = G_TEST.character_list[1]
    x_old_character, y_old_character = character_1.x_obj, character_1.y_obj
    x_old_box, y_old_box = character_1.x_obj + 1, character_1.y_obj
    box = G_TEST.obj_list[x_old_box, y_old_box]
    action = "1>"
    G_TEST.basic_move(action)
    assert (x_old_character + 1,
            y_old_character) == (character_1.x_obj, character_1.y_obj)
    assert (x_old_box + 1, y_old_box) == (box.x_obj, box.y_obj)


def test_wall_block():
    """Function testing if
    a wall blocks a character
    """
    character_2 = G_TEST.character_list[2]
    action = ["0^", "0<", "0v", "0>"]
    old_position = (character_2.x_obj, character_2.y_obj)
    for i in range(4):
        G_TEST.basic_move(action[i])
        assert old_position == (character_2.x_obj, character_2.y_obj)


def test_destroying_hole():
    """Function testing if
    a box pushed towards a
    depth 1 hole destroys the
    hole
    """
    character_3 = G_TEST.character_list[3]
    x_old_character, y_old_character = character_3.x_obj, character_3.y_obj
    action = "3>"
    G_TEST.basic_move(action)
    object_to_the_right = G_TEST.obj_list[character_3.x_obj +
                                          1, character_3.y_obj]
    assert isinstance(object_to_the_right, ob.Void)
    assert (x_old_character + 1,
            y_old_character) == (character_3.x_obj, character_3.y_obj)


def test_fill_hole():
    """Function testing if
    a box pushed towards a
    depth 2 hole reduces its
    depth
    """
    character_4 = G_TEST.character_list[4]
    x_old_character, y_old_character = character_4.x_obj, character_4.y_obj
    action = "4>"
    G_TEST.basic_move(action)
    object_to_the_right = G_TEST.obj_list[character_4.x_obj +
                                          1, character_4.y_obj]
    object_even_more_to_the_right = G_TEST.obj_list[character_4.x_obj +
                                                    2, character_4.y_obj]
    assert (x_old_character, y_old_character) == (
        character_4.x_obj, character_4.y_obj)
    assert isinstance(object_to_the_right, ob.Void)
    assert isinstance(object_even_more_to_the_right, ob.Hole)
    assert object_even_more_to_the_right.depth == 1


def test_turnstile():
    """Function testing if
    a turnstile works as
    expected"""
    character_5 = G_TEST.character_list[5]
    displacements = [(2, 0), (0, 2), (-2, 0), (0, -2)]
    actions = ["5>", "5^", "5<", "5v"]
    for i in range(4):
        old_coords = (character_5.x_obj, character_5.y_obj)
        G_TEST.basic_move(actions[i])
        assert add_list(old_coords, displacements[i]) == [
            character_5.x_obj, character_5.y_obj]


def test_turnstile_moving_condition_1():
    """Function testing if
    a non rotation condition
    works as expected
    """
    character_6 = G_TEST.character_list[6]
    x_old_character, y_old_character = character_6.x_obj, character_6.y_obj
    x_old_arm, y_old_arm = x_old_character + 1, y_old_character
    arm = G_TEST.obj_list[x_old_arm, y_old_arm]
    x_old_box, y_old_box = x_old_arm + 1, y_old_arm + 1
    box = G_TEST.obj_list[x_old_box, y_old_box]
    action = "6>"
    interaction = it.Interaction(G_TEST, 6, character_6, 1, 0)
    assert not interaction.can_rotate()[0]
    G_TEST.basic_move(action)
    assert (x_old_character, y_old_character) == (
        character_6.x_obj, character_6.y_obj)
    assert (x_old_arm, y_old_arm) == (arm.x_obj, arm.y_obj)
    assert (x_old_box, y_old_box) == (box.x_obj, box.y_obj)


def test_turnstile_moving_condition_2():
    """Function testing if
    another non rotation
    condition works as expected
    """
    character_7 = G_TEST.character_list[7]
    x_old_character, y_old_character = character_7.x_obj, character_7.y_obj
    x_old_arm, y_old_arm = x_old_character + 1, y_old_character
    arm = G_TEST.obj_list[x_old_arm, y_old_arm]
    x_old_box, y_old_box = x_old_arm + 1, y_old_arm
    box = G_TEST.obj_list[x_old_box, y_old_box]
    action = "7>"
    interaction = it.Interaction(G_TEST, 7, character_7, 1, 0)
    assert not interaction.can_rotate()[0]
    G_TEST.basic_move(action)
    assert (x_old_character, y_old_character) == (
        character_7.x_obj, character_7.y_obj)
    assert (x_old_arm, y_old_arm) == (arm.x_obj, arm.y_obj)
    assert (x_old_box, y_old_box) == (box.x_obj, box.y_obj)


def test_win():
    """Function testing if
    a character walking on
    a door wins the game"""
    action = "8>"
    G_TEST.basic_move(action)
    assert G_TEST.basic_wincheck() == 1

G_TEST2 = gr.Grid("./level3.txt")

def test_defeat():
    """Function testing if
    a character walking on
    a hole loses the game"""
    action = "9>"
    G_TEST2.basic_move(action)
    assert G_TEST2.basic_wincheck() == -1
