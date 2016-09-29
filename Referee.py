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
    This class checks the validity of moves and handles
    move generation for any purpose
    """
    def __init__(self):
        super(CRef,self).__init__()
        self.name = "Referee"
        self.N = np.array([1,0])
        self.S = np.array([-1,0])
        self.E = np.array([0,1])
        self.W = np.array([0,-1])

    def get_board_state(self):
        # ensure we have the board
        self.board_obj = self.att_modules["MainBus"].get_module("Board")
        self.turn = self.board_obj.turn
        self.pieceDict = self.board_obj.pieceDict

    def validateInput(self, msg):
        inp_move = msg.content
        self.get_board_state()
        # Re-writing this section with a different logic
        moves = self.gen_moves()
        # Let's test 
        #driver = self.att_modules['MainBus'].att_modules['Display']
        #for move in moves:
        #    test_board = self.board_obj.testMove(move)
        #    driver.BD.displayMove((test_board, self.turn))
        #
        if inp_move in moves:
            PM = ValidMove(content=inp_move)
        else:
            PM = InvalidMove(content=True, player=msg.player)
        return PM

    def gen_moves(self):
        # turn checking
        N, S, E, W = self.N, self.S, self.E, self.W
        if not self.turn:
            pieces = [1,2,3,4,5,6]
            epieces = [-1,-2,-3,-4,-5,-6]
            directions = {1:[N, N+N, N+E, N+W], 2:[N+N+E, N+N+W, S+S+E, S+S+W, E+E+N, E+E+S, W+W+N, W+W+S], 
                          3:[N+E, N+W, S+E, S+W], 4:[N,S,E,W], 5:[N,S,E,W,N+E,N+W,S+E,S+W], 
                          6:[N,S,E,W,N+E,N+W,S+E,S+W]}
        else:
            pieces = [-1,-2,-3,-4,-5,-6]
            epieces = [1,2,3,4,5,6]
            directions = {-1:[S, S+S, S+E, S+W], -2:[N+N+E, N+N+W, S+S+E, S+S+W, E+E+N, E+E+S, W+W+N, W+W+S], 
                          -3:[N+E, N+W, S+E, S+W], -4:[N,S,E,W], -5:[N,S,E,W,N+E,N+W,S+E,S+W], 
                          -6:[N,S,E,W,N+E,N+W,S+E,S+W]}
        # Pieces are the keys to the pieceDict that we want to 
        # generate moves for
        moves = []
        for i in range(8):
            for j in range(8):
                piece = self.board_obj.board[i][j]
                pos = np.array([i,j])
                if piece in pieces:
                    dirs = directions[piece]
                    for idir in dirs:
                        # Sort out pawns here
                        if ((piece == pieces[0]) or (piece == pieces[1]) or (piece == pieces[5])):
                            # OOB checking
                            npos = pos + np.array(idir)
                            if (npos > 7).any() or (npos < 0).any(): continue
                            npiece = self.board_obj.board[npos[0],npos[1]]
                            # Landing piece checking
                            if npiece in pieces: continue
                            if npiece in epieces: 
                                moves.append(np.array([pos,npos]))
                                break
                            moves.append(np.array([pos,npos]))
                        else:
                        # Every other piece here
                            for k in range(1,9):
                                npos = pos + np.array(idir) * k
                                # OOB checking
                                if (npos > 7).any() or (npos < 0).any(): break
                                # Landing piece checking
                                npiece = self.board_obj.board[npos[0],npos[1]]
                                if npiece in pieces: break
                                if npiece in epieces: 
                                    moves.append(np.array([pos,npos]))
                                    break
                                moves.append(np.array([pos,npos]))
        return np.array(moves)

    def handle_msg(self, msg):
        if msg.mtype == "PARSED_MOVE":
            PM = self.validateInput(msg)
            PM.raw_text = msg.raw_text
            self.send_to_bus(PM)
        else:
            pass
