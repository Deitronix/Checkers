__author__ = 'Hannah'
from piece import Piece

import numpy as NP
def humanMove(move_coordinates):
    import gui
    print("in innerLogic")
    board = NP.arange(64).reshape(8, 8)
    boardNumberToContents= {1: board[1,0], 2: board[3,0], 3: board[5,0], 4: board[7,0],
                            5: board[0,1],6: board[2,1],7: board[4,1],8: board[6,1],
                            9: board[1,2], 10: board[3,2], 11: board[5,2], 12: board[7,2],
                            13: board[0,3], 14: board[2,3], 15: board[4,3], 16: board[6,3],
                            17:board[1,4], 18:board[3,4], 19:board[5,4], 20:board[7,4],
                            21:board[0,5], 22:board[2,5], 23:board[4,5], 24:board[6,5],
                            25:board[1,6],  26:board[3,6],  27:board[5,6],  28:board[7,6],
                            29:board[0,7], 30:board[2,7], 31:board[4,7], 32:board[6,7]}

    NumberToCoordinates= {1: (1,0), 2: (3,0), 3: (5,0), 4: (7,0),
                            5: (0,1),6: (2,1),7: (4,1),8: (6,1),
                            9: (1,2), 10: (3,2), 11: (5,2), 12: (7,2),
                            13: (0,3), 14: (2,3), 15: (4,3), 16: (6,3),
                            17:(1,4), 18:(3,4), 19:(5,4), 20:(7,4),
                            21:(0,5), 22:(2,5), 23:(4,5), 24:(6,5),
                            25:(1,6),  26:(3,6),  27:(5,6),  28:(7,6),
                            29:(0,7), 30:(2,7), 31:(4,7), 32:(6,7)}


   # move_coordinates = gui.getCoordinates()
    #check first value
    print ("before conversions")
    coordinate1= int(move_coordinates[0])
    pieceToMove =  boardNumberToContents[coordinate1]
    print(coordinate1)
    print ("before if")
    if gui.board[pieceToMove] != Piece:
        print ("Error, you must start with a square with one of your pieces.")
        print(pieceToMove)






