from base_modules import BaseModule

class MainBus(BaseModule):
    '''
    The only function of this module is to pass the messages to 
    the attached modules
    '''
    def __init__(self):
        super(MainBus, self).__init__()
        self.name = "MainBus"

    #@in_history
    def handle_msg(self, msg):
        for module in self.att_modules.iterkeys():
            self.send(msg, self.att_modules[module])

    def run(self):
        while len(self.msg_q) > 0:
            curr_msg = self.msg_q.pop(0)
            self.handle_msg(curr_msg)
