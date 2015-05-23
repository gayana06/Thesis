__author__ = 'mcouceiro'

from simple_server import Producer, Listener
import replicareconciliation
from swift.oracle_plus.config import is_adaptive_mode


QUORUM = 'qrm'
ACK = 'ack'
CONFIRM = 'conf'
DELIMITER = ','


class ProxyConsensusManager(object):
    def __init__(self):
        self._oracle = None
        self._listener = None
        self._master = None
        self._slaves = []
        self._received_acks = 0

    def init(self, oracle, ip, port, master_ip, slave_ips_glued, num_workers, my_id):
        self._oracle = oracle

        if not is_adaptive_mode:
            self._listener = Listener(ip, port + my_id)
            #with open("/home/ubuntu/transition_statistics.txt", "a") as tran_file:
            #            tran_file.write("Criei um listener com " + str(ip) + ":" + str(port + my_id)+ "\n")
            self._listener.start()
            if not self._oracle.is_master():
                self._master = Producer(master_ip, port)
                # with open("/home/ubuntu/transition_statistics.txt", "a") as tran_file:
                #     tran_file.write("Criei o producer master com " + str(master_ip) + ":" + str(port)+ "\n")
            else:
                slave_ips = slave_ips_glued.split(DELIMITER)
                for worker_id in range(num_workers):
                    for ip_temp in slave_ips:
                        new_producer = Producer(ip_temp, port + worker_id)
                        self._slaves.append(new_producer)
                        with open("/home/ubuntu/transition_statistics.txt", "a") as tran_file:
                            tran_file.write("Criei slaves com " + str(ip_temp) + ":" + str(port + worker_id) + "\n")
                ports_for_other_children = [(port + i) for i in range(num_workers) if not i == my_id]
                #gayana-start
                #f = open('/home/ubuntu/portcount','w')
                #f.write('ports_for_other_children ='+ str(ports_for_other_children) +"num_workers="+str(num_workers)+"Slave ips = "+slave_ips_glued)
                #f.close()
                #gayana-end
                for port_temp in ports_for_other_children:
                    new_producer = Producer(master_ip, port_temp)
                    self._slaves.append(new_producer)
                    #with open("/home/ubuntu/transition_statistics.txt", "a") as tran_file:
                    #    tran_file.write("Criei slaves com " + str(master_ip) + ":" + str(port_temp) + "\n")

    def process_message(self, message):
        split = message.split(DELIMITER)
        if split[0] == QUORUM:
            self._process_quorum(split[1], split[2])
        elif split[0] == ACK:
            self._process_ack()
        elif split[0] == CONFIRM:
            self._process_confirm()

    def send_quorum_message(self, read_quorum, write_quorum):
        with open("/home/ubuntu/multi-proxy.txt", "a") as tran_file:
            tran_file.write("Read Write Quorum =  " + str(read_quorum) + ":" + str(write_quorum) + "\n")
        self._process_quorum(read_quorum, write_quorum)
        for item in self._slaves:
            item.send_message(QUORUM+DELIMITER+str(read_quorum)+DELIMITER+str(write_quorum))

    def _process_quorum(self, read_quorum, write_quorum):
        #tran_file = open("/home/ubuntu/transition_statistics.txt", "a")
        #tran_file.write("recebi quorum" + "\n")
        #tran_file.close()
        self._oracle.set_transition_quorum(int(read_quorum), int(write_quorum))
        replicareconciliation.get_replica_reconciliation().check_pending_requests(self._oracle.trigger_reconciliation())
        if not self._oracle.is_master():
            self._master.send_message(ACK)

    def _process_ack(self):
        #tran_file = open("/home/ubuntu/transition_statistics.txt", "a")
        #tran_file.write("recebi ack" + "\n")
        #tran_file.close()
        self._received_acks += 1
        if len(self._slaves) == self._received_acks:
            self._received_acks = 0
            for item in self._slaves:
                #tran_file = open("/home/ubuntu/transition_statistics.txt", "a")
                #tran_file.write("enviei confirm para slave" + "\n")
                #tran_file.close()
                item.send_message(CONFIRM)
            self._process_confirm()

    def _process_confirm(self):
        #tran_file = open("/home/ubuntu/transition_statistics.txt", "a")
        #tran_file.write("recebi confirm" + "\n")
        #tran_file.close()
        self._oracle.set_final_quorum()

    #gayana-start
    def simulatequorum(self, read_quorum, write_quorum):
	with open("/home/ubuntu/transition_statistics.txt", "a") as tran_file:
                    tran_file.write("simulate  read= "+str(read_quorum)+" write = "+write_quorum+"\n")
        self._oracle.set_transition_quorum(int(read_quorum), int(write_quorum))
        self._oracle.set_final_quorum()
    #gayana-end

#pseudo-singleton
proxyconsensusmanager = ProxyConsensusManager()

def get_proxyconsensusmanager():
    return proxyconsensusmanager
