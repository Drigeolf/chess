# Title: Referee class 
# Author: Vedat Sinan Ural, Ali Sinan Saglam
# Contact: vsural@gmail.com, asinansaglam@gmail.com
# Created on Sat Jun 13 23:53:13 2015

import numpy as np
from base_modules import BaseModule 
from base_modules import BaseMsg
 
class CRef(BaseModule):
    """
    A referee class for the chess engine. 
    This class checks the validity of moves and controls the flow of 
    the game. 
    """
    def __init__(self):
        super(CRef,self).__init__()
        self.name = "Referee"
        self.running = True

    def get_board_state(self):
        # ensure we have the board
        self.board_obj = self.att_modules["MainBus"].get_module("Board")
        self.turn = self.board_obj.turn
        self.pieceDict = self.board_obj.pieceDict

    def validateInput(self, inp_move):
        self.get_board_state()
        stPiece = self.board_obj.getSquare(inp_move[0])
        stcheck = self.check_starting_piece(stPiece)
        if stcheck:
            PM = BaseMsg(content=inp_move, mtype="VALID_MOVE")
        else:
            print("Invalid move inputted, try again.")
            PM = BaseMsg(content=True, mtype="READING_STATUS")
        return PM

    def check_starting_piece(self, piece):
        if not self.turn:
            if piece != abs(piece):
                return False
        else:
            if piece == abs(piece):
                return False
        return True

    def handle_msg(self, msg):
        if msg.mtype == "PARSED_MOVE":
            PM = self.validateInput(msg.content)
            self.send_to_bus(PM)
        else:
            pass
