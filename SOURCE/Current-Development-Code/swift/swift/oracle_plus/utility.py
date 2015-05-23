__author__ = 'Gayana'

from datetime import datetime
from swift.oracle_plus.config import is_adaptive_mode,log_path,PERFORMANCE_PATH,QUORUM_MAP_PATH,CASE_ID,PROCESSED_LOG_PATH,SENT_LOG_PATH,ENABLE_LOGS


def Is_Adaptive_Mode():
    return is_adaptive_mode

def get_current_datetime():
    return str(datetime.now())

def log_sent_messages(message):
    if ENABLE_LOGS:
        with open(SENT_LOG_PATH, "a") as tran_file:
            tran_file.write("Message = "+ str(message)+" --- at--- "+get_current_datetime()+"\n")

def log_processed_messages(message):
    if ENABLE_LOGS:
        with open(PROCESSED_LOG_PATH, "a") as tran_file:
            tran_file.write("Message = "+ str(message)+" --- at--- "+get_current_datetime()+"\n")

def log_query(qrery):
        with open("/home/ubuntu/ml_q.txt", "a") as tran_file:
            tran_file.write(qrery+"\n")
def log_oracle_plus(message):
    if ENABLE_LOGS:
        with open(log_path, "a") as tran_file:
            tran_file.write("Message = "+ str(message)+" --- at--- "+get_current_datetime()+"\n")

def log_performace(read, write,read_count,write_count,read_avg_duration,write_avg_duration,replied_get,replied_put,write_quorum):
    with open(PERFORMANCE_PATH, "a") as tran_file:
        tran_file.write("--------------------------------------------------------ZKZ\n")
        #tran_file.write("||CASE-ID ="+str(CASE_ID)+"|| --- at--- "+get_current_datetime()+"\n")
        #tran_file.write("||write_quorum ="+ str(write_quorum)+"|| --- at--- "+get_current_datetime()+"\n")
        #tran_file.write("||received_gets ="+ str(read_count)+"|| --- at--- "+get_current_datetime()+"\n")
        #tran_file.write("||received_puts ="+ str(write_count)+"|| --- at--- "+get_current_datetime()+"\n")
        #tran_file.write("||get_avg_latency ="+ str(read_avg_duration)+"|| --- at--- "+get_current_datetime()+"\n")
        #tran_file.write("||put_avg_latency ="+ str(write_avg_duration)+"|| --- at--- "+get_current_datetime()+"\n")
        #tran_file.write("||replied_gets ="+ str(replied_get)+"|| --- at--- "+get_current_datetime()+"\n")
        #tran_file.write("||replied_puts ="+ str(replied_put)+"|| --- at--- "+get_current_datetime()+"\n")
        tran_file.write("Read Tpt="+ str(read)+" Write Tpt="+str(write)+"|| --- at--- "+get_current_datetime()+"\n")
        tran_file.write("ZKZ--------------------------------------------------------\n\n")

def log_quorum_map(message):
    #if ENABLE_LOGS:
    with open(QUORUM_MAP_PATH, "a") as tran_file:
        tran_file.write("--------------------------------------------------------\n")
        tran_file.write("Quorum Map = "+ str(message)+" --- at--- "+get_current_datetime()+"\n")
        tran_file.write("--------------------------------------------------------\n\n")