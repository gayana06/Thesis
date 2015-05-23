__author__ = 'mcouceiro'

from threading import Lock
import traceback
from datetime import datetime

print_stacktrace = False

class QuorumManager(object):

    def __init__(self):
        self._write_quorum_size = 2
        self._read_quorum_size = 2
        self._transition_write_quorum_size = None
        self._transition_read_quorum_size = None
        self._quorum_lock = Lock()
        #with open("/home/ubuntu/transition_statistics.txt", "a") as tran_file:
        #        tran_file.write("A: I'm " + str(id(self)) + "\n")

    @property
    def _write_quorum_size(self):
        return self.__write_quorum_size

    @_write_quorum_size.setter
    def _write_quorum_size(self, value):
        self.__write_quorum_size = value
        #if print_stacktrace:
            #stacktrace = traceback.format_stack()
            #with open("/home/ubuntu/transition_statistics.txt", "a") as tran_file:
            #    tran_file.write("write_quorum_size set to" + str(value) + " by:\n" + "".join(stacktrace))

    @property
    def _transition_write_quorum_size(self):
        return self.__transition_write_quorum_size

    @_transition_write_quorum_size.setter
    def _transition_write_quorum_size(self, value):
        self.__transition_write_quorum_size = value
        #if print_stacktrace:
        #    stacktrace = traceback.format_stack()
        #    with open("/home/ubuntu/transition_statistics.txt", "a") as tran_file:
        #        tran_file.write("transition_write_quorum_size set to" + str(value) + " by:\n" + "".join(stacktrace))

    def get_read_quorum_size(self):
        with self._quorum_lock:
            return self._read_quorum_size

    def get_write_quorum_size(self):
        with self._quorum_lock:
            return self._write_quorum_size

    def set_initial_quorum_sizes(self, write_quorum, read_quorum):
        with self._quorum_lock:
            #with open("/home/ubuntu/transition_statistics.txt", "a") as tran_file:
            #    tran_file.write("B: I'm " + str(id(self)) + "\n")
            self._write_quorum_size = write_quorum
            self._read_quorum_size = read_quorum
            #with open("/home/ubuntu/transition_statistics.txt", "a") as tran_file:
            #    tran_file.write("set quorum to: R:" + str(self._read_quorum_size) + " W:" + str(self._write_quorum_size) + "\n")

    def set_transition_quorum(self, new_read_quorum, new_write_quorum):
        with self._quorum_lock:
            #if (self._transition_read_quorum_size or self._transition_write_quorum_size) is not None:
            #    with open("/home/ubuntu/transition_statistics.txt", "a") as tran_file:
            #        tran_file.write("transition currently running, aborting...")
            #        return
            #with open("/home/ubuntu/transition_statistics.txt", "a") as tran_file:
            #    tran_file.write("old quorum: R:" + str(self._read_quorum_size) + " W:" + str(self._write_quorum_size) + "\n")

            if new_read_quorum > self._read_quorum_size:
                self._read_quorum_size = new_read_quorum
            if new_write_quorum > self._write_quorum_size:
                self._write_quorum_size = new_write_quorum
            self._transition_read_quorum_size = new_read_quorum
            self._transition_write_quorum_size = new_write_quorum

           # with open("/home/ubuntu/transition_statistics.txt", "a") as tran_file:
           #     tran_file.write("C: I'm " + str(id(self)) + "\n")
           #     tran_file.write("Novo quorum recebido: read" + str(self._transition_read_quorum_size) + " e write: " + str(self._transition_write_quorum_size) + "\n")
           #     tran_file.write("Mudei quorum transicao para: read" + str(self._read_quorum_size) + " e write: " + str(self._write_quorum_size) + "\n")

    def set_final_quorum(self):
        with self._quorum_lock:
            #with open("/home/ubuntu/transition_statistics.txt", "a") as tran_file:
            #    tran_file.write("D: I'm " + str(id(self)) + "\n")
            #    tran_file.write("transition: read: " + str(self._transition_read_quorum_size) + " e write: " + str(self._transition_write_quorum_size) + "\n")
            #with open("/home/ubuntu/transition_statistics.txt", "a") as tran_file:
            #    tran_file.write("old quorum: R:" + str(self._read_quorum_size) + " W:" + str(self._write_quorum_size) + "\n")

            self._read_quorum_size = self._transition_read_quorum_size
            self._write_quorum_size = self._transition_write_quorum_size
            with open("/home/ubuntu/quorum_map.txt", "a") as tran_file:
                tran_file.write("New Quorum RW = "+str(self._read_quorum_size)+"|"+str(self._write_quorum_size)+" at "+str(datetime.now())+"\n")
            #with open("/home/ubuntu/transition_statistics.txt", "a") as tran_file:
            #    tran_file.write("Mudei quorum FINAL para: read: " + str(self._read_quorum_size) + " e write: " + str(self._write_quorum_size) + "\n" +
            #                "o meu quorum antigo era read: " + str(self._transition_read_quorum_size) + " e write: " + str(self._transition_write_quorum_size) + "\n")
            self._transition_read_quorum_size = None
            self._transition_write_quorum_size = None

    def compute_read_quorum_size(self, write_quorum_size, number_of_replicas):
        return number_of_replicas - write_quorum_size + 1

    def trigger_reconciliation(self):
        with self._quorum_lock:
            return self._transition_write_quorum_size > self._write_quorum_size


quorum_manager = QuorumManager()
#with open("/home/ubuntu/transition_statistics.txt", "a") as tran_file:
#    tran_file.write("Initialized quorum manager\n")


def get_quorum_manager():
    return quorum_manager