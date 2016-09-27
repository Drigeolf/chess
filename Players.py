from base_modules import BasePlayer

class HumanPlayer(BasePlayer):
    '''
    Human player class
    '''
    def __init__(self, input_reader=None, ptype='HUMAN'):
        self.input_reader = input_reader
        self.ptype = ptype

    def read_input(self):
        pass

class AIPlayer(BasePlayer):
    '''
    AI player class
    '''
    def __init__(self, input_reader=None, ptype='HUMAN'):
        self.input_reader = input_reader
        self.ptype = ptype

    def read_input(self):
        pass
