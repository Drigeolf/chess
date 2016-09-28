from base_modules import BasePlayer

class HumanPlayer(BasePlayer):
    '''
    Human player class
    '''
    def __init__(self, ptype='HUMAN'):
        self.ptype = ptype
        self.turn = turn

    def read_input(self):
        self.send_to_bus(ReadingStatus(content="MOVE"))
        pass

class AIPlayer(BasePlayer):
    '''
    AI player class
    '''
    def __init__(self, ptype='AI'):
        self.ptype = ptype

    def read_input(self):
        pass
