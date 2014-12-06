'''gui.py - this file create a graphical user interface that takes in user input and determines what
color that user is and whether they went first or second. It also indicates to the user whether it is
their turn or the computers
'''

import sys, pygame, threading
from newBoard import Board
#from board import Board
import _thread

class Gui():
    """Main class responsible for all gui updates, including inputs - keyboard and move -"""

    def __init__(self):
        pygame.init()
        img_folder = "img/"
        self.bsize = self.bwidth, self.bheight = 600, 600
        self.psize = self.pwidth, self.pheight = 235, 170
        self.wsize = self.wwidth, self.wheight = self.bwidth + self.pwidth, self.bheight

        self.screen = pygame.display.set_mode(self.wsize)

        self.menu = pygame.image.load(img_folder+"main_menu.png")
        self.menu = pygame.transform.scale(self.menu, self.bsize)
        self.menurect = self.menu.get_rect()
        self.human_win= pygame.image.load(img_folder+"human_win.png")
        self.human_win = pygame.transform.scale(self.human_win, self.bsize)
        self.cpu_win= pygame.image.load(img_folder+"cpu_win.png")
        self.cpu_win = pygame.transform.scale(self.cpu_win, self.bsize)
        self.console = pygame.image.load(img_folder+"consolebg.png")
        self.console = pygame.transform.scale(self.console, (self.pwidth, self.wheight))

        self.h_play = pygame.image.load(img_folder+"human_play.png")
        self.h_play = pygame.transform.scale(self.h_play, self.psize)
        self.h_play.get_rect()
        self.cpu_play_img = pygame.image.load(img_folder+"cpu_play.png")
        self.cpu_play_img = pygame.transform.scale(self.cpu_play_img, self.psize)
        self.cpu_play_img.get_rect()

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
        self.board = Board(self.screen, self.bwidth,self. bheight, self)
        self.black_pieces = list()
        self.white_pieces = list()

        self.inmenu = True # displays the menu if True
        self.pcolor = 0

        self.is_cpu_turn = True
        self.cpu_is_playing = False
        self.player_is_white = False

        self.show_numbers = False
        self.piece_is_selected = False
        self.selected_number = 0

        self.top_display = 0
        self.playing = False
        self.auto_playing = False


    def display(self, text):
        if text != "":
            self.text_display.append(text)
            if(len(self.text_display)>self.max_display - 1):
                self.top_display += 1

    def collide(self, piece_pos, mouse_pos):
        """Rough method to check if the mouses position is in for a piece"""

        return ((mouse_pos[0] < piece_pos[0] * self.board.pcwidth + self.board.pcwidth) and (mouse_pos[0] > piece_pos[0]
                                                                       *self.board.pcwidth) and
        (mouse_pos[1] < piece_pos[1]*self.board.pcheight + self.board.pcheight) and (mouse_pos[1] > piece_pos[1]* self.board.pcheight))

    def show(self):
        turn = 0
        text_offset = 0
        ratio_speed = 700
        direction = 1
        self.playing = True
        while self.playing:
            while True:
                for event in pygame.event.get():
                    if pygame.key.get_mods() & pygame.KMOD_ALT:
                        self.show_numbers = True
                    else:
                        self.show_numbers = False
                    if event.type == pygame.QUIT: sys.exit()

                    if event.type == pygame.MOUSEBUTTONUP:
                        if self.inmenu:
                            pos = pygame.mouse.get_pos()
                            if pos[1] < self.bheight/2:
                                # HUMAN IS WHITE
                                turn = 1
                                self.player_is_white = True
                                self.is_cpu_turn = True
                            elif pos[1] > self.bheight/2:
                                # HUMAN IS BLACK
                                self.player_is_white = False
                                self.is_cpu_turn = False
                            self.inmenu = False
                        else:
                            pos = pygame.mouse.get_pos()
                            if self.board.collidepoint(pos):
                                posx = pos[0]//self.board.pcwidth
                                posy = pos[1]//self.board.pcheight
                            #    try:
                               #     # Add selection to piece movement
                               #     selected_piece = self.board.locations[(posx,posy)]
                               #     self.piece_is_selected = True
                               #     self.selected_number = posy * 4 + posx // 2 + 1
                               # except KeyError :
                               #     #no piece exists at that position
                               #     if selected_piece.is_white == self.player_is_white:
                               #         if self.piece_is_selected:
                               #             to_location = posy * 4 + posx // 2 + 1
                               #             self.move("{} {}".format(self.selected_number, to_location))
                               #     self.piece_is_selected = False

                    if event.type == pygame.KEYDOWN:
                        # if not self.is_cpu_turn:
                        char = event.unicode
                        self.typing_text += char
                        if pygame.key.get_pressed()[pygame.K_RETURN]:
                            self.typing_text = self.typing_text[:-1]
                            if self.typing_text.lower() == "exit" or self.typing_text.lower() == "quit":
                                sys.exit(0)
                            elif self.typing_text == "undo" or self.typing_text == "u":
                                pass
                            elif self.typing_text.startswith("auto"):
                                if not self.auto_playing:
                                    _thread.start_new_thread(self.auto_play, ())
                                self.auto_playing = True
                                self.display(self.typing_text)
                                self.display("Auto-play ON")
                                self.typing_text = ""
                            elif self.typing_text.startswith("manual"):
                                self.auto_playing = False
                                self.display(self.typing_text)
                                self.display("Auto-play OFF")
                                self.typing_text = ""
                            else:
                                # ---- HUMAN PLAY ----#
                                if not self.is_cpu_turn:
                                    self.display(self.typing_text)
                                    if self.move(self.typing_text):
                                        self.is_cpu_turn = True
                                        turn = 1
                                    self.typing_text = ""

                        if pygame.key.get_pressed()[pygame.K_BACKSPACE]:
                            self.typing_text = self.typing_text[:-1]
                            self.typing_text = self.typing_text[:-1]

                        if pygame.key.get_pressed()[pygame.K_UP]:
                            self.top_display -= 1
                            if self.top_display < 0:
                                self.top_display = 0
                        if pygame.key.get_pressed()[pygame.K_DOWN]:
                            if self.top_display < len(self.text_display) - 1:
                                self.top_display += 1

                self.board.draw(self.inmenu)

                fnt = pygame.font.SysFont("Calibri", self.font_size)
                hintfnt = pygame.font.SysFont("monotype", self.font_size)
                if self.inmenu:
                    self.screen.blit(self.menu, self.menurect)
                    pygame.display.flip()
                else:
                    self.screen.blit(self.console, (self.bwidth, 0))
                    if self.is_cpu_turn:
                        self.screen.blit(self.cpu_play_img, (self.bwidth, 0))
                    else:
                        self.screen.blit(self.h_play, (self.bwidth, 0))
                    # --- CONSOLE TEXT ---
                    # Show numbers
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

                    # - Input display
                    text = fnt.render(">> "+self.typing_text+"_", 1, (0, 0, 0))
                    self.screen.blit(text, (self.bwidth, (self.max_display-1)*self.theight + self.pheight))

                    #-- Console display
                    i = 0
                    text_offset += direction
                    if text_offset<0 or text_offset>2*ratio_speed/3:
                        direction *= -1
                    i = self.top_display
                    current_d = 0
                    while current_d < self.max_display - 1 and i < len(self.text_display):
                        text = fnt.render("> " + self.text_display[i], 1, (0, 0, 0))
                        speed = 0
                        if text.get_width() > self.pwidth: # if text is too big
                            speed = text.get_width()/ratio_speed # get its speed ratio
                        self.screen.blit(text, (self.bwidth, current_d*self.theight + self.pheight),
                                         (speed*text_offset, 0, self.twidth, self.theight))
                        i += 1
                        current_d += 1

                    pygame.display.flip()
                    #- CPU play
                    if self.is_cpu_turn:
                        self.screen.blit(self.cpu_play_img, (self.bwidth, 0))

                        #--- THREAD DRIVEN CPU PLAY ----------
                        #Uncomment this line to set active
                        #if not self.cpu_is_playing:
                        #    _thread.start_new_thread(self.cpu_play, ())
                        #self.cpu_is_playing = True
                        #"""
                        #-------------------
                        self.cpu_play() #dont forget to reactivate this line after
                        if False:
                            #TODO Use human moves-check function ^
                            # IF HUMAN HAS NO MOVES (board.human_has_moves?)
                            self.screen.blit(self.cpu_win, (0,0))
                            self.after_game()
    def move(self, display_text):
        """
        Method for human play, through a string with the squares to use (Example: "23 11")

        :param display_text: string containing the squares for the play
        :return: True if human playe correctly
        """
        try:
            user_jump_exists = False
            if not self.auto_playing:
                if self.board.check_for_human_moves(self.player_is_white):

                    move_coords = self.typing_text.split(" ")
                    coord1 = int(move_coords[0])# move([0],[1])
                    coord2 = int(move_coords[1])

                    #print(user_jump_exists)
                    #coords = eval(self.typing_text.split(" "))
                    #if type(coords) is tuple and all(type(n) is int for n in coords):
                    #    self.board.human_controller(*coords)'''

                    #elif(self.board.check_for_human_jumps(self.player_is_white)):
                    if self.board.find_human_jumps(self.player_is_white):
                        #the user must jump

                        if self.board.is_jump(coord1, coord2, self.player_is_white):
                            self.board.human_controller(coord1, coord2, self.player_is_white)
                            if self.board.check_for_human_jumps(coord2):
                                return False
                            else:
                                return True
                        else:
                            raise Exception ("You must take a jump when the situation arises")
                    else:
                        #no jump available, the user makes a normal use
                        self.board.human_controller(coord1, coord2, self.player_is_white)
                        return True
                    #self.is_cpu_turn = True
                    #return True
                else:
                    raise Exception ("There are no valid moves left for the human player")
        except Exception as exp:
                self.display("Invalid command - %s" %str(exp))
                print (exp)
                return False


    def after_game(self):
        """
        This method will be called when the game is over

        :return:
        """
        self.playing = False
        pygame.display.flip()

    def auto_play(self):
        while self.auto_playing:
            if not self.is_cpu_turn:
                print("Auto - Playing...")
                if self.player_is_white:
                    computer_played = self.board.computer_turn("white")
                else:
                    computer_played = self.board.computer_turn("black")
                print("Auto - Played")
            self.is_cpu_turn = True

    def cpu_play(self):
        print("CPU - Playing...")
        if self.player_is_white:
            computer_played = self.board.computer_turn("black")
        else:
            computer_played = self.board.computer_turn("white")
        if not computer_played:
            # IF CPU HAS NO MOVES
            self.screen.blit(self.human_win, (0,0))
            self.after_game()

        print("CPU - Played!")
        self.cpu_is_playing = False
        self.is_cpu_turn = False

if __name__ == '__main__':
    gui = Gui()
    gui.show()