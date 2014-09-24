__author__ = 'Kokouvi Djogbessi'

import sys, pygame
from board import Board
pygame.init()

img_folder = "img/"
bsize = bwidth, bheight = 600, 600
psize = pwidth, pheight = 235, 170
wsize = wwidth, wheight = bwidth + pwidth, bheight

screen = pygame.display.set_mode(wsize, pygame.NOFRAME)

menu = pygame.image.load(img_folder+"main_menu.png")
menu = pygame.transform.scale(menu, bsize)
menurect = menu.get_rect()
console = pygame.image.load(img_folder+"consolebg.png")
console = pygame.transform.scale(console, (pwidth, wheight))

h_play = pygame.image.load(img_folder+"human_play.png")
h_play = pygame.transform.scale(h_play, psize)
h_play.get_rect()
cpu_play = pygame.image.load(img_folder+"cpu_play.png")
cpu_play = pygame.transform.scale(cpu_play, psize)
cpu_play.get_rect()

# ------ TEXT VARS ---------
max_display = 12
font_size = 23
theight = (wheight - pheight) // (max_display)
tsize = twidth, theight = pwidth, theight
typing_text = str()
text_display = list()
text_display.append("Welcome !")
text_display.append("Enter your moves")

# --GET VARS FROM MAIN --
board = Board(screen, bwidth, bheight)
black_pieces = list()
white_pieces = list()
# initializing board


def display(text):
    if text != "":
        text_display.append(text)
        if(len(text_display)>max_display - 1):
            del text_display[0]

def collide(piece_pos, mouse_pos):
    """Rough method to check if the mouses position is in for a piece"""

    return ((mouse_pos[0] < piece_pos[0] * board.pcwidth + board.pcwidth) and (mouse_pos[0] > piece_pos[0]
                                                                   *pcwidth) and
    (mouse_pos[1] < piece_pos[1]* board.pcheight + board.pcheight) and (mouse_pos[1] > piece_pos[1]* board.pcheight))

inmenu = True # displays the menu if True
pcolor = 0
# Get turn?
is_cpu_turn = True
player_is_white = False
show_numbers = False
clicked_piece = None
piece_is_selected = False
selected_number = 0

while 1:
    # TODO: GET TURN
    is_cpu_turn = False
    for event in pygame.event.get():
        if pygame.key.get_mods() & pygame.KMOD_ALT:
            show_numbers = True
        else:
            show_numbers = False
        if event.type == pygame.QUIT: sys.exit()
        if event.type == pygame.MOUSEBUTTONUP:
            if inmenu:
                pos = pygame.mouse.get_pos()
                if pos[0]<bheight/2 - 10:
                    # HUMAN IS WHITE
                    player_is_white = True
                elif  pos[0]>bheight/2 + 10 :
                    # HUMAN IS BLACK
                    player_is_white = False
                inmenu = False
            else:
                pos = pygame.mouse.get_pos()
                if board.collidepoint(pos):
                    clicked_piece = []
                    if player_is_white:
                        clicked_piece = [p for p in white_pieces if collide(p.pos, pos)]
                    else:
                        clicked_piece = [p for p in black_pieces if collide(p.pos, pos)]
                    if piece_is_selected:
                        if not len(clicked_piece)<0:
                            selected_number = 0
                            piece_is_selected = False
                        else:
                            new_selection = 4*clicked_piece[0].pos[1] + clicked_piece[0].pos[0]//2 + 1
                            if new_selection == selected_number:
                                pass
                            else:
                                selected_number = new_selection
                    elif len(clicked_piece):
                        selected_number = 4*clicked_piece[0].pos[1] + clicked_piece[0].pos[0]//2 + 1
                        typing_text += str(selected_number) + " "
                        piece_is_selected = True

        if event.type == pygame.KEYDOWN:
            if not is_cpu_turn:
                char = event.unicode
                typing_text += char
                if pygame.key.get_pressed()[pygame.K_RETURN]:
                    typing_text = typing_text[:-1]
                    if typing_text.lower() == "exit" or typing_text.lower() == "quit":
                        sys.exit(0)
                    elif typing_text == "undo" or typing_text == "u":
                        pass
                    else:
                        display(typing_text.replace(" ",""))
                        try:
                            move_coords = typing_text.split(" ")
                            coord1 = int(move_coords[0])# move([0],[1])
                            coord2 = int(move_coords[1])
                            board.humanMove((coord1, coord2))
                        except Exception as exp:
                            display("Invalid command - %s" %str(exp))
                            print (exp)
                        typing_text = ""
                        #innerLogic.humanMove(move_coords)
                if pygame.key.get_pressed()[pygame.K_BACKSPACE]:
                    typing_text = typing_text[:-1]
                    typing_text = typing_text[:-1]


    board.draw(inmenu)
    if inmenu:
        screen.blit(menu, menurect)
    else:
        screen.blit(console, (bwidth, 0))
        if is_cpu_turn:
            screen.blit(cpu_play, (bwidth, 0))
        else :
            board.draw(inmenu)
            # --- CONSOLE TEXT ---
            fnt = pygame.font.SysFont("Calibri", font_size)
            hintfnt = pygame.font.SysFont("monotype", font_size)
            if show_numbers:
                count = 1
                j = 0
                offset = 5
                while j < 8:
                    i = 0
                    while i < 8:
                        if i % 2 != j % 2:
                            text = hintfnt.render(str(count), 1, (255, 20 , 20))
                            screen.blit(text, (i*board.pcwidth+ offset, j*board.pcheight + offset))
                            count += 1
                        i += 1
                    j += 1
            i = 0

            while i < max_display - 1 and i < len(text_display):
                text = fnt.render("> " + text_display[i], 1, (0, 0, 0))
                screen.blit(text, (bwidth, (i)*theight + pheight))
                i += 1
            text = fnt.render(">> "+typing_text+"_", 1, (0, 0, 0))
            screen.blit(text, (bwidth, (max_display-1)*theight + pheight))
            screen.blit(h_play, (bwidth, 0))
    pygame.display.flip()