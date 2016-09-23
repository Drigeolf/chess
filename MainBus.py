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
            #print("#########")
            #print("Reading msg type %s"%msg.mtype)
            #print("Reading msg content")
            #print(msg.content)
            #print("Sending msg to: %s"%module)
            #print("#########")
            self.send(msg, self.att_modules[module])

    def get_module(self, module_name):
        return self.att_modules[module_name]
