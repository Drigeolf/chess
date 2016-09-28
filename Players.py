from base_modules import BasePlayer
from msgs import ReadingStatus, ReadInput

class HumanPlayer(BasePlayer):
    '''
    Human player class
    '''
    def __init__(self, ptype='HUMAN', turn=None):
        super(HumanPlayer, self).__init__()
        self.ptype = ptype
        self.turn = turn

    def read_input(self):
        self.board.send_to_bus(ReadingStatus(content="MOVE", player=self))

class AIPlayer(BasePlayer):
    '''
    AI player class
    '''
    def __init__(self, ptype='AI', turn=None):
        super(AIPlayer, self).__init__()
        self.ptype = ptype
        self.turn = turn

    def read_input(self):
        if not self.turn:
            self.board.send_to_bus(ReadInput(content='e2e4', player=self))
        else:
            self.board.send_to_bus(ReadInput(content='d7d5', player=self))
