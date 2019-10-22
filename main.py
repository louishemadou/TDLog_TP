"""Main module of the game"""

import grid as gr

print('TDLog TD2 Louis Hémadou')
LVL_NUMBER = str(
    input('Type 1 for an easy level, 2 for a (very) hard level.\n'))
MODE = str(input("Type 1 for displacement management in accordance with the exercise, 2 for an improved displacement management.\n"))

if MODE in ('1', '2'):
    if LVL_NUMBER in ('1', '2', '3'):
        G = gr.Grid("./level" + LVL_NUMBER + ".txt")
        G.display()
        if MODE == '1':
            while G.basic_wincheck() == 0:
                G.basic_play()
        if MODE == "2":
            while G.wincheck() == 0:
                G.play()
    else:
        print("This level has not been created yet !")
else:
    print("Enter a valid mode !")
