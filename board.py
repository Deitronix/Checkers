'''
Board.py - this file creates a representation of a game board and embodies all the game logic including
human and computer moving, jump pieces, kinging piece, and win conditions.
'''

from piece import Piece

import pygame
from collections import namedtuple
import copy

class Board:
    jumpFlag = 0 #to determine if the computer has made a jump
    locations = dict()
    black_pieces = list()
    white_pieces = list()
    img_folder = "img/"

    numberToCoordinates = {1: (1, 0), 2: (3, 0), 3: (5, 0), 4: (7, 0),
                           5: (0, 1), 6: (2, 1), 7: (4,1), 8: (6, 1),
                           9: (1, 2), 10: (3, 2), 11: (5, 2), 12: (7, 2),
                           13: (0, 3), 14: (2, 3), 15: (4, 3), 16: (6, 3),
                           17: (1, 4), 18: (3, 4), 19: (5, 4), 20: (7, 4),
                           21: (0, 5), 22: (2, 5), 23: (4, 5), 24: (6, 5),
                           25: (1, 6), 26: (3, 6), 27: (5, 6), 28: (7, 6),
                           29: (0,7), 30: (2, 7), 31: (4, 7), 32: (6, 7)}


    def __init__(self, screen, width, height):
        self.screen = screen
        self.width = width
        self.height = height


        self.boardimg = pygame.image.load(self.img_folder+"board.png")
        self.boardimg = pygame.transform.scale(self.boardimg, (width,height))
        self.boardrect = self.boardimg.get_rect()
        self.star = pygame.image.load(self.img_folder + "star.png")
        self.black_pieceimg = pygame.image.load(self.img_folder+"black_piece.png")
        self.white_pieceimg = pygame.image.load(self.img_folder+"white_piece.png")
        self.pcwidth = self.width//8
        self.pcheight = self.height//8

        # initializing black pieces
        x = 0
        y = 0

        while y < 3:
            x = 0
            while x < 8:

                if x % 2 != y % 2:
                    piece = Piece(screen=self.screen, is_white=False, pos=(x,y), width=self.pcwidth, height=self.pcheight, image=self.black_pieceimg)
                    self.locations[(x, y)] = piece
                    self.black_pieces.append(piece)
                x += 1
            y += 1

        # initializing white pieces
        x = 0
        y = 5
        while y < 8:
            x = 0
            while x < 8:
                if x % 2 != y % 2:
                    piece = Piece(screen = self.screen, is_white=True, pos=(x,y), width=self.pcwidth, height=self.pcheight, image=self.white_pieceimg)
                    self.locations[(x, y)] = piece
                    self.white_pieces.append(piece)
                x += 1
            y += 1

    def draw(self, inmenu):
            # -- DRAWING BOARD ---
            self.screen.blit(self.boardimg, self.boardrect)
            if not inmenu:
                for piece in self.black_pieces:
                    piece.draw()
                for piece in self.white_pieces:
                    #self.screen.blit(self.white_pc_img, (piece.pos[0]*self.width, (piece.pos[1])*self.height))
                    piece.draw()
                self.screen.blit(self.star, (0, 0))




#####################################################################################################################
    def human_controller(self, fromSquare, toSquare, player_is_white):
        fromCoord = self.numberToCoordinates[fromSquare]
        toCoord = self.numberToCoordinates[toSquare]
        fromPiece = self.locations.get(fromCoord, None)
        toPiece = self.locations.get(toCoord, None)

        if not self.validate_input(fromPiece, player_is_white):
           raise Exception ("Sorry, that is not a valid move")
        else:
            if fromPiece and not toPiece:
                if fromPiece.is_white:
                    if (toCoord[0] == fromCoord[0]+1 or toCoord[0] == fromCoord[0] - 1) and toCoord[1]== fromCoord[1]-1:
                         self.single_move(toCoord, fromCoord, fromPiece)
                    elif (toCoord[0] == fromCoord[0]+2 or toCoord[0] == fromCoord[0] - 2) and toCoord[1] == fromCoord[1]-2:
                        if toCoord[0] == fromCoord[0]+2:
                            jumpedPiece = self.locations[fromCoord[0]+1, fromCoord[1]-1]#white forward right
                            if jumpedPiece.is_white:
                                raise Exception("Sorry, that is not a valid move")
                        else:
                            jumpedPiece = self.locations[fromCoord[0]-1, fromCoord[1]-1]#white forward left
                            if jumpedPiece.is_white:
                                raise Exception("Sorry, that is not a valid move")
                        self.jump_move(toCoord, fromCoord, fromPiece)
                    elif fromPiece.is_king:
                        if (toCoord[0] == fromCoord[0]+1 or toCoord[0] == fromCoord[0] -1) and toCoord[1] == fromCoord[1]+1:
                            self.single_move(toCoord, fromCoord, fromPiece)
                        elif(toCoord[0] == fromCoord[0]+2 or toCoord[0] == fromCoord[0] -2) and toCoord[1] == fromCoord[1]+2:
                            if toCoord[0]== fromCoord[0]+2:
                                jumpedPiece = self.locations[fromCoord[0]+1, fromCoord[1]+1]#white backward right
                                if jumpedPiece.is_white:
                                    raise Exception("Sorry, that is not a valid move")
                            else:
                                jumpedPiece = self.locations[fromCoord[0]-1, fromCoord[1]+1]#white backward left
                                if jumpedPiece.is_white:
                                    raise Exception("Sorry, that is not a valid move")
                            self.jump_move(toCoord, fromCoord, fromPiece)
                        else:
                            raise Exception("Invalid human move (test)")
                    else:
                        raise Exception("Invalid human move")
                if not fromPiece.is_white:
                    if (toCoord[0] == fromCoord[0] + 1 or toCoord[0] == fromCoord[0] - 1) and toCoord[1] == fromCoord[1]+1:
                        self.single_move(toCoord, fromCoord, fromPiece)
                    elif (toCoord[0] == fromCoord[0] + 2 or toCoord[0] == fromCoord[0] - 2) and toCoord[1] == fromCoord[1]+2:
                        if toCoord[0] == fromCoord[0]+2:
                            jumpedPiece = self.locations[fromCoord[0]+1, fromCoord[1]+1]#black forward right
                            if not jumpedPiece.is_white:
                                raise Exception("Sorry, that is not a valid move")
                        else:
                            jumpedPiece = self.locations[fromCoord[0]-1, fromCoord[1]+1]#black backward left
                            if not jumpedPiece.is_white:
                                raise Exception("Sorry, that is not a valid move")
                        self.jump_move(toCoord, fromCoord, fromPiece)
                    elif(fromPiece.is_king):
                        if(toCoord[0] == fromCoord[0]+1 or toCoord[0] == fromCoord[0] - 1) and toCoord[1] == fromCoord[1]-1:
                            self.single_move(toCoord, fromCoord, fromPiece)
                        elif (toCoord[0] == fromCoord[0]+2 or toCoord[0] == fromCoord[0] - 2) and toCoord[1] == fromCoord[1]-2:
                            if toCoord[0] == fromCoord[0]+2:
                                jumpedPiece = self.locations[fromCoord[0]+1, fromCoord[1]-1]#black backward right
                                if not jumpedPiece.is_white:
                                    raise Exception("Sorry, that is not a valid move")
                            else:
                                jumpedPiece = self.locations[fromCoord[0]-1, fromCoord[1]-1]#white backward left
                                if not jumpedPiece.is_white:
                                    raise Exception("Sorry, that is not a valid move")
                            self.jump_move(toCoord, fromCoord, fromPiece)
                        else:
                            raise Exception("Invalid human move (test)")
                    else:
                        raise Exception("Invalid human move")
            else:
                raise Exception("Invalid human move!")


    def validate_input(self, fromPiece, player_is_white):

        if player_is_white and (not fromPiece.is_white):
            return False
        elif (not player_is_white) and fromPiece.is_white:
            return False
        else:
            return True

    def single_move(self, toCoord, fromCoord, fromPiece):


        self.locations[(toCoord[0], toCoord[1])] = fromPiece
        del self.locations[(fromCoord[0], fromCoord[1])]

        fromPiece._set_pos((toCoord[0], toCoord[1]))
        self.check_king(fromPiece, toCoord[1])


    def jump_move(self, toCoord, fromCoord, fromPiece):
        self.locations[(toCoord[0], toCoord[1])] = fromPiece
        del self.locations[(fromCoord[0], fromCoord[1])]
        fromPiece._set_pos((toCoord[0], toCoord[1]))

        if fromPiece.is_white:
            if(toCoord[0] > fromCoord[0]) and toCoord[1]<fromCoord[1]:#forward, right
                jumpedPiece = self.locations[(fromCoord[0]+1, fromCoord[1]-1)]
                del self.locations[fromCoord[0]+1, fromCoord[1]-1]
                self.black_pieces.remove(jumpedPiece)
                self.check_king(fromPiece, toCoord[1])
            elif(toCoord[0] < fromCoord[0]) and toCoord[1]<fromCoord[1]: #forward left
                jumpedPiece = self.locations[fromCoord[0]-1, fromCoord[1]-1]
                del self.locations[fromCoord[0]-1, fromCoord[1]-1]
                self.black_pieces.remove(jumpedPiece)
                self.check_king(fromPiece, toCoord[1])
            elif fromPiece.is_king and ((toCoord[0] > fromCoord[0]) and toCoord[1]>fromCoord[1]):#backward right for kings
                jumpedPiece = self.locations[fromCoord[0]+1, fromCoord[1]+1]
                del self.locations[fromCoord[0]+1, fromCoord[1]+1]
                self.black_pieces.remove(jumpedPiece)
            elif fromPiece.is_king and ((toCoord[0] < fromCoord[0]) and toCoord[1]>fromCoord[1]):#backward left for kings
                jumpedPiece = self.locations[fromCoord[0]-1, fromCoord[1]+1]
                del self.locations[fromCoord[0]-1, fromCoord[1]+1]
                self.black_pieces.remove(jumpedPiece)
        elif not fromPiece.is_white:
            if(toCoord[0]>fromCoord[0]) and toCoord[1]>fromCoord[1]:#forward right
                jumpedPiece = self.locations[fromCoord[0]+1, fromCoord[1]+1]
                del self.locations[fromCoord[0]+1, fromCoord[1]+1]
                self.white_pieces.remove(jumpedPiece)
                self.check_king(fromPiece, toCoord[1])
            elif(toCoord[0]<fromCoord[0]) and toCoord[1]>fromCoord[1]:#forward left
                jumpedPiece = self.locations[fromCoord[0]-1, fromCoord[1]+1]
                del self.locations[fromCoord[0]-1, fromCoord[1]+1]
                self.white_pieces.remove(jumpedPiece)
                self.check_king(fromPiece, toCoord[1])
            elif(toCoord[0]>fromCoord[0]) and toCoord[1]<fromCoord[1]:#backwards right
                jumpedPiece = self.locations[fromCoord[0]+1, fromCoord[1]-1]
                del self.locations[fromCoord[0]+1, fromCoord[1]-1]
                self.white_pieces.remove(jumpedPiece)
            elif(toCoord[0]<fromCoord[0]) and toCoord[1]<fromCoord[1]:#backwards left
                jumpedPiece = self.locations[fromCoord[0]-1, fromCoord[1]-1]
                del self.locations[fromCoord[0]-1, fromCoord[1]-1]
                self.white_pieces.remove(jumpedPiece)
        else:
            print("not a valid jump")
    def check_for_human_moves(self, player_is_white):
        if player_is_white:
            color = "white"
        else:
            color = "black"
        valid_moves = self.find_human_next_states(color)
        self.jumpFlag = 0
        return valid_moves

    def find_human_next_states(self, color):
        next_states = []
        if color == "black":
            for piece in self.black_pieces:
                valid_moves = self.find_valid_moves(piece, color)
                if valid_moves:
                    return True
        else:
            for piece in self.white_pieces:
                valid_moves = self.find_valid_moves(piece, color)
                if valid_moves:
                    return True

        return False


    def check_for_human_jumps(self, coord2):
        fromCoord = self.numberToCoordinates[coord2]
        fromPiece = self.locations.get(fromCoord, None)
        print("Coordinate 2 is ")
        print(coord2)
        if fromPiece.is_white:
            color = "white"
        else:
            color = "black"
        valid_moves = self.find_valid_moves(fromPiece, color)
        (move, jump) = valid_moves
        print("jump is ")
        print(jump)

        if jump:
            [((fromCoordX, fromCoordY), (toCoordX, toCoordY))] = jump
            if toCoordX < 0 or toCoordX > 7 or toCoordY < 0 or toCoordY > 7:
                self.jumpFlag = 0
                return False
            elif jump:
                '''if fromPiece.is_white and toCoordY ==0:#if it is made a king, stop jumping.
                    self.jumpFlag = 0
                    return False
                elif not fromPiece.is_white and toCoordY == 7:
                    self.jumpFlag = 0
                    return False'''
                self.jumpFlag = 0
                return True
        self.jumpFlag = 0
        return False

    def find_human_jumps(self, player_is_white):
        if player_is_white:
            color = "white"
        else:
            color = "black"

        next_states = []
        if color == "black":
            for piece in self.black_pieces:
                valid_moves = self.find_valid_moves(piece, color)
                (move, jump) = valid_moves
                if jump:

                    self.jumpFlag = 0
                    return True
        else:
            for piece in self.white_pieces:
                valid_moves = self.find_valid_moves(piece, color)
                (move, jump) = valid_moves
                if jump:
                    self.jumpFlag = 0
                    return True
        self.jumpFlag = 0
        return False

    def is_jump(self, coord_a, coord_b, player_is_white):
        fromCoord = self.numberToCoordinates[coord_a]
        fromPiece = self.locations.get(fromCoord, None)
        fromCoord = self.numberToCoordinates[coord_a]
        toCoord = self.numberToCoordinates[coord_b]

        if player_is_white:
            if(toCoord[0] == fromCoord[0] + 2 or toCoord[0] == fromCoord[0] - 2) and toCoord[1] == fromCoord[1]-2:#forward, right or forward left
                return True
            elif fromPiece.is_king and ((toCoord[0] == fromCoord[0] + 2 or toCoord[0] == fromCoord[0] - 2) and toCoord[1] == fromCoord[1]+2):#backward right, left for kings
                return True

            else:
                return False
        elif not player_is_white:
            if(toCoord[0] == fromCoord[0] + 2 or toCoord[0] == fromCoord[0] - 2) and toCoord[1] == fromCoord[1]+2:#forward right or left
                return True
            elif fromPiece.is_king and ((toCoord[0] == fromCoord[0] + 2 or toCoord[0] ==fromCoord[0] - 2) and toCoord[1] == fromCoord[1]-2):#backwards right, left
                return True

            else:
                return False
        else:
            return False

#####################################################################################################################

    def computerMove(self, color):
        possible_moves = self.find_next_states(color)
    # Choose a move somehow... for now you can probably do:
        if possible_moves:
            next_move = possible_moves[0]
            self.make_move_computer(next_move)
            return True
        else:
            #raise Exception ("No valid moves exist for computer. Other Player wins")
            print("No valid moves exist for computer. Other Player wins")
            return False

    def find_next_states(self, color):
        next_states = []
        if color == "black":
            for piece in self.black_pieces:
                valid_moves = self.find_valid_moves(piece, color)
                (move, jump) = valid_moves
                next_states = jump + next_states + move
        else:
            for piece in self.white_pieces:
                valid_moves = self.find_valid_moves(piece, color)
                (move, jump) = valid_moves
            #add next states to list instead of making a list of lists with append
                next_states = jump + next_states + move

#        for valid_move in valid_moves:
#            current_state = copied_board(self.locations, self.black_pieces, self.white_pieces)
#            next_states.append( self.update_board(current_state, valid_move))

        return next_states

    def find_valid_moves(self, piece, color):
        valid_moves = []
        valid_jump_moves = []
        (coordX, coordY) = piece._get_pos()
        fromSquare = (coordX, coordY)

        if not piece.is_white:
            moveToLeft = (coordX - 1, coordY + 1)
            moveToRight = (coordX + 1, coordY + 1)
            if piece.is_king:
               moveBackLeft = (coordX-1, coordY-1)
               moveBackRight = (coordX+1, coordY-1)
        else:
            moveToLeft = (coordX - 1, coordY - 1)
            moveToRight = (coordX + 1, coordY - 1)
            if piece.is_king:
               moveBackLeft = (coordX-1, coordY+1)
               moveBackRight = (coordX+1, coordY+1)
    #   jump move
        if piece.is_king and not self.is_valid_move(fromSquare, moveBackLeft, color):
            direction = "backwardLeft"
            if self.computer_jump(fromSquare, moveBackLeft, direction, color):
                if color == "black":
                    newMoveLeft = (coordX - 2, coordY - 2)
                    valid_jump_moves.append((fromSquare, newMoveLeft))
                else:
                    newMoveLeft = (coordX - 2, coordY + 2)
                    valid_jump_moves.append((fromSquare, newMoveLeft))
        elif piece.is_king and self.is_valid_move(fromSquare, moveBackLeft, color):
            valid_moves.append((fromSquare, moveBackLeft))

        if piece.is_king and not self.is_valid_move(fromSquare, moveBackRight, color):
            direction = "backwardRight"
            if self.computer_jump(fromSquare, moveBackRight, direction, color):
                if color == "black":
                    newMoveRight = (coordX + 2, coordY - 2)
                    valid_jump_moves.append((fromSquare, newMoveRight))
                else:
                    newMoveRight = (coordX + 2, coordY + 2)
                    valid_jump_moves.append((fromSquare, newMoveRight))
        elif piece.is_king and self.is_valid_move(fromSquare, moveBackRight, color):
            valid_moves.append((fromSquare, moveBackRight))

        if not self.is_valid_move(fromSquare, moveToLeft, color):
            direction = "forwardLeft"
            if self.computer_jump(fromSquare, moveToLeft, direction, color):
                if color == "black":
                    newMoveLeft = (coordX - 2, coordY + 2)
                    valid_jump_moves.append((fromSquare, newMoveLeft))
                else:
                    newMoveLeft = (coordX - 2, coordY - 2)
                    valid_jump_moves.append((fromSquare, newMoveLeft))

        #single move
        else:
             valid_moves.append((fromSquare, moveToLeft))

        if not self.is_valid_move(fromSquare, moveToRight, color):
            direction = "forwardRight"
            if self.computer_jump(fromSquare, moveToRight, direction, color):
                if color == "black":
                    newMoveRight = (coordX + 2, coordY + 2)
                    valid_jump_moves.append((fromSquare, newMoveRight))
                else:
                    newMoveRight = (coordX + 2, coordY - 2)
                    valid_jump_moves.append((fromSquare, newMoveRight))

        #single move
        else:
             valid_moves.append((fromSquare, moveToRight))

        return (valid_moves, valid_jump_moves)

    def is_valid_move(self, fromCoord, toCoord, color):
        fromPiece = self.locations.get(fromCoord, None)
        toPiece = self.locations.get(toCoord, None)
        (toCoordX, toCoordY) = toCoord

        return not toPiece and 0 <= toCoordX <= 7 and 0 <= toCoordY <= 7

    def make_move_computer(self, next_move):
        (fromCoord, toCoord) = next_move
        (fromCoordX, fromCoordY) = fromCoord
        fromPiece = self.locations[fromCoord]
        self.locations[toCoord] = fromPiece
        (fromCoordX, fromCoordY) = fromCoord
        (toCoordX, toCoordY) = toCoord
        # -- Display computer move ---
        fromSq = fromCoordY * 4 + fromCoordX//2 + 1
        toSq = toCoordY * 4 + toCoordX//2 + 1
        print("Computer move: {} - {}".format(fromSq, toSq))


        #check to see what color is being played and what needs to be removed
        if fromPiece.is_white:
            if fromPiece.is_king and self.jumpFlag == 1 and (fromCoordX > toCoordX) and (fromCoordY < toCoordY):
                jumpedPiece = self.locations[(fromCoordX-1, fromCoordY+1)]
                self.black_pieces.remove(jumpedPiece)
                del self.locations[fromCoordX-1, fromCoordY+1]
            elif fromPiece.is_king and self.jumpFlag == 1 and (fromCoordX < toCoordX) and (fromCoordY < toCoordY):
                jumpedPiece = self.locations[(fromCoordX+1, fromCoordY+1)]
                self.black_pieces.remove(jumpedPiece)
                del self.locations[fromCoordX+1, fromCoordY+1]
            #jump right forward and update board
            elif self.jumpFlag == 1 and (fromCoordX < toCoordX) and (fromCoordY > toCoordY):
                jumpedPiece = self.locations[(fromCoordX+1, fromCoordY-1)]
                self.black_pieces.remove(jumpedPiece)
                del self.locations[fromCoordX+1, fromCoordY-1]
            #jump left forward and update board
            elif self.jumpFlag == 1 and (fromCoordX > toCoordX) and (fromCoordY > toCoordY):
                jumpedPiece = self.locations[(fromCoordX-1, fromCoordY-1)]
                self.black_pieces.remove(jumpedPiece)
                del self.locations[fromCoordX-1, fromCoordY-1]
        else:
            if fromPiece.is_king and self.jumpFlag == 1 and (fromCoordX > toCoordX) and (fromCoordY > toCoordY):
                jumpedPiece = self.locations[(fromCoordX-1, fromCoordY-1)]
                self.white_pieces.remove(jumpedPiece)
                del self.locations[fromCoordX-1, fromCoordY-1]
            elif fromPiece.is_king and self.jumpFlag == 1 and (fromCoordX < toCoordX) and (fromCoordY > toCoordY):
                jumpedPiece = self.locations[(fromCoordX+1, fromCoordY-1)]
                self.white_pieces.remove(jumpedPiece)
                del self.locations[fromCoordX+1, fromCoordY-1]
            #jump left forward and update board
            if self.jumpFlag == 1 and ((fromCoordX > toCoordX) and (fromCoordY < toCoordY)):
                #if not self.right:
                jumpedPiece = self.locations[(fromCoordX-1, fromCoordY+1)]
                self.white_pieces.remove(jumpedPiece)
                del self.locations[fromCoordX-1, fromCoordY+1]
            #jump right forward and update board (forward to black side)
            elif self.jumpFlag == 1 and (fromCoordX < toCoordX) and (fromCoordY < toCoordY):
                #if self.right:
                jumpedPiece = self.locations[(fromCoordX+1, fromCoordY+1)]
                self.white_pieces.remove(jumpedPiece)
                del self.locations[fromCoordX+1, fromCoordY+1]
        #will allow to update for single moves
        if self.jumpFlag == 1:
            self.jumpFlag = 0
            del self.locations[fromCoord]
            fromPiece._set_pos(toCoord)

            if not fromPiece.is_king:
                self.check_king(fromPiece, toCoordY)
                if fromPiece.is_king:
                    return

            next_moves = self.multiple_jump(toCoord, fromPiece)
            if next_moves:
            #is not None:
                self.make_move_computer(next_moves)
        else:
            del self.locations[fromCoord]
            fromPiece._set_pos(toCoord)
            self.check_king(fromPiece, toCoordY)

    def multiple_jump(self, fromCoord, fromPiece):
        (fromCoordX, fromCoordY) = fromCoord
        new_moves = []


        if fromPiece.is_white:
            color = "white"
            if fromPiece.is_king:
                forwardLeft = (fromCoordX - 1, fromCoordY - 1)
                forwardRight = (fromCoordX + 1, fromCoordY - 1)
                backwardLeft = (fromCoordX - 1, fromCoordY + 1)
                backwardRight = (fromCoordX + 1, fromCoordY + 1)
            else:
                forwardLeft = (fromCoordX -1, fromCoordY -1)
                forwardRight = (fromCoordX +1, fromCoordY -1)
        else:
            color = "black"
            if fromPiece.is_king:
                forwardLeft = (fromCoordX - 1, fromCoordY + 1)
                forwardRight = (fromCoordX + 1, fromCoordY + 1)
                backwardLeft = (fromCoordX - 1, fromCoordY - 1)
                backwardRight = (fromCoordX + 1, fromCoordY - 1)
            else:
                forwardLeft = (fromCoordX - 1, fromCoordY + 1)
                forwardRight = (fromCoordX + 1, fromCoordY + 1)

        if fromPiece.is_king:
            if color == "black":
                if not self.is_valid_move(fromCoord, backwardLeft, color):
                    direction = "backwardLeft"
                    if self.computer_jump(fromCoord, backwardLeft, direction, color):
                        newMoveLeft = (fromCoordX - 2, fromCoordY - 2)
                        new_moves = (fromCoord, newMoveLeft)
                        return new_moves
                if not self.is_valid_move(fromCoord, forwardLeft, color):
                    direction = "forwardLeft"
                    if self.computer_jump(fromCoord, forwardLeft, direction, color):
                        newMoveLeft = (fromCoordX - 2, fromCoordY + 2)
                        new_moves = (fromCoord, newMoveLeft)
                        return new_moves
            else:
                if not self.is_valid_move(fromCoord, backwardLeft, color):
                    direction = "backwardLeft"
                    if self.computer_jump(fromCoord, backwardLeft, direction, color):
                        newMoveLeft = (fromCoordX - 2, fromCoordY + 2)
                        new_moves = (fromCoord, newMoveLeft)
                        return new_moves
                if not self.is_valid_move(fromCoord, forwardLeft, color):
                    direction = "forwardLeft"
                    if self.computer_jump(fromCoord, forwardLeft, direction, color):
                        newMoveLeft = (fromCoordX - 2, fromCoordY - 2)
                        new_moves = (fromCoord, newMoveLeft)
                        return new_moves

        if fromPiece.is_king:
            if color == "black":
                if not self.is_valid_move(fromCoord, backwardRight, color):
                    direction = "backwardRight"
                    if self.computer_jump(fromCoord, backwardRight, direction, color):
                        newMoveRight = (fromCoordX + 2, fromCoordY - 2)
                        new_moves = (fromCoord, newMoveRight)
                        return new_moves
                if not self.is_valid_move(fromCoord, forwardRight, color):
                    direction = "forwardRight"
                    if self.computer_jump(fromCoord, forwardRight, direction, color):
                        newMoveRight = (fromCoordX + 2, fromCoordY + 2)
                        new_moves = (fromCoord, newMoveRight)
                        return new_moves
            else:
                if not self.is_valid_move(fromCoord, backwardRight, color):
                    direction = "backwardRight"
                    if self.computer_jump(fromCoord, backwardRight, direction, color):
                        newMoveRight = (fromCoordX + 2, fromCoordY +2)
                        new_moves = (fromCoord, newMoveRight)
                        return new_moves
                if not self.is_valid_move(fromCoord, forwardRight, color):
                    direction = "forwardRight"
                    if self.computer_jump(fromCoord, forwardRight, direction, color):
                        newMoveRight = (fromCoordX + 2, fromCoordY - 2)
                        new_moves = (fromCoord, newMoveRight)
                        return new_moves

        if not self.is_valid_move(fromCoord, forwardLeft, color):
            direction = "forwardLeft"
            if self.computer_jump(fromCoord, forwardLeft, direction, color):
                if color == "black":
                    newMoveLeft = (fromCoordX - 2, fromCoordY + 2)
                    new_moves = (fromCoord, newMoveLeft)
                    return new_moves
                else:
                    newMoveLeft = (fromCoordX - 2, fromCoordY - 2)
                    new_moves = (fromCoord, newMoveLeft)
                    return new_moves

        if not self.is_valid_move(fromCoord, forwardRight, color):
            direction = "forwardRight"
            if self.computer_jump(fromCoord, forwardRight, direction, color):
                if color == "black":
                    newMoveRight = (fromCoordX + 2, fromCoordY + 2)
                    new_moves = (fromCoord, newMoveRight)
                    return new_moves
                else:
                    newMoveLeft = (fromCoordX + 2, fromCoordY - 2)
                    new_moves = (fromCoord, newMoveLeft)
                    return new_moves
        else:

            return new_moves

    def computer_jump(self, fromSquare, toSquare, direction, color):
        #toPiece and fromPiece are piece objects
        fromPiece = self.locations.get(fromSquare, None)
        toPiece = self.locations.get(toSquare, None)
        (toCoordX, toCoordY) = toSquare
        (fromCoordX, fromCoordY) = fromSquare
        toCoord = (toCoordX, toCoordY)
        newToKingPiece = False
        newToPiece = False

        #had to change from toCoordX, Y +/- 1 to fromCoordX, Y +/- 2. Otherwise the computer
        #thought it was possible to take a jump when it wasnt and forces a move that can't be taken
        if color == "white":
            if fromPiece.is_king:
                (backwardJumpLeftX, backwardJumpLeftY) = backwardJumpLeft = (fromCoordX - 2, fromCoordY+ 2)
                (backwardJumpRightX, backwardJumpRightY) = backwardJumpRight = (fromCoordX + 2, fromCoordY + 2)
                (forwardJumpLeftX, forwardJumpLeftY)= forwardJumpLeft = (fromCoordX - 2, fromCoordY - 2)
                (forwardJumpRightX, forwardJumpRightY)= forwardJumpRight = (fromCoordX + 2, fromCoordY - 2)
            else:
                forwardJumpLeft = (fromCoordX - 2, fromCoordY - 2)
                forwardJumpRight = (fromCoordX + 2, fromCoordY - 2)
        else:
            if fromPiece.is_king:
                (backwardJumpLeftX, backwardJumpLeftY) = backwardJumpLeft = (fromCoordX - 2, fromCoordY - 2)
                (backwardJumpRightX, backwardJumpRightY) = backwardJumpRight = (fromCoordX + 2, fromCoordY - 2)
                (forwardJumpLeftX, forwardJumpLeftY) = forwardJumpLeft = (fromCoordX - 2, fromCoordY + 2)
                (forwardJumpRightX, forwardJumpRightY) = forwardJumpRight = (fromCoordX + 2, fromCoordY + 2)
            else:
                forwardJumpLeft = (fromCoordX - 2, fromCoordY + 2)
                forwardJumpRight = (fromCoordX + 2, fromCoordY + 2)

        if fromPiece.is_king:
            if direction == "backwardRight":
                if not 0 <= backwardJumpRightX <= 7 and not 0 <= backwardJumpRightY <= 7:
                    return False
            elif direction == "backwardLeft":
                if not 0 <= backwardJumpLeftX <= 7 and not 0 <= backwardJumpLeftY <= 7:
                    return False
            if direction == "forwardRight":
                if not 0<= forwardJumpRightX <= 7 and not 0 <= forwardJumpRightY <=7:
                    return False
            elif direction == "forwardLeft":
                if not 0<= forwardJumpLeftX <= 7 and not 0 <= forwardJumpLeftY <=7:
                    return False

        if fromPiece and not toPiece:
            return False
        if not 0 <= toCoordX <= 7 and not 0 <= toCoordY <= 7:
            return False
        elif fromPiece and toPiece:
            if fromPiece.get_color() is not toPiece.get_color():
                if direction == "backwardLeft":
                    if fromPiece.is_king and self.is_valid_move(fromPiece, backwardJumpLeft, color):
                        newToKingPiece = True
                elif direction == "backwardRight":
                    if fromPiece.is_king and self.is_valid_move(fromPiece, backwardJumpRight, color):
                        newToKingPiece = True
                elif direction == "forwardLeft":
                    if fromPiece.is_king and self.is_valid_move(fromPiece, forwardJumpLeft, color):
                        newToPiece = True
                    elif self.is_valid_move(fromPiece, forwardJumpLeft, color):
                        newToPiece = True
                elif direction == "forwardRight":
                    if fromPiece.is_king and self.is_valid_move(fromPiece, forwardJumpRight, color):
                        newToPiece = True
                    elif self.is_valid_move(fromPiece, forwardJumpRight, color):
                        newToPiece = True

                if newToPiece and newToKingPiece:
                    self.jumpFlag = 1
                    return True
                elif newToKingPiece:
                    self.jumpFlag = 1
                    return True
                elif newToPiece:
                    self.jumpFlag = 1
                    return True
        return False


    def check_king(self, fromPiece, CoordY):

        if fromPiece.is_white:
            if CoordY == 0:
                fromPiece.make_king()
            else:
                return
            print(fromPiece.is_king)
        else:
            if CoordY == 7:
                fromPiece.make_king()
            else:
                return


    def collidepoint(self, pos):
        return self.boardrect.collidepoint(pos)