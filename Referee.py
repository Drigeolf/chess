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

    def validateInput(self, inp_move):
        vMove = inp_move
        PM = BaseMsg(content=vMove, mtype="VALID_MOVE")
        return PM

    def handle_msg(self, msg):
        if msg.mtype == "PARSED_MOVE":
            PM = self.validateInput(msg.content)
            self.send_to_bus(PM)
        else:
            pass
