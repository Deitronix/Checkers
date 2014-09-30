__author__ = 'Hannah Saloiye'

from piece import Piece
import pygame
from collections import namedtuple

class Board:
    anotherJump = False #for use with the computer move and jumping
    right = 0 #to determine which way the computer is moving right = 0 is right right = 1 is left
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




    def validateStart(self, boardLocation):
        print("in validate Start")

    def single_move(self, toCoord, fromCoord, fromPiece):
        self.locations[(toCoord.x, toCoord.y)] = fromPiece
        del self.locations[(fromCoord.x, fromCoord.y)]

        fromPiece._set_pos((toCoord.x, toCoord.y))
        self.check_king(fromPiece, toCoord.y)

    def jump_move(self, toCoord, fromCoord, fromPiece, direction):
        self.locations[(toCoord.x, toCoord.y)] = fromPiece
        del self.locations[(fromCoord.x, fromCoord.y)]
        fromPiece._set_pos((toCoord.x, toCoord.y))
        print("from piece.pos is: ")
        print(fromPiece.pos)

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
                jumpedPiece = self.locations[fromCoord.x+1, fromCoord.y+1]
                del self.locations[fromCoord.x+1, fromCoord.y+1]
                self.white_pieces.remove(jumpedPiece)
            elif(toCoord.x<fromCoord.x) and toCoord.y<fromCoord.y:#backwards left
                jumpedPiece = self.locations[fromCoord.x-1, fromCoord.y+1]
                del self.locations[fromCoord.x-1, fromCoord.y+1]
                self.white_pieces.remove(jumpedPiece)
        else:
            print("not a valid jump")




    def move_human(self, fromSquare, toSquare):

        fromCoord = self.numberToTupleKey[fromSquare]
        toCoord = self.numberToTupleKey[toSquare]
        fromPiece = self.locations.get(fromCoord, None)
        toPiece = self.locations.get(toCoord, None)
        if fromPiece and not toPiece:
            if fromPiece.is_white:
                if (toCoord.x == fromCoord.x+1 or toCoord.x == fromCoord.x - 1) and toCoord.y == fromCoord.y-1:
                    self.single_move(toCoord, fromCoord, fromPiece)
                elif (toCoord.x == fromCoord.x+2 or toCoord.x == fromCoord.x - 2) and toCoord.y == fromCoord.y-2:
                    if toCoord.x == fromCoord.x+2:
                        direction = "right"
                    else:
                        direction = "left"
                    self.jump_move(toCoord, fromCoord, fromPiece, direction)
                elif fromPiece.is_king:
                    if (toCoord.x == fromCoord.x+1 or toCoord.x == fromCoord.x -1) and toCoord.y == fromCoord.y+1:
                        self.single_move(toCoord, fromCoord, fromPiece)
                    elif(toCoord.x == fromCoord.x+2 or toCoord.x == fromCoord.x -2) and toCoord.y == fromCoord.y+2:
                        if toCoord.x == fromCoord.x+2:
                            direction = "right"
                        else:
                            direction = "left"
                        self.jump_move(toCoord, fromCoord, fromPiece, direction)
                else:
                    raise Exception("Invalid human move")
            if not fromPiece.is_white:
                if (toCoord.x == fromCoord.x + 1 or toCoord.x == fromCoord.x - 1) and toCoord.y == fromCoord.y+1:
                    self.single_move(toCoord, fromCoord, fromPiece)
                elif (toCoord.x == fromCoord.x + 2 or toCoord.x == fromCoord.x - 2) and toCoord.y == fromCoord.y+2:
                    if toCoord.x == fromCoord.x+2:
                        direction = "right"
                    else:
                        direction = "left"
                    self.jump_move(toCoord, fromCoord, fromPiece, direction)
                elif(fromPiece.is_king):
                    if(toCoord.x == fromCoord.x+1 or toCoord.x == fromCoord.x - 1) and toCoord.y == fromCoord.y-1:
                        self.single_move(toCoord, fromCoord, fromPiece)
                    elif (toCoord.x == fromCoord.x+2 or toCoord.x == fromCoord.x - 2) and toCoord.y == fromCoord.y-2:
                        if toCoord.x == fromCoord.x+2:
                            direction = "right"
                        else:
                            direction = "left"
                    self.jump_move(toCoord, fromCoord, fromPiece, direction)

                else:
                    raise Exception("Invalid human move")
        else:
            raise Exception("Invalid human move!")

    def collidepoint(self, pos):
        return self.boardrect.collidepoint(pos)


    def computerMove(self):
        possible_moves = self.find_next_states()
    # Choose a move somehow... for now you can probably do:
        if possible_moves:
            next_move = possible_moves[ 0 ]
            #check to see if anotherJump has already occurred and if there isn't a new jump to be made
            if self.anotherJump and self.jumpFlag == 0:
                self.anotherJump = False
                return
            if self.jumpFlag == 1:
                self.make_move_computer(next_move)
                self.jumpFlag = 0
                self.anotherJump = True
                self.computerMove()
            else:
                self.make_move_computer(next_move)
        else:
            raise Exception ("No valid moves exist for computer.")


    def find_next_states(self):
        next_states = []
        for piece in self.black_pieces:
            valid_moves = self.find_valid_moves(piece)
            (move, jump) = valid_moves
            #add next states to list instead of making a list of lists with append
            if jump:
               next_states = jump + next_states

            else:
                if not self.jumpFlag == 1:
                    next_states += move
#        for valid_move in valid_moves:
#            next_states.append( self.copy_board(valid_move))

        return next_states

    def find_valid_moves(self, piece):
        valid_moves = []
        valid_jump_moves = []
        (coordX, coordY) = piece._get_pos()
#        compColor = piece.get_color()
        fromSquare = (coordX, coordY)

        if not piece.is_white:
            moveToLeft = (coordX - 1, coordY + 1)
            moveToRight = (coordX + 1, coordY + 1)
            #if piece.is_king:
            #   moveBackLeft = (coordX-1, coordY-1)
            #   moveBackRight = (coordX+1, coordY-1)
        else:
            moveToLeft = (coordX - 1, coordY - 1)
            moveToRight = (coordX + 1, coordY - 1)
            #if piece.is_king:
            #    moveBackLeft = (coordX-1, coordY+1)
            #   moveBackRight = (coordX+1, coordY+1)
#       jump move
        if not self.is_valid_move(fromSquare, moveToLeft):
            direction = "left"
            if self.computer_jump(fromSquare, moveToLeft, direction):
                newMoveLeft = (coordX - 2, coordY + 2)
                valid_jump_moves.append((fromSquare, newMoveLeft))
                self.right = 1
        #       single move
        else:
            if not self.jumpFlag == 1:
                valid_moves.append((fromSquare, moveToLeft))

        if not self.is_valid_move(fromSquare, moveToRight):
            direction = "right"
            if self.computer_jump(fromSquare, moveToRight, direction):
                newMoveRight = (coordX + 2, coordY + 2)
                valid_jump_moves.append((fromSquare, newMoveRight))
                self.right = 0
        else:
            if not self.jumpFlag == 1:
                valid_moves.append((fromSquare, moveToRight))

        return (valid_moves, valid_jump_moves)

    def is_valid_move(self, fromCoord, toCoord):
        fromPiece = self.locations.get(fromCoord, None)
        toPiece = self.locations.get(toCoord, None)
        (toCoordX, toCoordY) = toCoord


        return not toPiece and 0 <= toCoordX <= 7 and 0 <= toCoordY <= 7


    def make_move_computer(self, next_move):
        (fromCoord, toCoord) = next_move
        fromPiece = self.locations[fromCoord]
        self.locations[toCoord] = fromPiece
        (CoordX, CoordY) = fromCoord

        #jump left and update board
        if self.jumpFlag == 1 and self.right == 1:
                jumpedPiece = self.locations[(CoordX-1, CoordY+1)]
                self.white_pieces.remove(jumpedPiece)
                del self.locations[CoordX-1, CoordY+1]
                self.check_king(fromPiece, CoordY)
        #jump right and update board
        elif self.jumpFlag == 1 and self.right == 0:
                jumpedPiece = self.locations[(CoordX+1, CoordY+1)]
                self.white_pieces.remove(jumpedPiece)
                del self.locations[CoordX+1, CoordY+1]
                self.check_king(fromPiece, CoordY)

        del self.locations[fromCoord]
        fromPiece._set_pos(toCoord)
        self.check_king(fromPiece, CoordY)

    def computer_jump(self, fromSquare, toSquare, direction):

        #toPiece and fromPiece are piece objects
        fromPiece = self.locations.get(fromSquare, None)
        toPiece = self.locations.get(toSquare, None)

        (toCoordX, toCoordY) = toSquare
        toCoord = (toCoordX, toCoordY)

        doubleLeft = (toCoordX - 1, toCoordY + 1)
        doubleRight = (toCoordX + 1, toCoordY + 1)

        if toPiece and Piece.get_color(toPiece) == Piece.get_color(fromPiece):
           return
        elif not (0,0) <= toCoord <= (7,7) and ((0,0)<=doubleLeft<=(7,7) or (0,0)<=doubleRight<=(7,7)):
            return
        else:
            if direction == "left":
                newToPiece = self.is_valid_move(fromPiece, doubleLeft)
            elif direction == "right":
                newToPiece = self.is_valid_move(fromPiece, doubleRight)

            if newToPiece:
                self.jumpFlag = 1
                return True
            return

    def check_king(self, fromPiece, CoordY):

        if fromPiece.is_white:
            if CoordY == 0:
                fromPiece.make_king()
            else:
                return
            print("in check_king")
            print(fromPiece.is_king)
        else:
            if CoordY == 7:
                fromPiece.make_king()
            else:
                return