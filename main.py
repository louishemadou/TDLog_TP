"""Main module of the game"""
import sys
from PyQt5.QtWidgets import QApplication
import grid as gr
import gui


G = gr.Grid("./level1.txt")
APP = QApplication(sys.argv)
GUI = gui.GUI(G, APP)
GUI.update_and_display()
sys.exit(APP.exec_())
