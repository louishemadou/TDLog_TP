"""Here is gathered everything concerning user interface."""
from PyQt5.QtWidgets import QWidget, QLabel, QGridLayout, QPushButton, QMessageBox
from PyQt5.QtGui import QPixmap
import object as ob


class GUI:
    """Handles graphical user interface using PyQt5"""

    def __init__(self, grid, app):
        self.app = app
        self.window = QWidget()  # Main window
        self.window.setWindowTitle("TDLog Louis Hémadou")
        self.grid = grid  # The grid which contains all the elements
        self.elements = [
            [None]*self.grid.height for _ in range(self.grid.width)]
        self.layout = QGridLayout(self.window)
        self.layout.setSpacing(0)
        self.selected_character = QWidget()  # Indicates which character is selected
        self.selected_character_label = QLabel()
        self.selected_character_label.setText(
            "Character " + self.grid.moving_character + " is selected")
        self.layout.addWidget(self.selected_character_label,
                              1, self.grid.height + 1, 1, self.grid.height + 2)
        self.create_game()
        self.create_buttons()

    def create_game(self):
        """This function initialises
        the grid where pictures
        will be
        """
        for _x in range(self.grid.width):
            for _y in range(self.grid.height):
                label = QLabel()
                self.elements[_x][_y] = label
                self.layout.addWidget(label, self.grid.height - _y, _x)

    def create_buttons(self):
        """This function creates
        and places the usefull buttons"""
        btn_left = QPushButton("Left", self.window)
        self.layout.addWidget(
            btn_left, 1/2 * self.grid.width, self.grid.height + 1)
        btn_left.clicked.connect(self.move_left)

        btn_right = QPushButton("Right", self.window)
        self.layout.addWidget(
            btn_right, 1/2 * self.grid.width, self.grid.height + 3)
        btn_right.clicked.connect(self.move_right)

        btn_up = QPushButton("Up", self.window)
        self.layout.addWidget(
            btn_up, 1/2 * self.grid.width - 1, self.grid.height + 2)
        btn_up.clicked.connect(self.move_up)

        btn_down = QPushButton("Down", self.window)
        self.layout.addWidget(
            btn_down, 1/2 * self.grid.width + 1, self.grid.height + 2)
        btn_down.clicked.connect(self.move_down)

        btn_change = QPushButton("Change", self.window)
        self.layout.addWidget(
            btn_change, 1/2 * self.grid.width, self.grid.height + 2)
        btn_change.clicked.connect(self.change_character)

    def move_left(self):
        """Moves the selected
        character by one case
        on the left
        """
        self.grid.get_action(self.grid.moving_character + "<")
        self.update_and_display()

    def move_right(self):
        """Moves the selected
        character by one case
        on the right
        """
        self.grid.get_action(self.grid.moving_character + ">")
        self.update_and_display()

    def move_up(self):
        """Moves the selected
        character by one case
        at the top
        """
        self.grid.get_action(self.grid.moving_character + "^")
        self.update_and_display()

    def move_down(self):
        """Moves the selected
        character by one case
        at the bottom
        """
        self.grid.get_action(self.grid.moving_character + "v")
        self.update_and_display()

    def change_character(self):
        """Switches to the next
        character
        """
        self.grid.get_action("c")
        self.update_and_display()

    def update_and_display(self):
        """Updates the interface in
        accordance with character
        displacements
        """
        character_to_picture = {1: "clementine.png",
                                2: "char2.png", 3: "char3.png", 4: "char4.png"}
        hole_to_picture = {1: "hole.png", 2: "deep_hole.png"}
        object_to_picture = {ob.Box: "crate.png", ob.Door: "door.png", ob.TurnstileBloc: "turnstile_block.png",
                             ob.TurnstileAxis: "turnstile_axis.png", ob.Wall: "feu.png", ob.Void: "empty.png"}
        for _x in range(self.grid.width):
            for _y in range(self.grid.height):
                if isinstance(self.grid.obj_list[_x, _y], ob.Character):
                    path = "./images/" + \
                        character_to_picture[self.grid.obj_list[_x, _y].number]
                elif isinstance(self.grid.obj_list[_x, _y], ob.Hole):
                    path = "./images/" + \
                        hole_to_picture[self.grid.obj_list[_x, _y].depth]
                else:
                    path = "./images/" + \
                        object_to_picture[type(self.grid.obj_list[_x, _y])]
                picture = QPixmap(path)
                self.elements[_x][_y].setPixmap(picture)
        self.window.show()
        if self.grid.wincheck() != 0:  # If the player won or lost:
            self.close_window()
        elif self.grid.character_just_died:  # If a character has just died
            self.grid.get_action("c")  # We switch to another character
        self.selected_character_label.setText(
            "Character " + self.grid.moving_character + " is selected")

    def close_window(self):
        """Displays endgame message
        and a button to close
        the application"""
        message_box = QMessageBox()
        win_or_lose_to_message = {1: "You win :)", -1: "You lose :("}
        message_box.setIcon(QMessageBox.Information)
        message_box.setText(win_or_lose_to_message[self.grid.wincheck()])
        message_box.setWindowTitle("Important information")
        message_box.setStandardButtons(QMessageBox.Ok)
        message_box.buttonClicked.connect(self.message_button_clicked)
        message_box.exec_()

    def message_button_clicked(self):
        """Closes the application
        """
        self.app.quit()
