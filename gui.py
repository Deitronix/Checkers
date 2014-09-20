__author__ = 'Kokouvi Djogbessi'

import sys, pygame
from piece import Piece
pygame.init()

img_folder = "img/"
bsize = bwidth, bheight = 600, 600
psize = pwidth, pheight = 235, 170
wsize = wwidth, wheight = bwidth + pwidth, bheight
pcsize = pcwidth, pcheight = bwidth//8, bheight//8

screen = pygame.display.set_mode(wsize, pygame.NOFRAME)
boardimg = pygame.image.load(img_folder+"board.png")
boardimg = pygame.transform.scale(boardimg, bsize)
boardrect = boardimg.get_rect()
menu = pygame.image.load(img_folder+"main_menu.png")
menu = pygame.transform.scale(menu, bsize)
menurect = menu.get_rect()
console = pygame.image.load(img_folder+"consolebg.png")
console = pygame.transform.scale(console, (pwidth, wheight - pheight))
white_pc_img = pygame.image.load(img_folder+"white_piece.png")
white_pc_img = pygame.transform.scale(white_pc_img, pcsize)
black_pc_img = pygame.image.load(img_folder+"black_piece.png")
black_pc_img = pygame.transform.scale(black_pc_img, pcsize)

h_play = pygame.image.load(img_folder+"human_play.png")
h_play = pygame.transform.scale(h_play, psize)
h_play.get_rect()
cpu_play = pygame.image.load(img_folder+"cpu_play.png")
cpu_play = pygame.transform.scale(cpu_play, psize)
cpu_play.get_rect()

# ------ TEXT VARS ---------
max_display = 10
font_size = 25
theight = (wheight - pheight) // (max_display)
tsize = twidth, theight = pwidth, theight
typing_text = str()
text_display = list()
text_display.append("Welcome !")
text_display.append("Enter your moves")

# --GET VARS FROM MAIN --
board = dict()
black_pieces = list()
white_pieces = list()
# initializing board

# initializing black pieces
x = 0
y = 0

while y < 3:
    x = 0
    while x < 8:

        if x % 2 != y % 2:
            print("(" + str(x) + " " + str(y) + ")")
            piece = Piece(is_white=False, pos=(x,y))
            board[(x, y)] = piece
            black_pieces.append(piece)
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
            piece = Piece(is_white=True, pos=(x,y))
            board[(x, y)] = piece
            white_pieces.append(piece)
        x += 1
    y += 1

def display(text):
    if text != "":
        text_display.append(text)
        if(len(text_display)>max_display - 1):
            del text_display[0]



inmenu = True # displays the menu if True
pcolor = 0
# Get turn?
is_cpu_turn = True

while 1:
    # TODO: GET TURN
    is_cpu_turn = False
    for event in pygame.event.get():
        if event.type == pygame.QUIT: sys.exit()
        if event.type == pygame.MOUSEBUTTONUP:
            if inmenu :
                pos = pygame.mouse.get_pos()
                if(pos[0]<bheight/2 - 10):
                    # HUMAN IS WHITE
                    pass
                elif(pos[0]>bheight/2 + 10):
                    # HUMAN IS BLACK
                    pass
                inmenu = False
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
                    else :
                        display(typing_text)
                        try:
                            move_coords = typing_text.split(" ")
                            coord1 = int(move_coords[0])# move([0],[1])
                            coord2 = int(move_coords[1])
                        except:
                            display("Invalid command")
                        typing_text = ""
                if pygame.key.get_pressed()[pygame.K_BACKSPACE]:
                    typing_text = typing_text[:-1]
                    typing_text = typing_text[:-1]


    screen.blit(boardimg, boardrect)
    if inmenu:
        screen.blit(menu, menurect)
    else :
        screen.blit(console, (bwidth, pheight))
        if is_cpu_turn:
            screen.blit(cpu_play, (bwidth, 0))
        else :
            # -- DRAWING BOARD ---
            for piece in black_pieces:
                screen.blit(black_pc_img, (piece.pos[0]*pcwidth, (piece.pos[1])*pcheight))
            for piece in white_pieces:
                screen.blit(white_pc_img, (piece.pos[0]*pcwidth, (piece.pos[1])*pcheight))

            # --- CONSOLE TEXT ---
            fnt = pygame.font.SysFont("Calibri", font_size)
            i = 0
            while i < max_display - 1 and i < len(text_display):
                text = fnt.render("> " + text_display[i], 1, (0, 0, 0))
                screen.blit(text, (bwidth, (i)*theight + pheight))
                i += 1
            text = fnt.render(">>"+typing_text+"_", 1, (255, 255, 0))
            screen.blit(text, (bwidth, (max_display-1)*theight + pheight))
            screen.blit(h_play, (bwidth, 0))
    pygame.display.flip()
