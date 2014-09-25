__author__ = 'Hannah Saloiye'

from piece import Piece
import pygame
from collections import namedtuple

class Board:
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


    def jump_move(self, toCoord, fromCoord, fromPiece, direction):
        self.locations[(toCoord.x, toCoord.y)] = fromPiece
        del self.locations[(fromCoord.x, fromCoord.y)]
        fromPiece._set_pos((toCoord.x, toCoord.y))

        jumpedPiece = self.locations.get(fromCoord, None)

        if direction == "right" and fromPiece.is_white:
            jumpedPiece = self.locations[(fromCoord.x+1, fromCoord.y-1)]
            del self.locations[fromCoord.x+1, fromCoord.y-1]
            self.black_pieces.remove(jumpedPiece)
        elif direction == "left" and fromPiece.is_white:
            jumpedPiece = self.locations[fromCoord.x-1, fromCoord.y-1]
            del self.locations[fromCoord.x-1, fromCoord.y-1]
            self.black_pieces.remove(jumpedPiece)
        elif direction == "right" and not fromPiece.is_white:
            jumpedPiece = self.locations[fromCoord.x+1, fromCoord.y+1]
            del self.locations[fromCoord.x+1, fromCoord.y+1]
            self.white_pieces.remove(jumpedPiece)
        else:
            jumpedPiece = self.locations[fromCoord.x-1, fromCoord.y+1]
            del self.locations[fromCoord.x-1, fromCoord.y+1]
            self.white_pieces.remove(jumpedPiece)


    def move_human(self, fromSquare, toSquare):
        #validate move
        #single
        #jump

        fromCoord = self.numberToTupleKey[fromSquare]
        toCoord = self.numberToTupleKey[toSquare]
        fromPiece = self.locations.get(fromCoord, None)
        toPiece = self.locations.get(toCoord, None)
        if fromPiece.is_white:
            if (toCoord.x == fromCoord.x+1 or toCoord.x == fromCoord.x -1) and toCoord.y == fromCoord.y-1:
                print(fromPiece.is_king)
                self.single_move(toCoord, fromCoord, fromPiece)
            elif (fromPiece.is_king) and ((toCoord.x == fromCoord.x+1 or toCoord.x == fromCoord.x -1) and toCoord.y == fromCoord.y+1):
                print(fromPiece.is_king)
                self.single_move(toCoord, fromCoord, fromPiece)
            elif (toCoord.x == fromCoord.x+2 or toCoord.x == fromCoord.x - 2) and toCoord.y == fromCoord.y-2:
                if toCoord.x == fromCoord.x+2:
                    direction = "right"
                else:
                    direction = "left"
                self.jump_move(toCoord, fromCoord, fromPiece, direction)
            elif (fromPiece.is_king) and ((toCoord.x == fromCoord.x+2 or toCoord.x == fromCoord.x -2) and toCoord.y == fromCoord.y+2):
                if toCoord.x == fromCoord.x+2:
                    direction = "right"
                else:
                    direction = "left"
                self.jump_move(toCoord, fromCoord, fromPiece, direction)
            else:
                raise Exception ("Invalid human move")
                print('invalid move!')
        if not fromPiece.is_white:
            #print(fromPiece.is_king)
            if (toCoord.x == fromCoord.x + 1 or toCoord.x == fromCoord.x - 1) and toCoord.y == fromCoord.y+1:
                self.single_move(toCoord, fromCoord, fromPiece)
            elif (fromPiece.is_king) and ((toCoord.x == fromCoord.x+1 or toCoord.x == fromCoord.x - 1) and toCoord.y == fromCoord.y-1):
                self.single_move(toCoord, fromCoord, fromPiece)
            elif (toCoord.x == fromCoord.x + 2 or toCoord.x == fromCoord.x - 2) and toCoord.y == fromCoord.y+2:
                if toCoord.x == fromCoord.x+2:
                    direction = "right"
                else:
                    direction = "left"
                self.jump_move(toCoord, fromCoord, fromPiece, direction)
            elif (fromPiece.is_king) and ((toCoord.x == fromCoord.x+2 or toCoord.x == fromCoord.x - 2) and toCoord.y == fromCoord.y-2):
                if toCoord.x == fromCoord.x+2:
                    direction = "right"
                else:
                    direction = "left"
                self.jump_move(toCoord, fromCoord, fromPiece, direction)
            else:
                raise Exception ("Invalid human move")
                print('invalid move!')
    def collidepoint(self, pos):
        return self.boardrect.collidepoint(pos)
