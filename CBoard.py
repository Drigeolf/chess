# Title: Chess Board Class and its methods
# Author: Vedat Sinan Ural, Ali Sinan Saglam
# Contact: vsural@gmail.com, asinansaglam@gmail.com
# Created on Sat Jun 13 23:53:13 2015

import numpy as np
from base_modules import BaseModule
from base_modules import BaseMsg
 
class CBoard(BaseModule):
    """
    A Chess board class written for our
    Chess engine program.
 
    Contains the current state of the board
    as well as methods for move generation.
 
    board is the representation of the chess board.
    Uses an 8x8 numpy array.
 
    turn indicates whether it's white's or black's turn;
    turn = 0 -> White's turn.
    turn = 1 -> Black's turn.
 
    cw, cb are castling status for white and black
    respectively. 0 means castling is allowed 1 means
    it is not allowed.
 
    threp is the status of the threefold repetition move
    threp = 0 means the rule isn't invoked.
 
    move50 is the status of the 50 move rule. If it is 0
    the rule isn't invoked.

    check shows if a king is in check currently in the board state
    """
    def __init__(self, board=None, turn=0, cw=0, cb=0, threp=0, move50=0, check=0):
        # First module related business
        super(CBoard, self).__init__()
        self.name = "Board"
        # Now board specific attributes
        self.board = board
        self.turn = 0
        self.cw = cw
        self.cb = cb
        self.threp = threp
        self.move50 = move50
        self.check = check 
        self.moveDict = { 
             "a": 0, "b": 1, "c": 2, 
             "d": 3, "e": 4, "f": 5, 
             "g": 6, "h": 7, "A": 0, 
             "B": 1, "C": 2, "D": 3, 
             "E": 4, "F": 5, "G": 6, 
             "H": 7, "1": 0, "2": 1, 
             "3": 2, "4": 3, "5": 4, 
             "6": 5, "7": 6, "8": 7 }
        self.pieceDict = {
              0: ".", 1: "P", 2: "N", 
              3: "B", 4: "R", 5: "Q",
              6: "K", -1: "o", -2: "n", 
              -3: "b", -4: "r", -5: "q",
              -6: "k" }
        # At least for now just initialize the board
        self.initBoard()

    def processMove(self, val_move):
        self.movePiece(val_move)
        ProM = BaseMsg(content=(self.board, self.turn), mtype="PROCESSED_MOVE")
        return ProM

    def sendBoard(self):
        ProM = BaseMsg(content=(self.board, self.turn), mtype="RENDER_BOARD")
        return ProM

    def handle_msg(self, msg):
        if msg.mtype == "VALID_MOVE":
            ProM = self.processMove(msg.content)
            self.send_to_bus(ProM)
        elif msg.mtype == "DISPLAY_BOARD":
            ProM = self.sendBoard()
            self.send_to_bus(ProM)
        else:
            pass
 
    def initBoard(self, gameType="normal"):
        """
        Method to initialize the board.
        It sets the board to an 8x8 numpy array with
        all the pieces in the starting position.
        """
        if gameType == "normal":
            self.initNormal()
        else: 
            raise NotImplementedError
            
    def initNormal(self):
        # Sets the board to an empty 8x8 np.array
        self.board = np.zeros((8, 8), int)
         
        # Setting up the pawns in place
        self.board[1][:] = 1
        self.board[6][:] = -1  # minus represents a black piece
 
        # Setting up rest of the white pieces
        self.board[0][0] = self.board[0][7] = 4  # Rooks
        self.board[0][1] = self.board[0][6] = 2  # Knights
        self.board[0][2] = self.board[0][5] = 3  # Bishops
        self.board[0][3] = 5  # Queen
        self.board[0][4] = 6  # King
 
        # Setting up rest of the black pieces
        self.board[7][0] = self.board[7][7] = -4  # Rooks
        self.board[7][1] = self.board[7][6] = -2  # Knights
        self.board[7][2] = self.board[7][5] = -3  # Bishops
        self.board[7][3] = -5  # Queen
        self.board[7][4] = -6  # King
        
        # Make it white's turn
        self.turn = 0
 
    def clearBoard(self):
        """
        Method to clear the board entirely.

        """
        self.board = np.zeros((8, 8), int)
        
    def movePiece(self, moveIndices):
        """
        Method to move the piece
   
        Arguments:
          MoveIndices: 
            Indices for the move in the format 
            ( (start tuple), (end tuple) )

        Returns:
          Nothing, just modifies the board. 
        """
        start, end = moveIndices[0], moveIndices[1]
        assert (start[0] < 8 and start[0] >= 0), "Starting point out of board."
        assert (start[1] < 8 and start[1] >= 0), "Starting point out of board."
        assert (end[0] < 8 and end[0] >= 0), "Ending point out of board."
        assert (end[1] < 8 and end[1] >= 0), "Ending point out of board."
        self.board[end] = self.board[start]
        self.board[start] = 0
        self.turn = (self.turn+1)%2
    
    def getSquare(self, coord):
        """
        Returns the piece at square indicated by coordinate given. 

        Arguments: 
          Coord (tuple): Coordinate of the square in tuple (row, column)

        Returns: 
          The contents of the square which can be passed to the piece
          dictionary to find out what piece it is. 
          
        """
        return self.board[coord]
