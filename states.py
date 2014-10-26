from piece import Piece
import pygame
from collections import namedtuple
import copy
from board import Board

def dfs_game_tree_rec(current_state, level, color):

    #if level is greater than a max of 6, end the recursive call
    if level >= 4:
        ((next_move),(black_pieces, white_pieces, location)) = current_state
        current_kings = 0
        #figure out current number of kings for evaluator
        for piece in black_pieces:
            if piece.is_king:
                current_kings += 1
        for piece in white_pieces:
            if piece.is_king:
                current_kings += 1
        #if there is a jump, take it and stop looking at other options
        if check_jump(next_move):
            current_state = ((next_move),(black_pieces, white_pieces, location))
            return (next_move, evaluate_board(current_state, current_kings, color))
        else:
            current_state = ((next_move),(black_pieces, white_pieces, location))
            return (next_move, evaluate_board(current_state, current_kings, color))

    else:
        #if the level is greater than 0, check to see if there is a jump
        #if so just return the jump move as soon as possible
        if level > 0:
            #current state now has a move associated with it
            ((next_move),(black_pieces, white_pieces, location)) = current_state
            current_state = (black_pieces, white_pieces, location)
            current_kings = 0

            if check_jump(next_move):
                current_state = ((next_move),(black_pieces, white_pieces, location))
                return (next_move, evaluate_board(current_state, current_kings, color))

        #next state is a node of the tree
        next_states = get_next_states(current_state, color)
        #depending if it's your turn or the opponents, min or max the nodes
        if is_player(level):
            #calling this method with new parameter values based off of some n in next_state
            #returns min value choice
            #also ensures to pass back the "parent" current state and not the child's current state
            #return min((dfs_game_tree_rec(n, level+1, color) for n in next_states), key = lambda a:a[1])
            (min_next_move, (_, score)) = min(((n, dfs_game_tree_rec(n, level+1, "white")) for n in next_states), key = lambda tpl: tpl[1][1])
            return (min_next_move, score)
        else:
            #returns max value choice
            #return max((dfs_game_tree_rec(n, level+1, color) for n in next_states), key = lambda a:a[1])
            (max_next_move, (_, score)) = max(((n, dfs_game_tree_rec(n, level+1, "black")) for n in next_states), key = lambda tpl: tpl[1][1])

            return (max_next_move, score)

def is_player(level):
    if level%2 == 1:
        return True
    else:
        return False

#thought I might need this, but appear not to
def switch_color(color):
    if color == "black":
        return "white"
    elif color == "white":
        return "black"

#def evaluate_board(current_state, color):
def evaluate_board(current_state, current_kings, color):
    ((fromCoord, toCoord), (black_pieces, white_pieces, location)) = current_state
    (fromCoordX, fromCoordY) = fromCoord
    (toCoordX, toCoordY) = toCoord

    valued_squares = ((2, 1), (4,1), (3, 2), (5, 2), (2, 3), (4, 3),
                (3, 4), (5, 4), (2, 5), (4, 5), (3, 6), (5, 6))

    value = 0
    if color == "black":
        if (len(black_pieces) - len(white_pieces)) > (len(white_pieces) - len(black_pieces)):
            value = value + 4
        black_king_count = 0
        for piece in black_pieces:
            if piece.is_king:
               black_king_count += 1
        if current_kings < black_king_count:
            value += 3

        if (location in valued_squares):
            value += 2
        #if len(white_pieces) + len(black_pieces) = 10
        # add distance into consideration value += 2;
        if check_jump((fromCoord,toCoord)):
            value += 20
        else:
            value = value + 1
    if color == "white":
        if (len(white_pieces) - len(black_pieces)) > (len(black_pieces) - len(white_pieces)):
            value = value + 4
        white_king_count = 0
        for piece in black_pieces:
            if piece.is_king:
               white_king_count += 1
        if current_kings < white_king_count:
            value += 3

        if (location in valued_squares):
            value += 2
        #if len(white_pieces) + len(black_pieces) = 10
        # add distance into consideration value += 2;
        if check_jump((fromCoord,toCoord)):
            value += 20
        else:
            value = value + 1
    return value



def copy_board(current_state):
    (black_pieces, white_pieces, locations) = current_state
    copy_locations = copy.deepcopy(locations)
    #iterating for each piece that is stored in the locations dictionary
    copy_white_pieces = [piece for piece in copy_locations.values() if piece.is_white]
    copy_black_pieces= [piece for piece in copy_locations.values() if not piece.is_white]
    copied_current_state = (copy_black_pieces, copy_white_pieces, copy_locations)

    return copied_current_state

def get_next_states(current_state, color):
    #(location, black_pieces, white_pieces) = current_state
    new_states = []
    moves = valid_moves(current_state, color)
    for m in moves:
        if check_jump(m):
            new_states.append(apply_move(m, copy_board(current_state)))
            return new_states
        else:
            new_states.append(apply_move(m, copy_board(current_state)))
    return new_states

def check_jump(move):
    (fromCoord, toCoord) = move
    (fromCoordX, fromCoordY) = fromCoord
    (toCoordX, toCoordY) = toCoord

    #a jump is at least 2 spaces away in a positive or negative direction
    if fromCoordY - toCoordY == 2 or fromCoordY + toCoordY == 2 or fromCoordY - toCoordY == -2 or fromCoordY + toCoordY == -2:
        return True
    else:
        return False

def valid_moves(current_state, color):
    #find all valid moves based off of current state passed through
    (black_pieces, white_pieces, location) = current_state
    next_moves = []

    if color == "black":
        for piece in black_pieces:
            valid_moves = find_valid_moves(current_state, piece, color)
            (move, jump) = valid_moves
            next_moves = jump + next_moves + move

    else:
        for piece in white_pieces:
            valid_moves = find_valid_moves(current_state, piece, color)
            (move, jump) = valid_moves
            #add next states to list instead of making a list of lists with append
            next_moves = jump + next_moves + move
    return next_moves

def apply_move (move, copied_current_state):
    #make the move based off of the copied board
    (fromCoord, toCoord) = move
    (black_pieces, white_pieces, location) = copied_current_state
    (fromCoordX, fromCoordY) = fromCoord
    fromPiece = location[fromCoord]
    location[toCoord] = fromPiece
    (fromCoordX, fromCoordY) = fromCoord
    (toCoordX, toCoordY) = toCoord

    #check to see if a piece can be jumped...if so set the flag.
    #might be able to get rid of all other jumpFlags being set to 1 or 0
    if check_jump(move):
        Board.jumpFlag = 1
    else:
        Board.jumpFlag = 0

    #check to see what color is being played and what needs to be removed
    if fromPiece.is_white:
        if fromPiece.is_king and Board.jumpFlag == 1 and (fromCoordX > toCoordX) and (fromCoordY < toCoordY):
            jumpedPiece = location[(fromCoordX-1, fromCoordY+1)]
            black_pieces.remove(jumpedPiece)
            del location[fromCoordX-1, fromCoordY+1]
        elif fromPiece.is_king and Board.jumpFlag == 1 and (fromCoordX < toCoordX) and (fromCoordY < toCoordY):
            jumpedPiece = location[(fromCoordX+1, fromCoordY+1)]
            black_pieces.remove(jumpedPiece)
            del location[fromCoordX+1, fromCoordY+1]
        #jump right forward and update board
        elif Board.jumpFlag == 1 and (fromCoordX < toCoordX) and (fromCoordY > toCoordY):
            jumpedPiece = location[(fromCoordX+1, fromCoordY-1)]
            black_pieces.remove(jumpedPiece)
            del location[fromCoordX+1, fromCoordY-1]
        #jump left forward and update board
        elif Board.jumpFlag == 1 and (fromCoordX > toCoordX) and (fromCoordY > toCoordY):
            jumpedPiece = location[(fromCoordX-1, fromCoordY-1)]
            black_pieces.remove(jumpedPiece)
            del location[fromCoordX-1, fromCoordY-1]
    else:
        if fromPiece.is_king and Board.jumpFlag == 1 and (fromCoordX > toCoordX) and (fromCoordY > toCoordY):
            jumpedPiece = location[(fromCoordX-1, fromCoordY-1)]
            white_pieces.remove(jumpedPiece)
            del location[fromCoordX-1, fromCoordY-1]
        elif fromPiece.is_king and Board.jumpFlag == 1 and (fromCoordX < toCoordX) and (fromCoordY > toCoordY):
            jumpedPiece = location[(fromCoordX+1, fromCoordY-1)]
            white_pieces.remove(jumpedPiece)
            del location[fromCoordX+1, fromCoordY-1]
        #jump left forward and update board
        if Board.jumpFlag == 1 and ((fromCoordX > toCoordX) and (fromCoordY < toCoordY)):
            #if not self.right:
            jumpedPiece = location[(fromCoordX-1, fromCoordY+1)]
            white_pieces.remove(jumpedPiece)
            del location[fromCoordX-1, fromCoordY+1]
        #jump right forward and update board (forward to black side)
        elif Board.jumpFlag == 1 and (fromCoordX < toCoordX) and (fromCoordY < toCoordY):
            jumpedPiece = location[(fromCoordX+1, fromCoordY+1)]
            white_pieces.remove(jumpedPiece)
            del location[fromCoordX+1, fromCoordY+1]
        #will allow to update for single moves
        if Board.jumpFlag == 1:
            Board.jumpFlag = 0
            del location[fromCoord]
            fromPiece._set_pos(toCoord)

            if not fromPiece.is_king:
                check_king(fromPiece, toCoordY)
                if fromPiece.is_king:
                    return ((fromCoord, toCoord), copied_current_state)

            next_moves = multiple_jump(copied_current_state, toCoord, fromPiece)
            if next_moves:
            #is not None:
                apply_move(next_moves, copied_current_state)
        else:

            del location[fromCoord]
            fromPiece._set_pos(toCoord)
            check_king(fromPiece, toCoordY)

    return ((fromCoord, toCoord), copied_current_state)

def multiple_jump(current_state, fromCoord, fromPiece):
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
            if not is_valid_move(current_state, fromCoord, backwardLeft, color):
                direction = "backwardLeft"
                if computer_jump(current_state, fromCoord, backwardLeft, direction, color):
                    newMoveLeft = (fromCoordX - 2, fromCoordY - 2)
                    new_moves = (fromCoord, newMoveLeft)
                    return new_moves
            if not is_valid_move(current_state, fromCoord, forwardLeft, color):
                direction = "forwardLeft"
                if computer_jump(current_state, fromCoord, forwardLeft, direction, color):
                    newMoveLeft = (fromCoordX - 2, fromCoordY + 2)
                    new_moves = (fromCoord, newMoveLeft)
                    return new_moves
        else:
            if not is_valid_move(current_state, fromCoord, backwardLeft, color):
                direction = "backwardLeft"
                if computer_jump(current_state, fromCoord, backwardLeft, direction, color):
                    newMoveLeft = (fromCoordX - 2, fromCoordY + 2)
                    new_moves = (fromCoord, newMoveLeft)
                    return new_moves
            if not is_valid_move(current_state, fromCoord, forwardLeft, color):
                direction = "forwardLeft"
                if computer_jump(current_state, fromCoord, forwardLeft, direction, color):
                    newMoveLeft = (fromCoordX - 2, fromCoordY - 2)
                    new_moves = (fromCoord, newMoveLeft)
                    return new_moves

    if fromPiece.is_king:
        if color == "black":
            if not is_valid_move(current_state, fromCoord, backwardRight, color):
                direction = "backwardRight"
                if computer_jump(current_state, fromCoord, backwardRight, direction, color):
                    newMoveRight = (fromCoordX + 2, fromCoordY - 2)
                    new_moves = (fromCoord, newMoveRight)
                    return new_moves
            if not is_valid_move(current_state, fromCoord, forwardRight, color):
                direction = "forwardRight"
                if computer_jump(current_state, fromCoord, forwardRight, direction, color):
                    newMoveRight = (fromCoordX + 2, fromCoordY + 2)
                    new_moves = (fromCoord, newMoveRight)
                    return new_moves
        else:
            if not is_valid_move(current_state, fromCoord, backwardRight, color):
                direction = "backwardRight"
                if computer_jump(current_state, fromCoord, backwardRight, direction, color):
                    newMoveRight = (fromCoordX + 2, fromCoordY +2)
                    new_moves = (fromCoord, newMoveRight)
                    return new_moves
            if not is_valid_move(current_state, fromCoord, forwardRight, color):
                direction = "forwardRight"
                if computer_jump(current_state, fromCoord, forwardRight, direction, color):
                    newMoveRight = (fromCoordX + 2, fromCoordY - 2)
                    new_moves = (fromCoord, newMoveRight)
                    return new_moves

    if not is_valid_move(current_state, fromCoord, forwardLeft, color):
        direction = "forwardLeft"
        if computer_jump(current_state, fromCoord, forwardLeft, direction, color):
            if color == "black":
                newMoveLeft = (fromCoordX - 2, fromCoordY + 2)
                new_moves = (fromCoord, newMoveLeft)
                return new_moves
            else:
                newMoveLeft = (fromCoordX - 2, fromCoordY - 2)
                new_moves = (fromCoord, newMoveLeft)
                return new_moves

    if not is_valid_move(current_state, fromCoord, forwardRight, color):
        direction = "forwardRight"
        if computer_jump(current_state, fromCoord, forwardRight, direction, color):
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

def find_valid_moves(current_state, piece, color):
    (black_pieces, white_pieces, location) = current_state
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
    if piece.is_king and not is_valid_move(current_state, fromSquare, moveBackLeft, color):
        direction = "backwardLeft"
        if computer_jump(current_state, fromSquare, moveBackLeft, direction, color):
            if color == "black":
                newMoveLeft = (coordX - 2, coordY - 2)
                jumped_piece = location[coordX-1, coordY-1]
                valid_jump_moves.append((fromSquare, newMoveLeft))
            else:
                newMoveLeft = (coordX - 2, coordY + 2)
                jumped_piece = location[coordX-1, coordY + 1]
                valid_jump_moves.append((fromSquare, newMoveLeft))
    elif piece.is_king and is_valid_move(current_state, fromSquare, moveBackLeft, color):
        valid_moves.append((fromSquare, moveBackLeft))

    if piece.is_king and not is_valid_move(current_state, fromSquare, moveBackRight, color):
        direction = "backwardRight"
        if computer_jump(current_state, fromSquare, moveBackRight, direction, color):
            if color == "black":
                newMoveRight = (coordX + 2, coordY - 2)
                jumped_piece = location[coordX + 1, coordY - 1]
                valid_jump_moves.append((fromSquare, newMoveRight))
            else:
                newMoveRight = (coordX + 2, coordY + 2)
                jumped_piece = location[coordX+1, coordY+1]
                valid_jump_moves.append((fromSquare, newMoveRight))
    elif piece.is_king and is_valid_move(current_state, fromSquare, moveBackRight, color):
        valid_moves.append((fromSquare, moveBackRight))

    if not is_valid_move(current_state, fromSquare, moveToLeft, color):
        direction = "forwardLeft"
        if computer_jump(current_state, fromSquare, moveToLeft, direction, color):
            if color == "black":
                newMoveLeft = (coordX - 2, coordY + 2)
                jumped_piece = location[coordX-1, coordY+1]
                valid_jump_moves.append((fromSquare, newMoveLeft))
            else:
                newMoveLeft = (coordX - 2, coordY - 2)
                jumped_piece = location[coordX-1, coordY-1]
                valid_jump_moves.append((fromSquare, newMoveLeft))

    #single move
    else:
        valid_moves.append((fromSquare, moveToLeft))

    if not is_valid_move(current_state, fromSquare, moveToRight, color):
        direction = "forwardRight"
        if computer_jump(current_state, fromSquare, moveToRight, direction, color):
            if color == "black":
                newMoveRight = (coordX + 2, coordY + 2)
                jumped_piece = location[coordX+1, coordY+1]
                valid_jump_moves.append((fromSquare, newMoveRight))
            else:
                newMoveRight = (coordX + 2, coordY - 2)
                jumped_piece = location[coordX+1, coordY-1]
                valid_jump_moves.append((fromSquare, newMoveRight))
    #single move
    else:
        valid_moves.append((fromSquare, moveToRight))

    return valid_moves, valid_jump_moves

def is_valid_move(current_move, fromCoord, toCoord, color):
    (black_pieces, white_pieces, locations) = current_move
    fromPiece = locations.get(fromCoord, None)
    toPiece = locations.get(toCoord, None)
    (toCoordX, toCoordY) = toCoord

    return not toPiece and 0 <= toCoordX <= 7 and 0 <= toCoordY <= 7

def computer_jump(current_state, fromSquare, toSquare, direction, color):
    (black_pieces, white_pieces, locations) = current_state
    #toPiece and fromPiece are piece objects
    fromPiece = locations.get(fromSquare, None)
    toPiece = locations.get(toSquare, None)
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
                if fromPiece.is_king and is_valid_move(current_state, fromPiece, backwardJumpLeft, color):
                    newToKingPiece = True
            elif direction == "backwardRight":
                if fromPiece.is_king and is_valid_move(current_state, fromPiece, backwardJumpRight, color):
                    newToKingPiece = True
            elif direction == "forwardLeft":
                if fromPiece.is_king and is_valid_move(current_state, fromPiece, forwardJumpLeft, color):
                    newToPiece = True
                elif is_valid_move(current_state, fromPiece, forwardJumpLeft, color):
                    newToPiece = True
            elif direction == "forwardRight":
                if fromPiece.is_king and is_valid_move(current_state, fromPiece, forwardJumpRight, color):
                    newToPiece = True
                elif is_valid_move(current_state, fromPiece, forwardJumpRight, color):
                    newToPiece = True

            if newToPiece and newToKingPiece:
                Board.jumpFlag = 1
                return True
            elif newToKingPiece:
                Board.jumpFlag = 1
                return True
            elif newToPiece:
                Board.jumpFlag = 1
                return True
    return False

def check_king(fromPiece, CoordY):

    if fromPiece.is_white:
        if CoordY == 0:
            fromPiece.make_king()
        else:
            return
    else:
        if CoordY == 7:
            fromPiece.make_king()
        else:
            return