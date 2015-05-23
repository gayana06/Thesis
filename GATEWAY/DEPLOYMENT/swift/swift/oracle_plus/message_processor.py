__author__ = 'Gayana'
from swift.oracle_plus.config import CURRENT_IP,MASTER_IP,SLAVE_IPS,LISTENING_PORT,IS_MASTER,ML_IP,ML_PORT
from swift.oracle_plus.communicator import Listener,Producer
from swift.oracle_plus.utility import log_sent_messages


class MessageProcessor():

    prefix_sending_topk="TOPK-"
    prefix_transition_done="TDONE-"
    prefix_do_transition="DOT-"
    prefix_do_final="FINAL-"

    def __init__(self):
        self.listener=None
        self.connect_slaves=[]
        self.connect_master=None

    def init(self):
        self.listener = Listener(CURRENT_IP, LISTENING_PORT)
        self.listener.start()
        if IS_MASTER:
            for ip in SLAVE_IPS:
                new_producer = Producer(ip, LISTENING_PORT)
                self.connect_slaves.append(new_producer)
        else:
            self.connect_master = Producer(MASTER_IP,LISTENING_PORT)

    def find_relavant_quorum(self,query):
        '''
        This will call the ML module and return the write quorum value
        '''
        connection=Producer(ML_IP, ML_PORT)
        return  connection.send_get_message(query)

    def send_topk_to_master(self,message):
        topk_message=self.prefix_sending_topk+message
        log_sent_messages(topk_message)
        self.connect_master.send_message(topk_message)

    def send_transition_complete_to_master(self,message):
        transition_done=self.prefix_transition_done+message
        log_sent_messages(transition_done)
        self.connect_master.send_message(transition_done)

    def ask_slaves_to_do_transition(self,message):
        do_transition=self.prefix_do_transition+message
        log_sent_messages(do_transition)
        for slave in self.connect_slaves:
            slave.send_message(do_transition)

    def ask_slaves_to_make_final_quorum(self,message):
        do_final=self.prefix_do_final+message
        log_sent_messages(do_final)
        for slave in self.connect_slaves:
            slave.send_message(do_final)

    def send_message(self,message):
        if IS_MASTER:
            for slave in self.connect_slaves:
                slave.send_message(message)
        else:
            self.connect_master.send_message(message)

messageProcessor=MessageProcessor()

def getMessageProcessor():
    return  messageProcessor