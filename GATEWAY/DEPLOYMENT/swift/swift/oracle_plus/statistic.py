__author__ = 'Gayana'

'''
read_object_path_list sample = ["/v1/AUTH_test1/wa_000016/tiny_2","/v1/AUTH_test1/wa_000016/tiny_3","/v1/AUTH_test1/wa_000016/tiny_5"]
write_object_path_list sample = ["/v1/AUTH_test1/wa_000016/tiny_10","/v1/AUTH_test1/wa_000016/tiny_6","/v1/AUTH_test1/wa_000016/tiny_7"]

input to the topk socket = /v1/AUTH_test1/wa_000016/tiny_2|/v1/AUTH_test1/wa_000016/tiny_3|/v1/AUTH_test1/wa_000016/tiny_5
output from topksocket = /v1/AUTH_test1/wa_000016/tiny_2|2|1,/v1/AUTH_test1/wa_000016/tiny_5|3|1

'''


from swift.oracle_plus.utility import log_oracle_plus,log_performace
from swift.oracle_plus.communicator import Producer
from swift.oracle_plus.config import DEFAULT_WRITE_QUORUM,IS_ML_TRAINING,SEP_COMMA,SEP_PIPE,topk_ip,topk_port,HTTP_GET,HTTP_PUT,TOPK_ERROR_THRESHOLD_PERCENTAGE,is_adaptive_mode,IS_ML_ENABLED,IS_TEST_COMMUNICATION,IS_MASTER,CURRENT_IP
from swift.oracle_plus.quorum_handler import get_quorum_handler
from swift.oracle_plus.message_processor import getMessageProcessor
from datetime import datetime
from threading import Lock
import time

class Statistics(object):

    read_object_path_list=[]
    write_object_path_list=[]
    write_topk_map={}
    read_topk_map={}
    get_request_count_map={}
    put_request_count_map={}
    total_get_request_duration_map={}
    total_put_request_duration_map={}
    avg_get_request_duration_map={}
    avg_put_request_duration_map={}
    replied_get_count_map={}
    replied_put_count_map={}
    object_lock=Lock()

    put_request_object_map={}

    write_old_topk_map={}
    read_old_topk_map={}

    '''
    These variables are to find the system throughput in every epoch to see how system perform
    '''
    system_get_count=0
    system_put_count=0
    system_put_duration=0
    system_get_duration=0
    system_replied_get_count=0
    system_replied_put_count=0
    start_time=time.time()
    has_set_time=False
    is_test=True
    system_lock=Lock()

    tail_system_get_count=0
    tail_system_put_count=0
    tail_system_get_duration=0
    tail_system_put_duration=0
    tail_system_replied_get_count=0
    tail_system_replied_put_count=0
    has_tail_started=False


    def add_request_object_to_map(self,req):
        if is_adaptive_mode and not get_quorum_handler().Is_Optimize_Tail():
            self.put_request_object_map[str(req.path)]=req;
            #if str(req.method)==HTTP_PUT:
            #    self.put_request_object_map[str(req.path)]=req;



    def set_start_time(self):
        if not self.has_set_time:
            self.has_set_time=True
            self.start_time=time.time()


    def update_system_requests(self,path,type):
        with self.system_lock:
            self.update_tail_count(path,type)
            if type==HTTP_GET:
                self.system_get_count+=1
            elif type==HTTP_PUT:
                self.system_put_count+=1

    def get_read_write_performance(self):
        duration=time.time()-self.start_time
        if duration > 0:
            read= self.system_get_count / duration
            write=self.system_put_count / duration
        else:
            read=0
            write=0
        return [read,write]

    def log_performace(self):
        with self.system_lock:
            duration=time.time()-self.start_time
            if duration > 0:
                read= self.system_get_count / duration
                write=self.system_put_count / duration
            else:
                read=0
                write=0

            if self.system_get_count>0:
                read_avg_duration=self.system_get_duration/self.system_get_count
            else:
                read_avg_duration=0

            if self.system_put_count>0:
                write_avg_duration=self.system_put_duration/self.system_put_count
            else:
                write_avg_duration=0

            log_performace(read,write,self.system_get_count,self.system_put_count,read_avg_duration,write_avg_duration,self.system_replied_get_count,self.system_replied_put_count,DEFAULT_WRITE_QUORUM)
            self.system_get_count=0
            self.system_put_count=0
            self.system_get_duration=0
            self.system_put_duration=0
            self.system_replied_get_count=0
            self.system_replied_put_count=0
            self.start_time=time.time()





    def add_objects_to_list(self,path,type):
        with self.object_lock:
            self.update_system_requests(path,type)
            if is_adaptive_mode and not get_quorum_handler().Is_Optimize_Tail():
                if type == HTTP_GET:
                    self.read_object_path_list.append(path)
                    if path in self.get_request_count_map.keys():
                        self.get_request_count_map[path]+=1
                    else:
                        self.get_request_count_map[path]=1
                elif type == HTTP_PUT:
                    self.write_object_path_list.append(path)
                    if path in self.put_request_count_map.keys():
                        self.put_request_count_map[path]+=1
                    else:
                        self.put_request_count_map[path]=1

    def update_tail_duration(self,path,duration,type):
        if not get_quorum_handler().is_key_in_map(path):
            if type=="GET":
                self.tail_system_get_duration+=duration
                self.tail_system_replied_get_count+=1
            else:
                self.tail_system_put_duration+=duration
                self.tail_system_replied_put_count+=1

    def update_tail_count(self,path,type):
        if not get_quorum_handler().is_key_in_map(path):
            if type=="GET":
                self.tail_system_get_count+=1
            else:
                self.tail_system_put_count+=1

    def sum_get_duration(self,path,duration):
        #log_oracle_plus("sum_get_duration = "+path +" Duration = "+str(duration))
        self.update_tail_duration(path,duration,"GET")
        if is_adaptive_mode and not get_quorum_handler().Is_Optimize_Tail():

            if path in self.total_get_request_duration_map.keys():
                self.total_get_request_duration_map[path]+=duration
            else:
                self.total_get_request_duration_map[path]=duration

            if path in self.replied_get_count_map.keys():
                self.replied_get_count_map[path]+=1
            else:
                self.replied_get_count_map[path]=1
        if IS_ML_TRAINING:
            self.system_get_duration+=duration
            self.system_replied_get_count+=1

    def sum_get_duration_new(self,path,duration):
        #log_oracle_plus("sum_get_duration = "+path +" Duration = "+str(duration))
        self.update_tail_duration(path,duration,"GET")
        if is_adaptive_mode and not get_quorum_handler().Is_Optimize_Tail():

            if len(self.read_topk_map)>0 and path in self.read_topk_map.keys():
                if path in self.total_get_request_duration_map.keys():
                    self.total_get_request_duration_map[path]+=duration
                else:
                    self.total_get_request_duration_map[path]=duration

                if path in self.replied_get_count_map.keys():
                    self.replied_get_count_map[path]+=1
                else:
                    self.replied_get_count_map[path]=1
        if IS_ML_TRAINING:
            self.system_get_duration+=duration
            self.system_replied_get_count+=1

    def sum_put_duration(self,path,duration):
        #log_oracle_plus("sum_put_duration = "+path +" Duration = "+str(duration))
        self.update_tail_duration(path,duration,"PUT")
        if is_adaptive_mode and not get_quorum_handler().Is_Optimize_Tail():
            if path in self.total_put_request_duration_map.keys():
                self.total_put_request_duration_map[path]+=duration
            else:
                self.total_put_request_duration_map[path]=duration

            if path in self.replied_put_count_map.keys():
                self.replied_put_count_map[path]+=1
            else:
                self.replied_put_count_map[path]=1
        if IS_ML_TRAINING:
            self.system_put_duration+=duration
            self.system_replied_put_count+=1

    def sum_put_duration_new(self,path,duration):
        #log_oracle_plus("sum_put_duration = "+path +" Duration = "+str(duration))
        self.update_tail_duration(path,duration,"PUT")
        if is_adaptive_mode and not get_quorum_handler().Is_Optimize_Tail():

            if len(self.write_topk_map)>0 and path in self.write_topk_map.keys():
                if path in self.total_put_request_duration_map.keys():
                    self.total_put_request_duration_map[path]+=duration
                else:
                    self.total_put_request_duration_map[path]=duration

                if path in self.replied_put_count_map.keys():
                    self.replied_put_count_map[path]+=1
                else:
                    self.replied_put_count_map[path]=1
        if IS_ML_TRAINING:
            self.system_put_duration+=duration
            self.system_replied_put_count+=1

    def calc_average_put_duration(self):
        for path in self.replied_put_count_map.keys():
            if self.replied_put_count_map[path]>0 and path in self.total_put_request_duration_map.keys():
                self.avg_put_request_duration_map[path] = self.total_put_request_duration_map[path] / self.replied_put_count_map[path]
            else:
                self.avg_put_request_duration_map[path]= 0



    def calc_average_get_duration(self):
        for path in self.replied_get_count_map.keys():
            if self.replied_get_count_map[path]>0  and path in self.total_get_request_duration_map.keys():
                self.avg_get_request_duration_map[path] = self.total_get_request_duration_map[path] / self.replied_get_count_map[path]
            else:
                self.avg_get_request_duration_map[path]=0

    def calc_average_get_duration_new(self):
        for path in self.read_topk_map.keys():
            if path in self.replied_get_count_map.keys() and self.replied_get_count_map[path]>0  and path in self.total_get_request_duration_map.keys():
                self.avg_get_request_duration_map[path] = self.total_get_request_duration_map[path] / self.replied_get_count_map[path]
            else:
                self.avg_get_request_duration_map[path]=0

    def calc_average_put_duration_new(self):
        for path in self.write_topk_map.keys():
            if path in self.replied_put_count_map.keys() and self.replied_put_count_map[path]>0 and path in self.total_put_request_duration_map.keys():
                self.avg_put_request_duration_map[path] = self.total_put_request_duration_map[path] / self.replied_put_count_map[path]
            else:
                self.avg_put_request_duration_map[path]= 0

    def get_top_read_map(self):
        return self.read_topk_map

    def get_top_write_map(self):
        return  self.write_topk_map

    def reset_statistics(self):
        with self.object_lock:
            self.get_request_count_map={}
            self.put_request_count_map={}
            self.total_get_request_duration_map={}
            self.total_put_request_duration_map={}
            self.replied_get_count_map={}
            self.replied_put_count_map={}
            self.put_request_object_map={}

            self.tail_system_get_count=0
            self.tail_system_put_count=0
            self.tail_system_get_duration=0
            self.tail_system_put_duration=0
            self.tail_system_replied_get_count=0
            self.tail_system_replied_put_count=0


    count=0
    def find_topk(self):
        if IS_TEST_COMMUNICATION:
            if IS_MASTER:
                message="From Master| at *"
            else:
                message="From IP |= "+str(CURRENT_IP)+" at ?*"
            getMessageProcessor().send_message(message)
        else:
            if self.count <2:
                if len(self.read_topk_map) >0 or len(self.write_topk_map) >0:
                    log_oracle_plus("Inside reporting topk at round "+str(self.count))
                    self.calc_average_get_duration_new()
                    self.calc_average_put_duration_new()
                else:
                    log_oracle_plus("No topk map at round "+str(self.count))
                performace= self.get_read_write_performance()
                if IS_ML_ENABLED:
                    #get_quorum_handler().update_quorum_map_with_ML("UPDATE",self.read_topk_map,self.write_topk_map,self.get_request_count_map,self.put_request_count_map,self.avg_get_request_duration_map,self.avg_put_request_duration_map,self.replied_get_count_map,self.replied_put_count_map,self.put_request_object_map,performace)
                    log_oracle_plus("Skipped ML")
                else:
                    get_quorum_handler().update_quorum_map("UPDATE",self.read_topk_map,self.write_topk_map)
                self.read_topk_map={}
                self.write_topk_map={}
                self.update_read_topk()
                self.update_write_topk()
                self.print_topk()
                self.log_performace()
                self.reset_statistics()
                self.count+=1
            else:
                if IS_ML_ENABLED:
                    get_quorum_handler().set_tail_optimization_status(True)
                    if self.tail_system_get_count>0:
                        read_avg_duration=self.tail_system_get_duration/self.tail_system_get_count
                    else:
                        read_avg_duration=0

                    if self.tail_system_put_count>0:
                        write_avg_duration=self.tail_system_put_duration/self.tail_system_put_count
                    else:
                        write_avg_duration=0
                    if not self.has_tail_started:
                        self.has_tail_started=True
                        get_quorum_handler().update_tail_quorum_with_ML(self.tail_system_put_count,self.tail_system_get_count,read_avg_duration,write_avg_duration,self.tail_system_replied_get_count,self.tail_system_replied_put_count)

                self.count+=1
                self.log_performace()
                self.reset_statistics()

            if self.count==60:
                get_quorum_handler().set_tail_optimization_status(False)
                self.has_tail_started=False
                log_oracle_plus("Flushing the optimizations")
                self.count=0;
                self.read_topk_map={}
                self.write_topk_map={}
                self.read_old_topk_map={}
                self.write_old_topk_map={}
                get_quorum_handler().clear_quorum_map()
                #here we need to write the data back for objects those write quorums size increases

            '''
            self.update_read_topk()
            self.update_write_topk()
            self.print_topk()
            self.calc_average_get_duration()
            self.calc_average_put_duration()
            performace= self.get_read_write_performance()
            if IS_ML_ENABLED:
                get_quorum_handler().update_quorum_map_with_ML("UPDATE",self.read_topk_map,self.write_topk_map,self.get_request_count_map,self.put_request_count_map,self.avg_get_request_duration_map,self.avg_put_request_duration_map,self.replied_get_count_map,self.replied_put_count_map,self.put_request_object_map,performace)
            else:
                get_quorum_handler().update_quorum_map("UPDATE",self.read_topk_map,self.write_topk_map)
            self.log_performace()
            self.reset_statistics()
            '''

    def print_topk(self):
        log_oracle_plus("READ TOPK MAP - " + str(len(self.read_topk_map)))
        log_oracle_plus(str(self.read_topk_map))
        log_oracle_plus("WRITE TOPK MAP - "+ str(len(self.write_topk_map)))
        log_oracle_plus(str(self.write_topk_map))

    def update_read_topk(self):
        #Updating the map should consider the threshold difference so that it will not add records when objects are not hot
        if len(self.read_object_path_list) > 0:
            temp_read_list=list(self.read_object_path_list)
            del self.read_object_path_list[:]

            filtered_list=[]
            for i in range(0,len(temp_read_list)):
                if temp_read_list[i] not in self.read_old_topk_map.keys():
                    filtered_list.append(temp_read_list[i])

            if len(filtered_list)>0:
                read_input=SEP_PIPE.join(filtered_list)
                read_topk=self.process_stream(read_input)
                log_oracle_plus(read_topk)
                rlist,rcount = self.procss_stream_output(read_topk)
                for i in range(0,int(len(rlist)/10)):
                    self.read_topk_map[rlist[i]]=rcount[i]
                    self.read_old_topk_map[rlist[i]]=rcount[i]

    def update_write_topk(self):
        #Updating the map should consider the threshold difference so that it will not add records when objects are not hot
        if len(self.write_object_path_list) > 0:
            temp_write_list=list(self.write_object_path_list)
            del self.write_object_path_list[:]

            filtered_list=[]
            for i in range(0,len(temp_write_list)):
                if temp_write_list[i] not in self.write_old_topk_map:
                    filtered_list.append(temp_write_list[i])

            if len(filtered_list)>0:
                write_input=SEP_PIPE.join(filtered_list)
                write_topk=self.process_stream(write_input)
                log_oracle_plus(write_topk)
                wlist,wcount = self.procss_stream_output(write_topk)
                for i in range(0,int(len(wlist)/10)):
                    self.write_topk_map[wlist[i]]=wcount[i]
                    self.write_old_topk_map[wlist[i]]=wcount[i]


    def procss_stream_output(self,result):
        list=result.split(SEP_COMMA)
        top_item_list=[]
        top_item_count_list=[]
        for item in list:
            temp_item_array=item.split(SEP_PIPE)
            error_percentage= (float(int(temp_item_array[2]))/ int(temp_item_array[1]))*100
            #log_oracle_plus("ERROR = "+str(error_percentage))
            if error_percentage <= TOPK_ERROR_THRESHOLD_PERCENTAGE:
                top_item_list.append(temp_item_array[0])
                top_item_count_list.append(int(temp_item_array[1]) - int(temp_item_array[2]))
        return  top_item_list,top_item_count_list



    def process_stream(self,input):
        connection=Producer(topk_ip, topk_port)
        return  connection.send_get_message(input+"\r\n")




statistics = Statistics()

def get_statistics():
    return statistics
