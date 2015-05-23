__author__ = 'Gayana'

from swift.oracle_plus.utility import log_processed_messages
import quorum_handler
from threading import Lock
from swift.oracle_plus.config import SLAVE_IPS
import sys
import traceback

class MessageManager():

    prefix_sending_topk="TOPK"
    prefix_transition_done="TDONE"
    prefix_do_transition="DOT"
    prefix_do_final="FINAL"
    delimiter="-"
    message_lock = Lock()
    topk_received_acks=0
    transition_complete_acks=0

    def process_message(self, message):
        try:
            with self.message_lock:
                split=message.split(self.delimiter)
                if split[0]==self.prefix_sending_topk:
                    self.process_topk_message(split[1])
                elif split[0]==self.prefix_do_transition:
                    self.process_do_transition(split[1])
                elif split[0]==self.prefix_transition_done:
                    self.process_done_transition(split[1])
                elif split[0]==self.prefix_do_final:
                    self.process_do_final(split[1])
                else:
                    log_processed_messages(str(message))
        except:
            exc_type, exc_value, exc_traceback = sys.exc_info()
            lines = traceback.format_exception(exc_type, exc_value, exc_traceback)
            error=''.join('!! ' + line for line in lines)
            log_processed_messages(error)

    def process_topk_message(self,message):
        log_processed_messages("Start topk = "+message)
        self.topk_received_acks+=1
        if message:
            topk_list=message.split("*")
            for item in topk_list:
                if item:
                    if "|" in item:
                        split=item.split("|")
                        quorum_handler.get_quorum_handler().add_to_gathered_topk_map(split[0],split[1])
            log_processed_messages("Done topk")
        if self.topk_received_acks == len(SLAVE_IPS):
            log_processed_messages("Topk received allacks")
            self.topk_received_acks=0
            quorum_handler.get_quorum_handler().enforce_transition_quorum()


    def process_do_transition(self,message):
        log_processed_messages("Start do tarnsition = "+message)
        if message:
            new_quorum_list=message.split("*")
            for item in new_quorum_list:
                if item:
                    if "|" in item:
                        split=item.split("|")
                        quorum_handler.get_quorum_handler().add_to_newquorum__map(split[0],split[1])
            quorum_handler.get_quorum_handler().applyTransitionQuorum()
        log_processed_messages("Done do transition")

    def process_done_transition(self,message):
        log_processed_messages("Start done transition = "+message)
        self.transition_complete_acks+=1
        if self.transition_complete_acks == len(SLAVE_IPS):
            self.transition_complete_acks=0
            log_processed_messages("Got all transition done acks")
            quorum_handler.get_quorum_handler().enforce_final_quorum()
        log_processed_messages("Done done transition")

    def process_do_final(self,message):
        log_processed_messages("Start do final = "+message)
        quorum_handler.get_quorum_handler().applyFinalQuorum()
        log_processed_messages("Done do final")

messageManager=MessageManager()

def getMessageManager():
    return messageManager