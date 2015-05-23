__author__ = 'mariac'

import threading
from swift import gettext_ as _
import ctypes
from proxyconsensus import get_proxyconsensusmanager
from replicareconciliation import get_replica_reconciliation
import time
import sys
from threading import Lock
import traceback
import quorum_manager
from simple_server import Producer
from swift.oracle_plus.statistic import get_statistics
from datetime import datetime

class See50Oracle(object):
    _lib_path = None
    _model_path = None
    _ML_lib = None

    def set_lib_path(self, path):
        self._lib_path = path

    def set_model_path(self, path):
        self._model_path = path

    def initiate_model(self, trees):
	#gayana-start
        f = open('/home/ubuntu/logger','w')
        f.write('init_model Lib path='+self._lib_path+" Model Path = "+self._model_path)
        #f.close()
        #gayana-end
	f.write('before lib load')
        self._ML_lib = cdll.LoadLibrary('/home/ubuntu/oracle_files/libsee5.so')
        #self._ML_lib = ctypes.CDLL(self._lib_path)
	#self._ML_lib = ctypes.CDLL('/home/ubuntu/oracle_files/libsee5.so')
	f.write('lib loaded')
        if trees:
            f.write('tree start')
            self._ML_lib.initiateSee5withTrees(self._model_path)
	    f.write('tree end')
        else:
	    f.write('other start')
            self._ML_lib.initiateSee5withRules(self._model_path)
            f.write('other end')
	f.close()

    def query_model(self, query):
        query_res = ctypes.c_char_p(self._ML_lib.getPrediction(query))
        return int(query_res.value)
    #gayana-start
    def query_model_via_socket(self, query):
        f = open('/home/ubuntu/oracle-socket','w')
        f.write('Before socket')
        sock=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        server_address=('172.31.0.175',50000)
        f.write('Before Connect to server')
        sock.connect(server_address)     
        f.write('After Connect to server')
	try:
	    #query='5,178,20,0.00572598840772,0.0262176970641,79,12,?'
	    f.write('Query = '+query)
	    sock.sendall(query)
	    data = sock.recv(100)
            newquorum=data.decode('UTF-8')
            f.write('New Quorum = '+newquorum)
            return newquorum
	finally:
	    sock.close()
            f.close()
   
    def sampleProducer(self,query):
        f = open('/home/ubuntu/oracle-socket','w')
        f.write('Before Produce\n')
        con=Producer('172.31.0.175', 50000)
        f.write('After Produce\n')
        #quorum=  con.send_get_message('5,178,20,0.00572598840772,0.0262176970641,79,12,?')
        quorum=  con.send_get_message(query)
	f.write('Sent Message = ' +query + '\nReceived : ' + quorum+'\n')
        f.close()
	return quorum
    #gayana-end


class MetricsGatherer(object):

    _numberOfGets = 0
    _numberOfPuts = 0

    _averageGetDuration = 0
    _averagePutDuration = 0

    _numberOfRepliedGets = 1
    _numberOfRepliedPuts = 1

    _numberOfRepliedGets_during_transition = 1
    _numberOfRepliedPuts_during_transition = 1

    _averageGetDuration_during_transition = 0
    _averagePutDuration_during_transition = 0

    _transition = False
    _transition_clock = 0
    _reconciliation_clock = 0

    def increase_gets(self):
        self._numberOfGets += 1

    def increase_puts(self):
        self._numberOfPuts += 1

    def add_get_duration(self, duration):
        self._averageGetDuration += duration
        self._numberOfRepliedGets += 1
        if self._transition:
            self._averageGetDuration_during_transition += duration
            self._numberOfRepliedGets_during_transition += 1

    def add_put_duration(self, duration):
        self._averagePutDuration += duration
        self._numberOfRepliedPuts += 1
        if self._transition:
            self._averagePutDuration_during_transition += duration
            self._numberOfRepliedPuts_during_transition += 1

    def get_gets(self):
        return self._numberOfGets

    def get_puts(self):
        return self._numberOfPuts

    def get_get_service_time(self):
        try:
            return self._averageGetDuration / self._numberOfRepliedGets
        except ZeroDivisionError:
            pass

    def get_put_service_time(self):
        try:
            return self._averagePutDuration / self._numberOfRepliedPuts
        except ZeroDivisionError:
            pass

    def get_replied_gets(self):
        return self._numberOfRepliedGets

    def get_replied_puts(self):
        return self._numberOfRepliedPuts

    def reset_statistics(self):
        self._numberOfGets = 0
        self._numberOfPuts = 0
        self._averageGetDuration = 0
        self._averagePutDuration = 0
        self._numberOfRepliedGets = 1
        self._numberOfRepliedPuts = 1

    def set_transition(self, state):
        if state:
            self._transition_clock = time.time()
        if not state:
            duration = time.time() - self._transition_clock
            string_to_write = _(str(duration) + "," + str(self._averageGetDuration / self._numberOfRepliedGets) + "," +
                                str(self._averagePutDuration / self._numberOfRepliedPuts) + "," +
                                str(self._reconciliation_clock))
            with open("/home/ubuntu/transition_statistics.txt", "a") as tran_file:
                tran_file.write(_(string_to_write + "\n"))
            self._averagePutDuration_during_transition = 0
            self._numberOfRepliedPuts_during_transition = 1
            self._averageGetDuration_during_transition = 0
            self._numberOfRepliedGets_during_transition = 1
            self._reconciliation_clock = 0
        self._transition = state

    def set_reconciliation_clock_init(self):
        self._reconciliation_clock = time.time()

    def set_reconciliation_clock_end(self):
        self._reconciliation_clock = time.time() - self._reconciliation_clock


class Oracle(object):

    _is_init = False
    _is_init_lock = Lock()

    _oracleThread = None
    _running = False

    _average_window_size = 10  # in seconds
    _number_of_replicas = 4

    _use_adaptation = True

    _oracle_output_file_name = "/home/ubuntu/oracle.txt"
    _file = None

    _coiso = 0
    is_first_run=True
    _is_master = False

    def set_attributes(self, number_of_replicas, average_window_size, use_adaptation, write_quorum, read_quorum,
                       oracle_log_file, oracle_lib_path, oracle_model_path, ip, port, master_ip, slave_ips_glued,
                       timeout, my_id, num_workers):
        with Oracle._is_init_lock:
            if not Oracle._is_init:
                Oracle._is_init = True
                self._average_window_size = average_window_size
                self._number_of_replicas = number_of_replicas
                self._use_adaptation = use_adaptation
                self._oracle_output_file_name = oracle_log_file
                if ip == master_ip and my_id == 0:
                    self._is_master = True

                quorum_manager.get_quorum_manager().set_initial_quorum_sizes(write_quorum, read_quorum)
                get_ML_oracle().set_lib_path(oracle_lib_path)
                get_ML_oracle().set_model_path(oracle_model_path)
                get_proxyconsensusmanager().init(self, ip, port, master_ip, slave_ips_glued, num_workers, my_id)
                get_replica_reconciliation().init(number_of_replicas, timeout)

                with open("/home/ubuntu/transition_statistics.txt", "a") as tran_file:
                    tran_file.write(_("----------------------------------------------" + str(my_id) + " IP = " + ip+ " is master = " +str(self._is_master) +"\n"))

    def evaluate(self, query):
	return get_ML_oracle().sampleProducer(query)
        #return get_ML_oracle().query_model(query)
        #return get_ML_oracle().query_model_via_socket(query)

    def run_oracle(self):
	#gayana-start
        #f = open('/home/ubuntu/logger','w')
        #f.write('run oracle before if')
        #f.close()
        #gayana-end
        if not Oracle._running and self._use_adaptation and self._is_master:
	    #f.write('run oracle inside if')
	    #get_ML_oracle().initiate_model(True)
	    #f.write('run oracle afetr ML')
	    #new_write_quorum_size = self.evaluate('?')
            #with open("/home/ubuntu/transition_statistics.txt", "a") as tran_file:
            #        tran_file.write("Oracle Started\n")
            Oracle._running = True
            self._run()

    def _run(self):
        try:
            get_statistics().set_start_time()

            #with open("/home/ubuntu/transition_statistics.txt", "a") as tran_file:
            #            tran_file.write("Inside oracle run\n")
            query = _(str(quorum_manager.get_quorum_manager().get_write_quorum_size()) + ','
                      + str(get_metrics_gatherer().get_gets())
                      + "," + str(get_metrics_gatherer().get_puts()) + "," +
                      str(get_metrics_gatherer().get_get_service_time()) + "," +
                      str(get_metrics_gatherer().get_put_service_time()) + "," +
                      str(get_metrics_gatherer().get_replied_gets()) + "," +
                      str(get_metrics_gatherer().get_replied_puts()))
            #with open("/home/ubuntu/transition_statistics.txt", "a") as tran_file:
            #            tran_file.write("Query = " + query +"\n")
            get_metrics_gatherer().reset_statistics()
            #with open("/home/ubuntu/transition_statistics.txt", "a") as tran_file:
            #            tran_file.write("after gather stats output file = "+ self._oracle_output_file_name  + " \n")
        #self._file = open(self._oracle_output_file_name, "w")
            #self._file.write(_(query + "\n"))
            #self._file.close()
            #with open(self._oracle_output_file_name, "a") as tran_file:
            #            tran_file.write(_(query + "\n"))
            new_write_quorum_size = self.evaluate(_(query + ",?"))

            if not self.is_first_run and (new_write_quorum_size != quorum_manager.get_quorum_manager().get_write_quorum_size() and self._coiso >=0):
                #with open("/home/ubuntu/transition_statistics.txt", "a") as tran_file:
                #    tran_file.write("+ change from: " + str(quorum_manager.get_quorum_manager().get_write_quorum_size())
                #                    + " to " + str(new_write_quorum_size) + "\n")
                #with open("/home/ubuntu/quorum_map.txt", "a") as tran_file:
                #    tran_file.write("+ change from: " + str(quorum_manager.get_quorum_manager().get_write_quorum_size())
                #                    + " to " + str(new_write_quorum_size) + "at "+str(datetime.now())+"\n")
                with open("/home/ubuntu/quorum_map.txt", "a") as tran_file:
                    tran_file.write("Query = "+str(query)+" Reply = "+str(new_write_quorum_size)+"\n")
                    tran_file.write("Changed from = "+str(quorum_manager.get_quorum_manager().get_write_quorum_size())+" To = "+str(new_write_quorum_size)+" at "+str(datetime.now())+"\n")
                get_proxyconsensusmanager().send_quorum_message(
                    quorum_manager.get_quorum_manager().compute_read_quorum_size(int(new_write_quorum_size), self._number_of_replicas),
                    new_write_quorum_size)
                #newreadQ=quorum_manager.get_quorum_manager().compute_read_quorum_size(new_write_quorum_size, self._number_of_replicas)
            #    newreadQ=int(self._number_of_replicas)-int(new_write_quorum_size)+1
            #with open("/home/ubuntu/transition_statistics.txt", "a") as tran_file:
                #    tran_file.write("New read q = "+str(newreadQ)+" New write q = "+str(new_write_quorum_size)+"\n")
            #self.set_transition_quorum(int(newreadQ), int(new_write_quorum_size))
               # self.set_final_quorum()
                self._coiso = 0
            else:
                self._coiso += 1
                self.is_first_run=False

            # if self._coiso > 3:
            #     if new_write_quorum_size > QuorumManager.get_write_quorum_size():
            #         QuorumManager.increase_write_quorum_size(new_write_quorum_size, self._number_of_replicas)
            #     elif new_write_quorum_size < QuorumManager.get_write_quorum_size():
            #         QuorumManager.decrease_write_quorum_size(new_write_quorum_size, self._number_of_replicas)
            #     self._coiso = 0
            # else:
            #     self._coiso += 1
            get_statistics().log_performace()
        except:
            exc_type, exc_value, exc_traceback = sys.exc_info()
            lines = traceback.format_exception(exc_type, exc_value, exc_traceback)
            error=''.join('!! ' + line for line in lines)
            with open("/home/ubuntu/multi-proxy.txt", "a") as tran_file:
                tran_file.write("Error = "+str(error)+"\n")

        self._oracleThread = threading.Timer(self._average_window_size, self._run)
        self._oracleThread.setDaemon(True)
        self._oracleThread.start()

    def run_adaptive(self):
        return self._use_adaptation

    def set_transition_quorum(self, new_read_quorum, new_write_quorum):
        #with open("/home/ubuntu/transition_statistics.txt", "a") as tran_file:
        #        tran_file.write("Before transition quorum\n")
        get_metrics_gatherer().set_transition(True)
	#with open("/home/ubuntu/transition_statistics.txt", "a") as tran_file:
        #        tran_file.write("After transition quorum\n")
        quorum_manager.get_quorum_manager().set_transition_quorum(new_read_quorum, new_write_quorum)

    def set_final_quorum(self):
        quorum_manager.get_quorum_manager().set_final_quorum()
        get_metrics_gatherer().set_transition(False)

    def trigger_reconciliation(self):
        return quorum_manager.get_quorum_manager().trigger_reconciliation()

    def is_master(self):
        return self._is_master


def my_quorum_size(req_type):
    """
    Number of successful backend requests needed for the proxy to consider
    the client request successful based on the size of the quorums defined by the Oracle
    """
    if req_type == 'GET':
        return quorum_manager.get_quorum_manager().get_read_quorum_size()
    else:
        return quorum_manager.get_quorum_manager().get_write_quorum_size()

#print_stacktrace = False
#Pseudo-singleton
oracle = Oracle()
#if print_stacktrace:
#    stacktrace = traceback.format_stack()
#    with open("/home/ubuntu/transition_statistics.txt", "a") as tran_file:
#        tran_file.write("Oracle initialized by\n" + "".join(stacktrace))

metricsGatherer = MetricsGatherer()
ML_oracle = See50Oracle()


def get_oracle():
    return oracle


def get_metrics_gatherer():
    return metricsGatherer


def get_ML_oracle():
    return ML_oracle

