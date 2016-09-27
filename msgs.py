from base_modules import BaseMsg

# A description of all msgs we have
class ReadInput(BaseMsg):
    '''
    This is the msg from the input reader, passing the input entered by the player
    to the main bus. Text is the content 
    '''
    def __init__(self, content=None, mtype='READ_INPUT'):
        self.content = content
        self.mtype = mtype

class ReadCommand(BaseMsg):
    '''
    Msg that gets sent out from the input parser, if the input is not a move
    and is a command of invalid input.
    '''
    def __init__(self, content=None, mtype='READ_COMMAND'):
        self.content = content
        self.mtype = mtype

class ParsedMove(BaseMsg):
    '''
    Msg from the move parser, returning the move in a way the board/referee will understand.
    Also returns the original raw text.
    '''
    def __init__(self, content=None, mtype='PARSED_MOVE', raw_text=''):
        self.content = content
        self.raw_text = raw_text
        self.mtype = mtype

class ValidMove(BaseMsg):
    '''
    Msg from the Referee, this is the move that is validated and ready to be passed
    to board for processing.
    '''
    def __init__(self, content=None, mtype='VALID_MOVE', raw_text=''):
        self.content = content
        self.raw_text = raw_text
        self.mtype = mtype

class InvalidMove(BaseMsg):
    '''
    Invalid move command 
    '''
    def __init__(self, content=None, mtype='INVALID_MOVE', raw_text=''):
        self.content = content
        self.mtype = mtype

class InvalidCommand(BaseMsg):
    '''
    Invalid command 
    '''
    def __init__(self, content=None, mtype='INVALID_COMMAND', raw_text=''):
        self.content = content
        self.mtype = mtype

class QuitGame(BaseMsg):
    '''
    Command to quit the game
    '''
    def __init__(self, content=None, mtype='QUIT_GAME'):
        self.content = content
        self.mtype = mtype

class ProcessedMove(BaseMsg):
    '''
    Msg from the board, indicating a move is processed after validation, also returns the board state
    in it's content. This is used for rendering the board after making the move. 
    '''
    def __init__(self, content=None, mtype='PROCESSED_MOVE'):
        self.content = content
        self.mtype = mtype


class ReadingStatus(BaseMsg):
    '''
    Msg that can be used to turn input reading on and off. True in content indicates that the system
    is ready to take in input, false indicates otherwise.
    '''
    def __init__(self, content=None, mtype='READING_STATUS'):
        self.content = content
        self.mtype = mtype

class DisplayBoard(BaseMsg):
    '''
    Msg that can be used to display the board, it's read by board class to signal the need to show the 
    board to the player, w/o making a move
    '''
    def __init__(self, content=None, mtype='DISPLAY_BOARD', tmodule="Board"):
        self.content = content
        self.mtype = mtype
        self.tmodule = tmodule

class RenderBoard(BaseMsg):
    '''
    Msg that can be used to display the board, it's read by board class to signal the need to show the 
    board to the player, w/o making a move
    '''
    def __init__(self, content=None, mtype='RENDER_BOARD', tmodule="Display"):
        self.content = content
        self.mtype = mtype
        self.tmodule = tmodule

class RenderMenu(BaseMsg):
    '''
    Msg to display the menu. Contains the dictionary of menus and the information about the previous menu 
    we are coming from, incase we have to return to it
    '''
    def __init__(self, content=None, mtype='RENDER_MENU', menu_dict=None, prev_menu=None, tmodule="Display"):
        self.content = content
        self.menu_dict = menu_dict
        self.prev_menu = prev_menu
        self.mtype = mtype
        self.tmodule = tmodule

class GotoMenu(BaseMsg):
    '''
    Msg to signal GameState to heat to a particular menu
    '''
    def __init__(self, content=None, mtype='GOTO_MENU', tmodule="GameState"):
        self.content = content
        self.mtype = mtype
        self.tmodule = tmodule

class StartGame(BaseMsg):
    '''
    Msg that can be used to display the board, it's read by board class to signal the need to show the 
    board to the player, w/o making a move
    '''
    def __init__(self, content=None, mtype='START_GAME', tmodule="GameState"):
        self.content = content
        self.mtype = mtype
        self.tmodeul = tmodule 

class InitGame(BaseMsg):
    '''
    Msg that can be used to display the board, it's read by board class to signal the need to show the 
    board to the player, w/o making a move
    '''
    def __init__(self, content=None, mtype='INIT_GAME', tmodule="GameState"):
        self.content = content
        self.mtype = mtype
        self.tmodule = tmodule
