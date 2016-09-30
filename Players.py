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
        from msgs import ValidMove
        import random
        ref = self.board.att_modules["MainBus"].att_modules["Referee"]
        moves, move_strs = ref.gen_moves()
        rand_i = random.randint(0, len(moves)-1)
        rand_move = moves[rand_i]
        rand_str = self.board.move_to_str(rand_move)
        self.board.send_to_bus(ValidMove(content=rand_move, raw_text=rand_str))
