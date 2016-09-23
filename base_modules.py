# A decorator for the classes
#def in_history(f):
#    def new_f(*args, **kwargs):
#        args[0].msg_history.append(args[1])
#        f(*args, **kwargs)
#    return new_f

# Module classes
class BaseModule(object):
    '''
    Every module will have a history, types of msges they know
    and a list of attached modules. At the moment sending basically
    just calls the target modules receive function
    '''
    def __init__(self):
        self.msg_q = []
        self.att_modules = {}
        self.msg_types = {}
        self.msg_history = []
        self.name = "Base"

    def send(self, msg, tmodule):
        tmodule.msg_q.append(msg)

    def send_to_bus(self, msg):
        self.send(msg, self.att_modules["MainBus"])

    def attach_module(self, module):
        self.att_modules[module.name] = module

    def connect_module(self, module):
        self.att_modules[module.name] = module
        module.att_modules[self.name] = self

    def run(self):
        while len(self.msg_q) > 0:
            curr_msg = self.msg_q.pop(0)
            self.handle_msg(curr_msg)

class BaseMsg:
    '''
    A message class is only an object with a specific message type 
    and some attributes so that the target module knows what to do 
    with the module. All types are in all caps
    '''
    def __init__(self, content=None, mtype='BASE'):
        self.mtype = mtype
        self.content = content
