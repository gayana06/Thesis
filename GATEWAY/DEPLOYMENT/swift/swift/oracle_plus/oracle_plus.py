__author__ = 'Gayana'

import threading
from swift.oracle_plus.utility import log_oracle_plus,Is_Adaptive_Mode
from swift.oracle_plus.statistic import get_statistics
from swift.oracle_plus.config import oracle_loop_time
from swift.oracle_plus.message_processor import getMessageProcessor
from swift.oracle_plus.quorum_handler import get_quorum_handler
from threading import Lock
from swift.oracle import oracle
import sys
import traceback

class Oracle_Plus(object):
    is_oracle_plus_running=False
    current_thread=None
    _is_init=False
    _is_init_lock=Lock()
    _is_master = False

    '''
    _is_init=False
    _is_master = False
    _is_init_lock=Lock()
    def set_attributes(self,use_adaptation,pid):
        with Oracle_Plus._is_init_lock:
            if not Oracle_Plus._is_init:
                Oracle_Plus._is_init = True
                self._use_adaptation = use_adaptation
                if pid == 0:
                    self._is_master = True
    '''

    def set_attributes(self,myid):
        with Oracle_Plus._is_init_lock:
            if not Oracle_Plus._is_init:
                Oracle_Plus._is_init = True
                getMessageProcessor().init()
                get_quorum_handler().start_send_back_thread()




    def run_oracle_plus(self):
        '''
        if not Oracle_Plus.is_oracle_plus_running  and self._is_master:
            Oracle_Plus.is_oracle_plus_running=True
            self.default_run()
            log_oracle_plus("I am inside")
        '''
        if not Oracle_Plus.is_oracle_plus_running and Is_Adaptive_Mode():
            Oracle_Plus.is_oracle_plus_running=True
            self.begin_run()
        elif not Oracle_Plus.is_oracle_plus_running and not Is_Adaptive_Mode() and (not oracle.get_oracle().run_adaptive() or not oracle.get_oracle().is_master()):
            Oracle_Plus.is_oracle_plus_running=True
            self.default_run()




    def begin_run(self):
        try:
            get_statistics().set_start_time()
            get_statistics().find_topk()
        except:
                exc_type, exc_value, exc_traceback = sys.exc_info()
                lines = traceback.format_exception(exc_type, exc_value, exc_traceback)
                error=''.join('!! ' + line for line in lines)
                log_oracle_plus(error)
        self.current_thread = threading.Timer(oracle_loop_time, self.begin_run)
        self.current_thread.setDaemon(True)
        self.current_thread.start()

    def default_run(self):
        try:
            get_statistics().set_start_time()
            get_statistics().log_performace()
        except:
            exc_type, exc_value, exc_traceback = sys.exc_info()
            lines = traceback.format_exception(exc_type, exc_value, exc_traceback)
            error=''.join('!! ' + line for line in lines)
            log_oracle_plus(error)
        self.current_thread = threading.Timer(oracle_loop_time, self.default_run)
        self.current_thread.setDaemon(True)
        self.current_thread.start()

oracle_plus = Oracle_Plus()

def get_oracle_plus():
    return oracle_plus