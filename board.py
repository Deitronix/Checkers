__author__ = 'Hannah Saloiye'

from piece import Piece
import pygame

class Board:
    locations = dict()
    black_pieces = list()
    white_pieces = list()
    img_folder = "img/"
    #boardimg
    #boardrect
    #width
    #height
   # screen

    def __init__(self, screen, width, height):
        self.screen = screen
        self.width = width
        self.height = height

        self.boardimg = pygame.image.load(self.img_folder+"board.png")
        self.boardimg = pygame.transform.scale(self.boardimg, (width,height))
        self.boardrect = self.boardimg.get_rect()
        self.star = pygame.image.load(self.img_folder + "star.png")

        # initializing black pieces
        x = 0
        y = 0

        while y < 3:
            x = 0
            while x < 8:

                if x % 2 != y % 2:
                    print("(" + str(x) + " " + str(y) + ")")
                    piece = Piece(screen=self.screen, is_white=False, pos=(x,y), width=self.width//8, height=self.height//8)
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
                    print("(" + str(x) + " " + str(y) + ")")
                    piece = Piece(screen = self.screen, is_white=True, pos=(x,y), width=self.width//8, height=self.height//8)
                    self.locations[(x, y)] = piece
                    self.white_pieces.append(piece)
                x += 1
            y += 1


    def draw(self):
            # -- DRAWING BOARD ---
            self.screen.blit(self.boardimg, self.boardrect)
            for piece in self.black_pieces:
                piece.draw()
            for piece in self.white_pieces:
                #self.screen.blit(self.white_pc_img, (piece.pos[0]*self.width, (piece.pos[1])*self.height))
                 piece.draw()
            self.screen.blit(self.star, (0, 0));