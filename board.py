'''
Board.py - this file creates a representation of a game board and embodies all the game logic including
human and computer moving, jump pieces, kinging piece, and win conditions.
'''

from piece import Piece
import pygame
from collections import namedtuple

class Board:
    jumpFlag = 0 #to determine if the computer has made a jump
    locations = dict()
    black_pieces = list()
    white_pieces = list()
    img_folder = "img/"

    #setting data structures for internal
    Coordinate = namedtuple('Coordinate', 'x, y')
    coordinate1 = Coordinate(1, 0)
    coordinate2 = Coordinate(3, 0)
    coordinate3 = Coordinate(5, 0)
    coordinate4 = Coordinate(7, 0)
    coordinate5 = Coordinate(0, 1)
    coordinate6 = Coordinate(2, 1)
    coordinate7 = Coordinate(4, 1)
    coordinate8 = Coordinate(6, 1)
    coordinate9 = Coordinate(1, 2)
    coordinate10 = Coordinate(3, 2)
    coordinate11 = Coordinate(5, 2)
    coordinate12 = Coordinate(7, 2)
    coordinate13 = Coordinate(0, 3)
    coordinate14 = Coordinate(2, 3)
    coordinate15 = Coordinate(4, 3)
    coordinate16 = Coordinate(6, 3)
    coordinate17 = Coordinate(1, 4)
    coordinate18 = Coordinate(3, 4)
    coordinate19 = Coordinate(5, 4)
    coordinate20 = Coordinate(7, 4)
    coordinate21 = Coordinate(0, 5)
    coordinate22 = Coordinate(2, 5)
    coordinate23 = Coordinate(4, 5)
    coordinate24 = Coordinate(6, 5)
    coordinate25 = Coordinate(1, 6)
    coordinate26 = Coordinate(3, 6)
    coordinate27 = Coordinate(5, 6)
    coordinate28 = Coordinate(7, 6)
    coordinate29 = Coordinate(0, 7)
    coordinate30 = Coordinate(2, 7)
    coordinate31 = Coordinate(4, 7)
    coordinate32 = Coordinate(6, 7)

    numberToTupleKey= {1: coordinate1, 2: coordinate2, 3: coordinate3, 4: coordinate4,
                       5: coordinate5, 6: coordinate6,   7: coordinate7, 8: coordinate8,
                       9: coordinate9,  10: coordinate10, 11: coordinate11, 12: coordinate12,
                       13: coordinate13,  14: coordinate14, 15: coordinate15, 16: coordinate16,
                       17: coordinate17,  18: coordinate18, 19: coordinate19, 20: coordinate20,
                       21: coordinate21,  22: coordinate22, 23: coordinate23, 24: coordinate24,
                       25: coordinate25,  26: coordinate26, 27: coordinate27, 28: coordinate28,
                       29: coordinate29, 30: coordinate30, 31: coordinate31, 32: coordinate32,}




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



    def single_move(self, toCoord, fromCoord, fromPiece):
        self.locations[(toCoord.x, toCoord.y)] = fromPiece
        del self.locations[(fromCoord.x, fromCoord.y)]

        fromPiece._set_pos((toCoord.x, toCoord.y))
        self.check_king(fromPiece, toCoord.y)


    def jump_move(self, toCoord, fromCoord, fromPiece):
        self.locations[(toCoord.x, toCoord.y)] = fromPiece
        del self.locations[(fromCoord.x, fromCoord.y)]
        fromPiece._set_pos((toCoord.x, toCoord.y))

        if fromPiece.is_white:
            if(toCoord.x > fromCoord.x) and toCoord.y<fromCoord.y:#forward, right
                jumpedPiece = self.locations[(fromCoord.x+1, fromCoord.y-1)]
                del self.locations[fromCoord.x+1, fromCoord.y-1]
                self.black_pieces.remove(jumpedPiece)
                self.check_king(fromPiece, toCoord.y)
            elif(toCoord.x < fromCoord.x) and toCoord.y<fromCoord.y: #forward left
                jumpedPiece = self.locations[fromCoord.x-1, fromCoord.y-1]
                del self.locations[fromCoord.x-1, fromCoord.y-1]
                self.black_pieces.remove(jumpedPiece)
                self.check_king(fromPiece, toCoord.y)
            elif fromPiece.is_king and ((toCoord.x > fromCoord.x) and toCoord.y>fromCoord.y):#backward right for kings
                jumpedPiece = self.locations[fromCoord.x+1, fromCoord.y+1]
                del self.locations[fromCoord.x+1, fromCoord.y+1]
                self.black_pieces.remove(jumpedPiece)
            elif fromPiece.is_king and ((toCoord.x < fromCoord.x) and toCoord.y>fromCoord.y):#backward left for kings
                jumpedPiece = self.locations[fromCoord.x-1, fromCoord.y+1]
                del self.locations[fromCoord.x-1, fromCoord.y+1]
                self.black_pieces.remove(jumpedPiece)
        elif not fromPiece.is_white:
            if(toCoord.x>fromCoord.x) and toCoord.y>fromCoord.y:#forward right
                jumpedPiece = self.locations[fromCoord.x+1, fromCoord.y+1]
                del self.locations[fromCoord.x+1, fromCoord.y+1]
                self.white_pieces.remove(jumpedPiece)
                self.check_king(fromPiece, toCoord.y)
            elif(toCoord.x<fromCoord.x) and toCoord.y>fromCoord.y:#forward left
                jumpedPiece = self.locations[fromCoord.x-1, fromCoord.y+1]
                del self.locations[fromCoord.x-1, fromCoord.y+1]
                self.white_pieces.remove(jumpedPiece)
                self.check_king(fromPiece, toCoord.y)
            elif(toCoord.x>fromCoord.x) and toCoord.y<fromCoord.y:#backwards right
                jumpedPiece = self.locations[fromCoord.x+1, fromCoord.y-1]
                del self.locations[fromCoord.x+1, fromCoord.y-1]
                self.white_pieces.remove(jumpedPiece)
            elif(toCoord.x<fromCoord.x) and toCoord.y<fromCoord.y:#backwards left
                jumpedPiece = self.locations[fromCoord.x-1, fromCoord.y-1]
                del self.locations[fromCoord.x-1, fromCoord.y-1]
                self.white_pieces.remove(jumpedPiece)
        else:
            print("not a valid jump")

    def validate_input(self, fromPiece, player_is_white):

        if player_is_white and (not fromPiece.is_white):
            return False
        elif (not player_is_white) and fromPiece.is_white:
            return False
        else:
            return True


    def move_human(self, fromSquare, toSquare, player_is_white):
        fromCoord = self.numberToTupleKey[fromSquare]
        toCoord = self.numberToTupleKey[toSquare]
        fromPiece = self.locations.get(fromCoord, None)
        toPiece = self.locations.get(toCoord, None)

        if not self.validate_input(fromPiece, player_is_white):
           raise Exception ("Sorry, that is not a valid move")
        else:
            if fromPiece and not toPiece:
                if fromPiece.is_white:
                    if (toCoord.x == fromCoord.x+1 or toCoord.x == fromCoord.x - 1) and toCoord.y == fromCoord.y-1:
                         self.single_move(toCoord, fromCoord, fromPiece)
                    elif (toCoord.x == fromCoord.x+2 or toCoord.x == fromCoord.x - 2) and toCoord.y == fromCoord.y-2:
                        if toCoord.x == fromCoord.x+2:
                            jumpedPiece = self.locations[fromCoord.x+1, fromCoord.y-1]#white forward right
                            if jumpedPiece.is_white:
                                raise Exception("Sorry, that is not a valid move")
                        else:
                            jumpedPiece = self.locations[fromCoord.x-1, fromCoord.y-1]#white forward left
                            if jumpedPiece.is_white:
                                raise Exception("Sorry, that is not a valid move")
                        self.jump_move(toCoord, fromCoord, fromPiece)
                    elif fromPiece.is_king:
                        if (toCoord.x == fromCoord.x+1 or toCoord.x == fromCoord.x -1) and toCoord.y == fromCoord.y+1:
                            self.single_move(toCoord, fromCoord, fromPiece)
                        elif(toCoord.x == fromCoord.x+2 or toCoord.x == fromCoord.x -2) and toCoord.y == fromCoord.y+2:
                            if toCoord.x == fromCoord.x+2:
                                jumpedPiece = self.locations[fromCoord.x+1, fromCoord.y+1]#white backward right
                                if jumpedPiece.is_white:
                                    raise Exception("Sorry, that is not a valid move")
                            else:
                                jumpedPiece = self.locations[fromCoord.x-1, fromCoord.y+1]#white backward left
                                if jumpedPiece.is_white:
                                    raise Exception("Sorry, that is not a valid move")
                            self.jump_move(toCoord, fromCoord, fromPiece)
                        else:
                            raise Exception("Invalid human move (test)")
                    else:
                        raise Exception("Invalid human move")
                if not fromPiece.is_white:
                    if (toCoord.x == fromCoord.x + 1 or toCoord.x == fromCoord.x - 1) and toCoord.y == fromCoord.y+1:
                        self.single_move(toCoord, fromCoord, fromPiece)
                    elif (toCoord.x == fromCoord.x + 2 or toCoord.x == fromCoord.x - 2) and toCoord.y == fromCoord.y+2:
                        if toCoord.x == fromCoord.x+2:
                            jumpedPiece = self.locations[fromCoord.x+1, fromCoord.y+1]#black forward right
                            if not jumpedPiece.is_white:
                                raise Exception("Sorry, that is not a valid move")
                        else:
                            jumpedPiece = self.locations[fromCoord.x-1, fromCoord.y+1]#black backward left
                            if not jumpedPiece.is_white:
                                raise Exception("Sorry, that is not a valid move")
                        self.jump_move(toCoord, fromCoord, fromPiece)
                    elif(fromPiece.is_king):
                        if(toCoord.x == fromCoord.x+1 or toCoord.x == fromCoord.x - 1) and toCoord.y == fromCoord.y-1:
                            self.single_move(toCoord, fromCoord, fromPiece)
                        elif (toCoord.x == fromCoord.x+2 or toCoord.x == fromCoord.x - 2) and toCoord.y == fromCoord.y-2:
                            if toCoord.x == fromCoord.x+2:
                                jumpedPiece = self.locations[fromCoord.x+1, fromCoord.y-1]#black backward right
                                if not jumpedPiece.is_white:
                                    raise Exception("Sorry, that is not a valid move")
                            else:
                                jumpedPiece = self.locations[fromCoord.x-1, fromCoord.y-1]#white backward left
                                if not jumpedPiece.is_white:
                                    raise Exception("Sorry, that is not a valid move")
                            self.jump_move(toCoord, fromCoord, fromPiece)
                        else:
                            raise Exception("Invalid human move (test)")
                    else:
                        raise Exception("Invalid human move")
            else:
                raise Exception("Invalid human move!")
    def check_for_human_jumps(self, player_is_white):
        if player_is_white:
            color = "white"
        else:
            color = "black"
        jumps_exist = self.find_human_jumps(color)
        self.jumpFlag = 0
        return jumps_exist

    def find_human_jumps(self, color):
        next_states = []
        if color == "black":
            for piece in self.black_pieces:
                valid_moves = self.find_valid_moves(piece, color)
                (move, jump) = valid_moves
                if jump:
                    return True
        else:
            for piece in self.white_pieces:
                valid_moves = self.find_valid_moves(piece, color)
                (move, jump) = valid_moves
                if jump:
                    return True

        return False

    def is_jump_helper(self, coord_a, coord_b, player_is_white):
        fromCoord = self.numberToTupleKey[coord_a]
        fromPiece = self.locations.get(fromCoord, None)

        if self.is_jump(fromPiece, coord_a, coord_b, player_is_white):
            return True
        else:
            return False

    def is_jump(self, fromPiece, coord_a, coord_b, player_is_white):
        fromCoord = self.numberToTupleKey[coord_a]
        toCoord = self.numberToTupleKey[coord_b]

        #in the case that a piece becomes a king in the middle of a double jump, it check needs to know to consider the piece a king
        #this will not work if there is an error.  make a flag to see if it has been made a king. if so, then change it back before the error

        #if player_is_white and toCoord.y ==0:
        #    fromPiece.make_king()
        #elif not player_is_white and toCoord.y == 7:
        #    fromPiece.make_king()

        if player_is_white:
            if(toCoord.x == fromCoord.x + 2 or toCoord.x == fromCoord.x - 2) and toCoord.y == fromCoord.y-2:#forward, right or forward left
                return True
            elif fromPiece.is_king and ((toCoord.x == fromCoord.x + 2 or toCoord.x == fromCoord.x - 2) and toCoord.y == fromCoord.y+2):#backward right, left for kings
                return True
            elif (toCoord.x == fromCoord.x + 2 or toCoord.x == fromCoord.x -2) and toCoord.y == fromCoord.y-2 and toCoord.y == 0: #forward right or left and ends on king spot
                fromPiece.make_king()
                return True
            else:
                return False
        elif not player_is_white:
            if(toCoord.x == fromCoord.x + 2 or toCoord.x == fromCoord.x - 2) and toCoord.y == fromCoord.y+2:#forward right or left
                return True
            elif fromPiece.is_king and ((toCoord.x == fromCoord.x + 2 or toCoord.x ==fromCoord.x - 2) and toCoord.y == fromCoord.y-2):#backwards right, left
                return True
            elif (toCoord.x == fromCoord.x + 2 or toCoord.x == fromCoord.x -2) and toCoord.y == fromCoord.y+2 and toCoord.y == 0: #forward right or left and ends on king spot
                fromPiece.make_king()
                return True
            else:
                return False
        else:
            return False


    def human_double(self, coord1, coord2, coord3, player_is_white):

        fromCoord = self.numberToTupleKey[coord1]
        fromPiece = self.locations.get(fromCoord, None)
        (coordX, coordY) = fromCoord

        if self.is_jump(fromPiece, coord1, coord2, player_is_white) and self.is_jump(fromPiece, coord2, coord3, player_is_white):
                self.move_human(coord1,coord2, player_is_white)
                self.move_human(coord2, coord3, player_is_white)
        else:
            raise Exception ("Invalid double move")

    def collidepoint(self, pos):
        return self.boardrect.collidepoint(pos)

    def computerMove(self, color):
        possible_moves = self.find_next_states(color)
    # Choose a move somehow... for now you can probably do:
        if possible_moves:
            next_move = possible_moves[ 0 ]
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
#            next_states.append( self.copy_board(valid_move))

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
            direction = "left"
            if self.computer_jump(fromSquare, moveBackLeft, direction, color):
                if color == "black":
                    newMoveLeft = (coordX - 2, coordY - 2)
                    valid_jump_moves.append((fromSquare, newMoveLeft))
                else:
                    newMoveLeft = (coordX - 2, coordY + 2)
                    valid_jump_moves.append((fromSquare, newMoveLeft))
            else:
                print("i do nothing")
        elif piece.is_king and self.is_valid_move(fromSquare, moveBackLeft, color):
            valid_moves.append((fromSquare, moveBackLeft))

        if piece.is_king and not self.is_valid_move(fromSquare, moveBackRight, color):
            direction = "right"
            if self.computer_jump(fromSquare, moveBackRight, direction, color):
                if color == "black":
                    newMoveRight = (coordX + 2, coordY - 2)
                    valid_jump_moves.append((fromSquare, newMoveRight))
                else:
                    newMoveRight = (coordX + 2, coordY + 2)
                    valid_jump_moves.append((fromSquare, newMoveRight))
            else:
                print("i do nothing")
        elif piece.is_king and self.is_valid_move(fromSquare, moveBackRight, color):
            valid_moves.append((fromSquare, moveBackRight))

        if not self.is_valid_move(fromSquare, moveToLeft, color):
            direction = "left"
            if self.computer_jump(fromSquare, moveToLeft, direction, color):
                if color == "black":
                    newMoveLeft = (coordX - 2, coordY + 2)
                    valid_jump_moves.append((fromSquare, newMoveLeft))
                else:
                    newMoveLeft = (coordX - 2, coordY - 2)
                    valid_jump_moves.append((fromSquare, newMoveLeft))
            #else:
            #    print("i do nothing")
        #single move
        else:
             valid_moves.append((fromSquare, moveToLeft))

        if not self.is_valid_move(fromSquare, moveToRight, color):
            direction = "right"
            if self.computer_jump(fromSquare, moveToRight, direction, color):
                if color == "black":
                    newMoveRight = (coordX + 2, coordY + 2)
                    valid_jump_moves.append((fromSquare, newMoveRight))
                else:
                    newMoveRight = (coordX + 2, coordY - 2)
                    valid_jump_moves.append((fromSquare, newMoveRight))
            #else:
             #   print("i do nothing")
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
            self.check_king(fromPiece, toCoordY)
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
            moveLeft = (fromCoordX -1, fromCoordY -1)
            moveRight = (fromCoordX +1, fromCoordY -1)
            color = "white"
        else:
            moveLeft = (fromCoordX -1, fromCoordY+1)
            moveRight = (fromCoordX + 1, fromCoordY + 1)
            color = "black"
        if not self.is_valid_move(fromCoord, moveLeft, color):
            direction = "left"
            if self.computer_jump(fromCoord, moveLeft, direction, color):
                if color == "black":
                    newMoveLeft = (fromCoordX - 2, fromCoordY + 2)
                    new_moves = (fromCoord, newMoveLeft)
                    return new_moves
                else:
                    newMoveLeft = (fromCoordX - 2, fromCoordY - 2)
                    new_moves = (fromCoord, newMoveLeft)
                    return new_moves
           
        if not self.is_valid_move(fromCoord, moveRight, color):
            direction = "right"
            if self.computer_jump(fromCoord, moveRight, direction, color):
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
        #fromPiece.is_king

    def computer_jump(self, fromSquare, toSquare, direction, color):
        #toPiece and fromPiece are piece objects
        fromPiece = self.locations.get(fromSquare, None)
        toPiece = self.locations.get(toSquare, None)
        (toCoordX, toCoordY) = toSquare
        (fromCoordX, fromCoordY) = fromSquare
        toCoord = (toCoordX, toCoordY)
        newToKingPiece = False

        #had to change from toCoordX, Y +/- 1 to fromCoordX, Y +/- 2. Otherwise the computer
        #thought it was possible to take a jump when it wasnt and forces a move that can't be taken
        if color == "white":
            doubleLeft = (fromCoordX - 2, fromCoordY - 2)
            doubleRight = (fromCoordX + 2, fromCoordY - 2)
            if fromPiece.is_king:
                doubleBackLeft = (fromCoordX - 2, fromCoordY+ 2)
                doubleBackRight = (fromCoordX + 2, fromCoordY + 2)
        else:
            doubleLeft = (fromCoordX - 2, fromCoordY + 2)
            doubleRight = (fromCoordX + 2, fromCoordY + 2)
            if fromPiece.is_king:
                doubleBackLeft = (fromCoordX - 2, fromCoordY - 2)
                doubleBackRight = (fromCoordX + 2, fromCoordY - 2)

        if fromPiece and not toPiece:
            return False
        elif not 0 <= toCoordX <= 7 and not 0<= toCoordY <=7:
            return False
        elif fromPiece and toPiece:
            if fromPiece.get_color() is not toPiece.get_color():
                if direction == "left":
                    if fromPiece.is_king:
                        newToKingPiece = self.is_valid_move(fromPiece, doubleBackLeft, color)
                        newToPiece = self.is_valid_move(fromPiece, doubleLeft, color)
                    else:
                        newToPiece = self.is_valid_move(fromPiece, doubleLeft, color)
                elif direction == "right":
                    if fromPiece.is_king:
                        newToKingPiece = self.is_valid_move(fromPiece, doubleBackRight, color)
                        newToPiece = self.is_valid_move(fromPiece, doubleRight, color)
                    else:
                        newToPiece = self.is_valid_move(fromPiece, doubleRight, color)

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

    #currently not doing anything, but will use in future
    def adjacent_sqaures(self, piece, color):
        (coordX, coordY) = piece._get_pos()
        fromPiece = (coordX, coordY)
        possible_moves = []
        possible_king_moves = []

        if color == "black":
            right_neighbor = (coordX+1, coordY +1)
            left_neighbor = (coordX-1, coordY +1)

            if self.check_king(fromPiece, coordY+1):
                return possible_king_moves
        else:
            right_neighbor = (coordX+1, coordY -1)
            left_neighbor = (coordX -1, coordY-1)

        return possible_moves, possible_king_moves

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