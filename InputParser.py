from base_modules import BaseModule
from msgs import ParsedMove, InvalidCommand, QuitGame, GotoMenu

class InputParser(BaseModule):
    def __init__(self):
        super(InputParser, self).__init__()
        self.name = "InputParser"
        self.in_game = False
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
        self.menu_dict = {"MAIN MENU": ["NEW GAME","LOAD GAME","SETTINGS","EXIT GAME"],
                          "NEW GAME": ["SINGLEPLAYER", "LOCAL MULTIPLAYER"],
                          "LOAD GAME": ["NOT_IMPLEMENTED"], 
                          "SETTINGS": ["NOT_IMPLEMENTED"], 
                          "EXIT GAME": ["QUIT_GAME"], 
                          "SINGLEPLAYER": ["NOT_IMPLEMENTED"], 
                          "LOCAL MULTIPLAYER": ["NEW_LMULTI"]}

    def processInput(self, msg):
        inp_str = msg.content
        # Let's first confirm that it's an actual move
        if self.in_game:
            try:
                pMove = self.parseMove(inp_str)
                MM = ParsedMove(content=pMove, raw_text=inp_str, player=msg.player)
            except:
                MM = self.parseCommand(msg)
        else:
            MM = self.parseMenuCommand(msg)
        return MM

    def handle_msg(self, msg):
        if msg.mtype == "READ_INPUT":
            MM = self.processInput(msg)
            self.send_to_bus(MM)
        if msg.mtype == "START_GAME":
            self.in_game = True
        else:
            pass

    def parseMenuCommand(self, msg):
        cmd = msg.content
        if cmd == "exit" or cmd =="quit":
            MM = QuitGame()
        else:
            try:
                self.menu_dict[cmd]
                MM = GotoMenu(content=cmd)
            except KeyError:
                MM = InvalidCommand()
        return MM

    def parseCommand(self, msg):
        cmd = msg.content
        if cmd == "exit" or cmd =="quit":
            MM = QuitGame(content=True)
        else:
            MM = InvalidCommand(player=msg.player)
        return MM

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
            #print("The move not in dictionary, not a valid move: %s"%move)
            raise
    
    def trPiece(self, piece):
        """
        Helper function for translating the chess pieces. Meant to be 
        used for function "map" in order to convert from index to piece.

        """
        try:
            return self.pieceDict[piece]
        except KeyError:
            #print("The piece not in dictionary, not a valid piece: %s"%piece)
            raise
            
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
        try:
            s_col, s_row = map(self.trChar, [start[0], start[1]])
        except KeyError:
            raise

        assert len(end) == 2, "Move description is wrong: %s"%(end)
        try:
            e_col, e_row = map(self.trChar, [end[0], end[1]])
        except KeyError:
            raise
        
        return ( (s_row, s_col), (e_row, e_col) )
