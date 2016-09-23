from base_modules import BaseModule
from base_modules import BaseMsg

class MoveParser(BaseModule):
    def __init__(self):
        super(MoveParser, self).__init__()
        self.name = "Parser"
        # Parser related
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

    def processMove(self, inp_str):
        pMove = self.parseMove(inp_str)
        MM = BaseMsg(content=pMove, mtype="PARSED_MOVE")
        return MM

    def handle_msg(self, msg):
        if msg.mtype == "READ_INPUT":
            MM = self.processMove(msg.content)
            self.send_to_bus(MM)
        else:
            pass

    def parseMove(self, move, notation="longAlg"):
        """
        Move parser of the chess board. Will eventually support multiple
        notations via the kwarg notation. 
    
        Arguments:
          Move (arg): 
            Move in string format, make sure the notation fits the specifications
            found here: https://en.wikipedia.org/wiki/Chess_notation
          Notation (kwarg):
            The notation of the move. Currently only long algebraic notation is available.
   
        Returns:
          Parsed move in ((start coord tuple), (end coord tuple)) format.
        """
        if notation == "longAlg":
            return self.parseLongAlg(move)
        else: 
            NotImplementedError
            
    def trChar(self, move):
        """
        Helper function for translating the chess notation. Meant to be 
        used for function "map" in order to convert from notation to index. 

        """
        try:
            return self.moveDict[move]
        except KeyError:
            print("The move not in dictionary: %s"%move)
            raise
    
    def trPiece(self, piece):
        """
        Helper function for translating the chess pieces. Meant to be 
        used for function "map" in order to convert from index to piece.

        """
        return self.pieceDict[piece]
            
    def parseLongAlg(self, move):
        """
        Parser for Long Algebraic chess notation. 
        
        Arguments:
          Move (str): 
            Move description as a string in long algebraic
            chess notation.
            https://en.wikipedia.org/wiki/Chess_notation
            It's formatted as: x#-y# where x,y are 
            columns (letters a-h), and #s are rows 1-8. 
            TODO: Learn how to link with rst. 

        Returns (tuple): 
          Returns a tuple fully describing one move in format
          ( (starting coord of move), (ending coord of move) )
          coords are in 2D tuples. 
        """
        
        assert isinstance(move, basestring), "Move is not a string"
        
        start, end = move[0:2], move[2:4]
        
        assert len(start) == 2, "Move description is wrong: %s"%(start)
        s_col, s_row = map(self.trChar, [start[0], start[1]])
        
        assert len(end) == 2, "Move description is wrong: %s"%(end)
        e_col, e_row = map(self.trChar, [end[0], end[1]])
        
        return ( (s_row, s_col), (e_row, e_col) )
