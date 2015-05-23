__author__ = 'Gayana'

from swift.oracle_plus.config import DEFAULT_READ_QUORUM,DEFAULT_WRITE_QUORUM,REPLICA_COUNT,IS_MASTER,IS_STATIC_POLICY_ENABLED,SIZE,COLLECT_BEST,All_BEST,oracle_loop_time
from threading import Lock
from swift.oracle_plus.utility import log_oracle_plus,log_quorum_map,log_processed_messages,log_query
from  swift.oracle_plus.pending_request_monitor import get_pending_req_monitor
from  swift.oracle_plus.message_processor import getMessageProcessor
from  swift.oracle_plus.swift_requester import get_swift_requester
from swift.common.utilnew import GreenAsyncPile
import time
import sys
import traceback
import threading
'''
Here onwards always quorum means write quorum.
Read quorum = replica count - write quorum + 1
map={obj:[write,read]}
'''
class Quorum_handler(object):
    quorum_map={}
    ultimate_quorum_map={}
    already_exist_adjusted_map={}
    sent_topk_map={}
    gathered_topk_map={}
    put_request_obj_map={}
    newQuorumMap={}
    quorum_lock = Lock()
    newquorum_string=''
    is_optimize_tail=False
    tail_write_quorum=DEFAULT_WRITE_QUORUM
    tail_read_quorum=DEFAULT_READ_QUORUM

    #def init(self):
    #    self.start_send_back_thread()


    def Is_Optimize_Tail(self):
        return self.is_optimize_tail

    def set_tail_optimization_status(self,doOptimize):
        self.is_optimize_tail=doOptimize
        if not doOptimize:
            self.tail_write_quorum=DEFAULT_WRITE_QUORUM
            self.tail_read_quorum=DEFAULT_READ_QUORUM

    def is_key_in_map(self,path):
        if path in self.quorum_map:
            return True
        else:
            return False

    def clear_quorum_map(self):
        self.quorum_map={}
        self.reset_data()

    def get_quorum_of(self,obj):
        with self.quorum_lock:
            if obj in self.quorum_map:
                writeq = self.quorum_map[obj][0]
                readq = self.quorum_map[obj][1]
            else:
                sections=obj.split("/")
                list=sections[len(sections)-1].split("_")
                log_oracle_plus(str(list))
                if All_BEST and len(list)==3:
                    #if "w1_tiny_0000" in obj or "w3_tiny_0000" in obj or "w5_tiny_0000" in obj or "w7_tiny_0000" in obj or "w9_tiny_0000" in obj or "w11_tiny_0000" in obj or "w13_tiny_0000" in obj or "w15_tiny_0000" in obj or "w17_tiny_0000" in obj or "w19_tiny_0000" in obj:
                    #if "w1_tiny" in obj or "w3_tiny" in obj or "w5_tiny" in obj or "w7_tiny" in obj or "w9_tiny" in obj or "w11_tiny" in obj or "w13_tiny" in obj or "w15_tiny" in obj or "w17_tiny" in obj or "w19_tiny" in obj:
                    key = int(list[2])
                    if (list[0]=="w1" or  list[0]=="w3" or list[0]=="w5" or list[0]=="w7" or list[0]=="w9" or list[0]=="w11") and key<=200:
                        writeq=5
                        readq=1
                    elif "w1_tiny" in obj or "w3_tiny" in obj or "w5_tiny" in obj or "w7_tiny" in obj or "w9_tiny" in obj or "w11_tiny" in obj or "w13_tiny" in obj or "w15_tiny" in obj or "w17_tiny" in obj or "w19_tiny" in obj:
                        if self.is_optimize_tail:
                            writeq = self.tail_write_quorum
                            readq = self.tail_read_quorum
                        else:
                            writeq = DEFAULT_WRITE_QUORUM
                            readq = DEFAULT_READ_QUORUM
                    #elif "w2_tiny_0000" in obj or "w4_tiny_0000" in obj or "w6_tiny_0000" in obj or "w8_tiny_0000" in obj or "w10_tiny_0000" in obj or "w12_tiny_0000" in obj or "w14_tiny_0000" in obj or "w16_tiny_0000" in obj or "w18_tiny_0000" in obj or "w20_tiny_0000" in obj:
                    #elif "w2_tiny" in obj or "w4_tiny" in obj or "w6_tiny" in obj or "w8_tiny" in obj or "w10_tiny" in obj or "w12_tiny" in obj or "w14_tiny" in obj or "w16_tiny" in obj or "w18_tiny" in obj or "w20_tiny" in obj:
                    elif (list[0]=="w2" or  list[0]=="w4" or list[0]=="w6" or list[0]=="w8" or list[0]=="w10" or list[0]=="w12") and key<=200:
                        writeq=1
                        readq=5
                    else:
                        if self.is_optimize_tail:
                            writeq = self.tail_write_quorum
                            readq = self.tail_read_quorum
                        else:
                            writeq = DEFAULT_WRITE_QUORUM
                            readq = DEFAULT_READ_QUORUM

                else:
                    if self.is_optimize_tail:
                        writeq = self.tail_write_quorum
                        readq = self.tail_read_quorum
                    else:
                        writeq = DEFAULT_WRITE_QUORUM
                        readq = DEFAULT_READ_QUORUM
            #log_oracle_plus("Req-Path = "+str(obj) +" Read-Q = "+str(readq) +" Write-Q = "+str(writeq))
            return readq,writeq
    resend_map={}
    resend_lock=Lock()


    def check_tail_read(self,obj,content):
        if self.is_optimize_tail and obj not in self.quorum_map:
            previous_wq=int(content.split("|")[1])
            if previous_wq < self.tail_write_quorum:
                newcontent=content.split("|")[0]+"|"+str(self.tail_write_quorum)
                log_oracle_plus("Rewritten obj : "+str(obj))
                self.resend_map[obj]=newcontent
                #pile = GreenAsyncPile(1)
                #pile.spawn(get_swift_requester().resend_write, obj,newcontent)
                #get_swift_requester().resend_write(obj,newcontent)
            else:
                log_oracle_plus("No Problem : "+str(obj))

    def start_send_back_thread(self):
        log_query("Start ")
        try:
            self.send_back()
        except:
                exc_type, exc_value, exc_traceback = sys.exc_info()
                lines = traceback.format_exception(exc_type, exc_value, exc_traceback)
                error=''.join('!! ' + line for line in lines)
                log_oracle_plus(error)
        self.current_thread = threading.Timer(5, self.start_send_back_thread)
        self.current_thread.setDaemon(True)
        self.current_thread.start()


    def send_back(self):
        count=len(self.resend_map)
        if count>0:
            for i in range(0,count):
                key, value = self.resend_map.popitem()
                log_query("Sent "+str(key))
                get_swift_requester().resend_write(key,value)



    def update_quorum_map(self,operation,read_map,write_map):
        '''
        This will collect all the relevant data to query the ML module and call  find_relavant_quorum()
        get the quorum values and update the map
        Furthermore based on the operation passed it will (add, update) or delete records from the map

        '''
        with self.quorum_lock:
            if operation == "UPDATE":
                if len(read_map)>0:
                    for k,v in read_map.items():
                        if k in write_map.keys() and write_map[k] > v:
                            self.quorum_map[k]=[1,5]
                        else:
                            self.quorum_map[k]=[5,1]
                if len(write_map)>0:
                    for k,v in write_map.items():
                        if k not in read_map.keys():
                            self.quorum_map[k]=[1,5]

        log_quorum_map(str(self.quorum_map))
        log_oracle_plus("-------------------------------------------------------------------")


    def update_quorum_map_with_ML(self,operation,read_map,write_map,get_count_map,put_count_map,avg_get_time_map,avg_put_time_map,replied_get_count_map,replied_put_count_map,put_request_obj_map,performace):
        #self.reset_data()
        self.put_request_obj_map=put_request_obj_map.copy()
        temp_list=[]
        if operation == "UPDATE":
            if len(read_map)>0:
                for k,v in read_map.items():
                    temp_list.append(k)
            if len(write_map)>0:
                for k,v in write_map.items():
                    if k not in read_map.keys():
                        temp_list.append(k)
            sent_top_string=''
            for item in temp_list:
                query=self.generate_query(item,get_count_map,put_count_map,avg_get_time_map,avg_put_time_map,replied_get_count_map,replied_put_count_map,performace)
                self.sent_topk_map[item]=query;
                if IS_MASTER:
                    self.add_to_gathered_topk_map(item,query)
                sent_top_string+=item+"|"+query+"*"

            #send to master if I am a slave or add it to gathered_topk_map otherwise
            if IS_MASTER:
                log_processed_messages("Masters topk ="+str(self.sent_topk_map))
            else:
                getMessageProcessor().send_topk_to_master(sent_top_string)

    def update_tail_quorum_with_ML(self,received_puts,received_gets,get_avg_latency,put_avg_latency,replied_gets,replied_puts):
        sent_top_string=''
        log_oracle_plus("Tail update_tail_quorum_with_ML Start")
        log_oracle_plus("received_puts="+str(received_puts)+",received_gets="+str(received_gets)+",get_avg_latency"+str(get_avg_latency)+",put_avg_latency"+str(put_avg_latency)+",replied_gets"+str(replied_gets)+",replied_puts"+str(replied_puts))
        if IS_MASTER:
            log_processed_messages("Master Tail")
            query=self.generate_tail_query(received_puts,received_gets,get_avg_latency,put_avg_latency,replied_gets,replied_puts)
            item="TAIL"
            self.sent_topk_map[item]=query;
            self.add_to_gathered_topk_map(item,query)
        else:
            getMessageProcessor().send_topk_to_master(sent_top_string)
        log_oracle_plus("Tail update_tail_quorum_with_ML Done")

    def add_to_gathered_topk_map(self,key,value):
        with self.quorum_lock:
            self.gathered_topk_map[key]=value

    def add_to_newquorum__map(self,key,value):
        self.newQuorumMap[key]=[int(value),REPLICA_COUNT-int(value)+1]

    def query_ML(self):
        if len(self.gathered_topk_map.keys()) > 0:
            log_oracle_plus("Gathered Keys at ML = "+str(self.gathered_topk_map))
            for item in self.gathered_topk_map.keys():
                new_writeq= getMessageProcessor().find_relavant_quorum(self.gathered_topk_map[item])
                log_query(str(item)+" = "+str(self.gathered_topk_map[item])+" = "+str(new_writeq))
                self.newQuorumMap[item]=[int(new_writeq),REPLICA_COUNT-int(new_writeq)+1]
                self.newquorum_string+=item+"|"+new_writeq+"*"

    def Static_Policies(self):
        if len(self.gathered_topk_map.keys()) > 0:
            log_oracle_plus("Gathered Keys at static policies = "+str(self.gathered_topk_map))
            for item in self.gathered_topk_map.keys():
                if "w1_tiny" in item or "w3_tiny" in item or "w5_tiny" in item or "w7_tiny" in item or "w9_tiny" in item or "w11_tiny" in item or "w13_tiny" in item or "w15_tiny" in item or "w17_tiny" in item or "w19_tiny" in item:
                    new_writeq=5
                else:
                    new_writeq=1
                log_oracle_plus(str(new_writeq))
                self.newQuorumMap[item]=[int(new_writeq),REPLICA_COUNT-int(new_writeq)+1]
                self.newquorum_string+=item+"|"+str(new_writeq)+"*"

    def enforce_transition_quorum(self):
        if IS_STATIC_POLICY_ENABLED:
            self.Static_Policies()
        else:
            self.query_ML()
        getMessageProcessor().ask_slaves_to_do_transition(self.newquorum_string)
        self.applyTransitionQuorum()

    def enforce_final_quorum(self):
        getMessageProcessor().ask_slaves_to_make_final_quorum("final")
        self.applyFinalQuorum()

    def applyTransitionQuorum(self):
        if len(self.newQuorumMap.keys()) > 0:
            for item in self.newQuorumMap.keys():
                if self.is_optimize_tail:
                    log_oracle_plus("Tail applyTransition Start")
                    current_read=self.tail_read_quorum
                    current_write=self.tail_write_quorum
                    self.sent_topk_map[item]=[current_write,current_read]
                    newquorum=self.newQuorumMap[item]
                    new_read=newquorum[1]
                    new_write=newquorum[0]
                    if new_read > current_read:
                        transition_read=new_read
                        transition_write=current_write
                        self.ultimate_quorum_map[item]=[new_write,new_read]
                    elif new_write > current_write:
                        transition_read=current_read
                        transition_write=new_write
                        self.ultimate_quorum_map[item]=[new_write,new_read]
                    else:
                        transition_read=current_read
                        transition_write=current_write
                        self.already_exist_adjusted_map[item]=[transition_write,transition_read]
                    with self.quorum_lock:
                        self.tail_write_quorum=transition_write
                        self.tail_read_quorum=transition_read
                    log_oracle_plus("Tail applyTransition Done")
                elif item in self.sent_topk_map.keys():
                    current_read,current_write= self.get_quorum_of(item)
                    self.sent_topk_map[item]=[current_write,current_read]
                    newquorum=self.newQuorumMap[item]
                    new_read=newquorum[1]
                    new_write=newquorum[0]
                    if new_read > current_read:
                        transition_read=new_read
                        transition_write=current_write
                        self.ultimate_quorum_map[item]=[new_write,new_read]
                    elif new_write > current_write:
                        transition_read=current_read
                        transition_write=new_write
                        self.ultimate_quorum_map[item]=[new_write,new_read]
                    else:
                        transition_read=current_read
                        transition_write=current_write
                        self.already_exist_adjusted_map[item]=[transition_write,transition_read]
                    with self.quorum_lock:
                        self.quorum_map[item]=[transition_write,transition_read]

            if len(self.ultimate_quorum_map.keys()) > 0:
                #pile = GreenAsyncPile(len(self.ultimate_quorum_map))
                for key in self.ultimate_quorum_map.keys():
                    if self.ultimate_quorum_map[key][0] > self.sent_topk_map[key][0]:
                        #send the request back with new write quorum
                        log_oracle_plus("Sent write with new quorum to key = "+key)
                        if key in self.put_request_obj_map:
                            #pile.spawn(get_swift_requester().print_request_details, key,self.put_request_obj_map[key])
                            get_swift_requester().print_request_details(key,self.put_request_obj_map[key])
                #for response in pile:
                #    log_oracle_plus("Came response = "+str(response))



        #tell master that writing is done if I am slave. Increment ack otherwise
        if IS_MASTER:
            pass
        else:
            getMessageProcessor().send_transition_complete_to_master("done")

    def applyFinalQuorum(self):
        if len(self.newQuorumMap.keys()) > 0:
            for key in self.newQuorumMap.keys():
                log_oracle_plus("Updating Key="+str(key)+" Values = "+str(self.newQuorumMap[key]))
                if self.is_optimize_tail:
                    log_oracle_plus("Tail applyFinalQuorum Start")
                    with self.quorum_lock:
                        self.tail_write_quorum=self.newQuorumMap[key][0]
                        self.tail_read_quorum=self.newQuorumMap[key][1]
                    log_oracle_plus("Tail applyFinalQuorum Done")
                else:
                    with self.quorum_lock:
                        self.quorum_map[key]=[self.newQuorumMap[key][0],self.newQuorumMap[key][1]]

        self.reset_data()

        log_quorum_map(str(self.quorum_map))
        log_oracle_plus("-------------------------------------------------------------------")
        '''
        for key in self.quorum_map.keys():
            if key not in ultimate_quorum_map.keys() and key not in already_exist_adjusted_map.keys():
                with self.quorum_lock:
                    self.quorum_map[key]=[DEFAULT_WRITE_QUORUM,DEFAULT_READ_QUORUM]
        '''

    def reset_data(self):
        self.ultimate_quorum_map={}
        self.already_exist_adjusted_map={}
        self.sent_topk_map={}
        self.gathered_topk_map={}
        self.newQuorumMap={}
        self.put_request_obj_map
        self.newquorum_string=''

    def generate_tail_query(self,received_puts,received_gets,get_avg_latency,put_avg_latency,replied_gets,replied_puts):
        #Id
        query="1,"
        #WriteQ
        query+=str(DEFAULT_WRITE_QUORUM)+","

        #PercW=received_puts/(received_gets+received_puts)
        if received_puts >0:
            puts=received_puts
            gets=received_gets
            query+=str((puts/float((puts+gets)))*100)+","
        else:
            query+="0,"
        #received_gets
        query+=str(received_gets)+","
        gets=received_gets

        #received_puts
        query+=str(received_puts)+","
        puts=received_puts

        #received
        #query+=str(gets+puts)+","

        #get_avg_latency
        avgget=get_avg_latency
        query+=str(get_avg_latency)+","

        #put_avg_latency
        query+=str(put_avg_latency)+","
        avgput=put_avg_latency

        #replied_gets
        rgets=replied_gets
        query+=str(replied_gets)+","

        #replied_puts
        rputs=replied_puts
        query+=str(replied_puts)+","

        #diff received /( replied_gets + replied_puts).
        #if rputs>0 or rgets>0:
        #    query+=str((gets+puts)/float((rgets+rputs)))+","
        #else:
        #    query+="0,"

        #size
        query+=str(SIZE)+","

        #diff2 := get_avg_latency/put_avg_latency
        #if avgput>0:
        #    query+=str((avgget/float(avgput)))+","
        #else:
        #    query+="0,"

        #read
        query+="1,"
        #write
        query+="1,"
        #total
        query+=str((rgets+rputs)/float(oracle_loop_time))+","
        query+= "?"

        #log_query(str(item)+","+query)
        return query


    def generate_query(self,item,get_count_map,put_count_map,avg_get_time_map,avg_put_time_map,replied_get_count_map,replied_put_count_map,performace):
        if item in self.quorum_map.keys():
            current_quorum = self.quorum_map[item][0]
        else:
            current_quorum=DEFAULT_WRITE_QUORUM

        #Id
        query="1,"
        #WriteQ
        query+=str(current_quorum)+","

        #PercW=received_puts/(received_gets+received_puts)
        if item in put_count_map.keys() and put_count_map[item] >0:
            puts=put_count_map[item]
            if item in get_count_map.keys():
                gets=get_count_map[item]
            else:
                gets=0
            query+=str((puts/float((puts+gets)))*100)+","
        else:
            query+="0,"
        #received_gets
        if item in get_count_map.keys():
            query+=str(get_count_map[item])+","
            gets=get_count_map[item]
        else:
            query+="0,"
            gets=0
        #received_puts
        if item in put_count_map.keys():
            query+=str(put_count_map[item])+","
            puts=put_count_map[item]
        else:
            query+="0,"
            puts=0
        #received
        #query+=str(gets+puts)+","

        #get_avg_latency
        if item in avg_get_time_map.keys():
            avgget=avg_get_time_map[item]
            query+=str(avg_get_time_map[item])+","
        else:
            query+="0,"
            avgget=0
        #put_avg_latency
        if item in avg_put_time_map.keys():
            query+=str(avg_put_time_map[item])+","
            avgput=avg_put_time_map[item]
        else:
            query+="0,"
            avgput=0
        #replied_gets
        if item in replied_get_count_map.keys():
            rgets=replied_get_count_map[item]
            query+=str(replied_get_count_map[item])+","
        else:
            query+="0,"
            rgets=0
        #replied_puts
        if item in replied_put_count_map.keys():
            rputs=replied_put_count_map[item]
            query+=str(replied_put_count_map[item])+","
        else:
            query+="0,"
            rputs=0

        #diff received /( replied_gets + replied_puts).
        #if rputs>0 or rgets>0:
        #    query+=str((gets+puts)/float((rgets+rputs)))+","
        #else:
        #    query+="0,"

        #size
        query+=str(SIZE)+","

        #diff2 := get_avg_latency/put_avg_latency
        #if avgput>0:
        #    query+=str((avgget/float(avgput)))+","
        #else:
        #    query+="0,"

        #read
        query+="1,"
        #write
        query+="1,"
        #total
        query+=str((rgets+rputs)/float(oracle_loop_time))+","

        if COLLECT_BEST:
            if "w1_tiny" in item or "w3_tiny" in item or "w5_tiny" in item or "w7_tiny" in item or "w9_tiny" in item or "w11_tiny" in item or "w13_tiny" in item or "w15_tiny" in item or "w17_tiny" in item or "w19_tiny" in item:
                query+="5"
            else:
                query+="1"
        else:
            query+= "?"

        #log_query(str(item)+","+query)
        return query



    def generate_query_old(self,item,get_count_map,put_count_map,avg_get_time_map,avg_put_time_map,replied_get_count_map,replied_put_count_map):
        if item in self.quorum_map.keys():
            current_quorum = self.quorum_map[item][0]
        else:
            current_quorum=DEFAULT_WRITE_QUORUM

        query=str(current_quorum)+","

        if item in get_count_map.keys():
            query+=str(get_count_map[item])+","
        else:
            query+="0,"

        if item in put_count_map.keys():
            query+=str(put_count_map[item])+","
        else:
            query+="0,"

        if item in avg_get_time_map.keys():
            query+=str(avg_get_time_map[item])+","
        else:
            query+="0,"

        if item in avg_put_time_map.keys():
            query+=str(avg_put_time_map[item])+","
        else:
            query+="0,"

        if item in replied_get_count_map.keys():
            query+=str(replied_get_count_map[item])+","
        else:
            query+="0,"

        if item in replied_put_count_map.keys():
            query+=str(replied_put_count_map[item])+","
        else:
            query+="0,"

        query+= "?"
        return query






quorum_handler = Quorum_handler()


def get_quorum_handler():
    return quorum_handler

def get_quorum(obj_path):
    return get_quorum_handler().get_quorum_of(obj_path)