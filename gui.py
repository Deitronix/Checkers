__author__ = 'Kokouvi Djogbessi'

import sys, pygame, threading
from board import Board

class Gui():
    """Thread responsible for all gui updates, including inputs - keyboard and move -"""

    def __init__(self):
        threading.Thread.__init__(self)
        pygame.init()
        img_folder = "img/"
        self.bsize = self.bwidth, self.bheight = 600, 600
        self.psize = self.pwidth, self.pheight = 235, 170
        self.wsize = self.wwidth, self.wheight = self.bwidth + self.pwidth, self.bheight

        self.screen = pygame.display.set_mode(self.wsize, pygame.NOFRAME)

        self.menu = pygame.image.load(img_folder+"main_menu.png")
        self.menu = pygame.transform.scale(self.menu, self.bsize)
        self.menurect = self.menu.get_rect()
        self.console = pygame.image.load(img_folder+"consolebg.png")
        self.console = pygame.transform.scale(self.console, (self.pwidth, self.wheight))

        self.h_play = pygame.image.load(img_folder+"human_play.png")
        self.h_play = pygame.transform.scale(self.h_play, self.psize)
        self.h_play.get_rect()
        self.cpu_play = pygame.image.load(img_folder+"cpu_play.png")
        self.cpu_play = pygame.transform.scale(self.cpu_play, self.psize)
        self.cpu_play.get_rect()

        # ------ TEXT VARS ---------
        self.max_display = 12
        self.font_size = 23
        self.theight = (self.wheight - self.pheight) // (self.max_display)
        self.tsize = self.twidth, self.theight = self.pwidth, self.theight
        self.typing_text = str()
        self.text_display = list()
        self.text_display.append("Welcome !")
        self.text_display.append("Enter your moves")

        # --GET VARS FROM MAIN --
        self.board = Board(self.screen, self.bwidth,self. bheight)
        self.black_pieces = list()
        self.white_pieces = list()

        self.inmenu = True # displays the menu if True
        self.pcolor = 0
        # Get turn
        self.is_cpu_turn = True
        self.player_is_white = False

        self.show_numbers = False
        self.piece_is_selected = False
        self.selected_number = 0


    def display(self, text):
        if text != "":
            self.text_display.append(text)
            if(len(self.text_display)>self.max_display - 1):
                del self.text_display[0]

    def collide(self, piece_pos, mouse_pos):
        """Rough method to check if the mouses position is in for a piece"""

        return ((mouse_pos[0] < piece_pos[0] * self.board.pcwidth + self.board.pcwidth) and (mouse_pos[0] > piece_pos[0]
                                                                       *self.board.pcwidth) and
        (mouse_pos[1] < piece_pos[1]*self.board.pcheight + self.board.pcheight) and (mouse_pos[1] > piece_pos[1]* self.board.pcheight))

    def show(self):
        while 1:
            # TODO: GET TURN
            for event in pygame.event.get():
                if pygame.key.get_mods() & pygame.KMOD_ALT:
                    self.show_numbers = True
                else:
                    self.show_numbers = False
                if event.type == pygame.QUIT: sys.exit()
                if event.type == pygame.MOUSEBUTTONUP:
                    if self.inmenu:
                        pos = pygame.mouse.get_pos()
                        if pos[0]<self.bheight/2 - 10:
                            # HUMAN IS WHITE
                            self.player_is_white = True
                            self.is_cpu_turn = True
                        elif  pos[0]>self.bheight/2 + 10 :
                            # HUMAN IS BLACK
                            self.player_is_white = False
                            self.is_cpu_turn = False
                        self.inmenu = False
                    else:
                        pos = pygame.mouse.get_pos()
                        if self.board.collidepoint(pos):
                            clicked_piece = []
                            if self.player_is_white:
                                clicked_piece = [p for p in self.white_pieces if self.collide(p.pos, pos)]
                            else:
                                clicked_piece = [p for p in self.black_pieces if self.collide(p.pos, pos)]
                            if self.piece_is_selected:
                                if not len(clicked_piece)<0:
                                    self.selected_number = 0
                                    self.piece_is_selected = False
                                else:
                                    new_selection = 4*clicked_piece[0].pos[1] + clicked_piece[0].pos[0]//2 + 1
                                    if new_selection == self.selected_number:
                                        pass
                                    else:
                                        self.selected_number = new_selection
                            elif len(clicked_piece):
                                self.selected_number = 4*clicked_piece[0].pos[1] + clicked_piece[0].pos[0]//2 + 1
                                self.typing_text += str(self.selected_number) + " "
                                self.piece_is_selected = True
                                #TODO Finish selection process

                if event.type == pygame.KEYDOWN:
                    if not self.is_cpu_turn:
                        char = event.unicode
                        self.typing_text += char
                        if pygame.key.get_pressed()[pygame.K_RETURN]:
                            self.typing_text = self.typing_text[:-1]
                            if self.typing_text.lower() == "exit" or self.typing_text.lower() == "quit":
                                sys.exit(0)
                            elif self.typing_text == "undo" or self.typing_text == "u":
                                pass
                            else:
                                self.display(self.typing_text)
                                try:
                                    move_coords = self.typing_text.split(" ")
                                    coord1 = int(move_coords[0])# move([0],[1])
                                    coord2 = int(move_coords[1])
                                    self.board.move_human(coord1, coord2)
                                except Exception as exp:
                                    self.display("Invalid command - %s" %str(exp))
                                    print (exp)
                                self.typing_text = ""
                                #innerLogic.humanMove(move_coords)
                        if pygame.key.get_pressed()[pygame.K_BACKSPACE]:
                            self.typing_text = self.typing_text[:-1]
                            self.typing_text = self.typing_text[:-1]


            self.board.draw(self.inmenu)
            if self.inmenu:
                self.screen.blit(self.menu, self.menurect)
            else:
                self.screen.blit(self.console, (self.bwidth, 0))
                if self.is_cpu_turn:
                    self.screen.blit(self.cpu_play, (self.bwidth, 0))
                else :
                    # --- CONSOLE TEXT ---
                    fnt = pygame.font.SysFont("Calibri", self.font_size)
                    hintfnt = pygame.font.SysFont("monotype", self.font_size)
                    if self.show_numbers:
                        count = 1
                        j = 0
                        offset = 5
                        while j < 8:
                            i = 0
                            while i < 8:
                                if i % 2 != j % 2:
                                    text = hintfnt.render(str(count), 1, (255, 20 , 20))
                                    self.screen.blit(text, (i*self.board.pcwidth+ offset, j*self.board.pcheight + offset))
                                    count += 1
                                i += 1
                            j += 1

                    #TODO - Wrap lines
                    # - Input display
                    text = fnt.render(">> "+self.typing_text+"_", 1, (0, 0, 0))
                    self.screen.blit(text, (self.bwidth, (self.max_display-1)*self.theight + self.pheight))
                    self.screen.blit(self.h_play, (self.bwidth, 0))

                    #-- Console display
                    i = 0
                while i < self.max_display - 1 and i < len(self.text_display):
                    text = fnt.render("> " + self.text_display[i], 1, (0, 0, 0))
                    self.screen.blit(text, (self.bwidth, i*self.theight + self.pheight))
                    i += 1
            pygame.display.flip()

if __name__ == '__main__':
    gui = Gui()
    #Synchronize with inside comps
    gui.show()