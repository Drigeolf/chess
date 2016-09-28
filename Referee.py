# Title: Referee class 
# Author: Vedat Sinan Ural, Ali Sinan Saglam
# Contact: vsural@gmail.com, asinansaglam@gmail.com
# Created on Sat Jun 13 23:53:13 2015

import numpy as np
from base_modules import BaseModule 
from msgs import ValidMove, InvalidMove
 
class CRef(BaseModule):
    """
    A referee class for the chess engine. 
    This class checks the validity of moves and controls the flow of 
    the game. 
    """
    def __init__(self):
        super(CRef,self).__init__()
        self.name = "Referee"

    def get_board_state(self):
        # ensure we have the board
        self.board_obj = self.att_modules["MainBus"].get_module("Board")
        self.turn = self.board_obj.turn
        self.pieceDict = self.board_obj.pieceDict

    def validateInput(self, msg):
        inp_move = msg.content
        self.get_board_state()
        # Check to see if correct piece is moving
        stPiece = self.board_obj.getSquare(inp_move[0])
        stCheck = self.check_starting_piece(stPiece)
        # Now check to see if the movement is correct
        mvCheck = self.movement_check(inp_move, stPiece)
        # 
        if stCheck and mvCheck:
            PM = ValidMove(content=inp_move)
        else:
            PM = InvalidMove(content=True, player=msg.player)
        return PM

    def check_starting_piece(self, piece):
        # Make sure a piece is actually selected
        if piece == ".":
            return False
        # Ensure correct turn
        if not self.turn:
            if piece != abs(piece):
                return False
        else:
            if piece == abs(piece):
                return False
        return True

    def movement_check(self, inp_move, piece):
        # We have the starting position and the piece id
        # let's start implementing everything here first, maybe
        # I'll move them out to different functions later

        # Start with pawns
        if piece == 1:
            # Temporarily forget about en-passant
            valid_moves = self.calc_wpawn(inp_move)
            if inp_move in valid_moves:
                return True
            else:
                return False
        elif piece == -1:
            valid_moves = self.calc_bpawn(inp_move)
            if inp_move in valid_moves:
                return True
            else:
                return False
        # Knights
        elif piece == 2 or piece == -2:
            valid_moves = self.calc_knight(inp_move)
            if inp_move in valid_moves:
                return True
            else:
                return False
        ## Bishops
        #elif piece == 3 or piece == -3:
        #    valid_moves = self.calc_bishop(inp_move)
        #    if inp_move in valid_moves:
        #        return True
        #    else:
        #        return False
        ## Rooks
        #elif piece == 4 or piece == -4:
        #    valid_moves = self.calc_rook(inp_move)
        #    if inp_move in valid_moves:
        #        return True
        #    else:
        #        return False
        ## Queens
        #elif piece == 5 or piece == -5:
        #    valid_moves = self.calc_queen(inp_move)
        #    if inp_move in valid_moves:
        #        return True
        #    else:
        #        return False
        ## Kings
        #elif piece == 6 or piece == -6:
        #    valid_moves = self.calc_king(inp_move)
        #    if inp_move in valid_moves:
        #        return True
        #    else:
        #        return False
        ## Incorrect selection
        #else:
        #    return False


    def check_empty(self, square):
        if self.board_obj.getSquare(square) == 0:
            return True
        return False

    def calc_wpawn(self, move_tpl):
        valid_moves = []
        st,fn = move_tpl
        st1, st2 = st
        fn1, fn2 = fn
        
        # Currently only checking to see if we can move to an empty
        # space, no capture, no en-passant, no checking the first square
        # in front
        if st1 == 1:
            if self.check_empty((3,st2)):
                valid_moves.append((st, (3,st2)))
        if self.check_empty((st1+1,st2)):
            valid_moves.append((st, (st1+1,st2)))
        return valid_moves

    def calc_bpawn(self, move_tpl):
        valid_moves = []
        st,fn = move_tpl
        st1, st2 = st
        fn1, fn2 = fn
        
        # Currently only checking to see if we can move to an empty
        # space, no capture, no en-passant, no checking the first square
        # in front
        if st1 == 6:
            if self.check_empty((4,fn2)):
                valid_moves.append((st, (4,fn2)))
        if self.check_empty((fn1-1,fn2)):
            valid_moves.append((st, (fn1-1,fn2)))
        return valid_moves

    def calc_knight(self, move_tpl):
        valid_moves = []
        st,fn = move_tpl
        st1, st2 = st
        fn1, fn2 = fn

        # Currently only checking for empty space, no capture
        if (st1+2 <= 7):
            if (st2+1) <= 7:
                if self.check_empty((st1+2,st2+1)):
                    valid_moves.append((st,(st1+2,st2+1)))
            if ((st2-1) >= 0):
                if self.check_empty((st1+2,st2-1)):
                    valid_moves.append((st,(st1+2,st2-1)))
        if (st1-2 >= 0):
            if (st2+1) <= 7:
                if self.check_empty((st1-2,st2+1)):
                    valid_moves.append((st,(st1-2,st2+1)))
            if ((st2-1) >= 0):
                if self.check_empty((st1-2,st2-1)):
                    valid_moves.append((st,(st1-2,st2-1)))
        return valid_moves

    def calc_bishop(self, move_tpl):
        valid_moves = []
        st,fn = move_tpl
        st1, st2 = st
        fn1, fn2 = fn

    def handle_msg(self, msg):
        if msg.mtype == "PARSED_MOVE":
            PM = self.validateInput(msg)
            PM.raw_text = msg.raw_text
            self.send_to_bus(PM)
        else:
            pass
