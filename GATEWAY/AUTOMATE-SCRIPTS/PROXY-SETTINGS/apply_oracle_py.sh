is_adaptive_mode=True
IS_ML_ENABLED=True
IS_STATIC_POLICY_ENABLED=False
topk_ip="127.0.0.1"
topk_port=42000
oracle_loop_time=60
socket_receive_byte=20000
DEFAULT_READ_QUORUM=5
DEFAULT_WRITE_QUORUM=1
REPLICA_COUNT=5
TOPK_ERROR_THRESHOLD_PERCENTAGE=100
ML_IP="127.0.0.1"
ML_PORT=50000
PENDING_REQ_MONITOR_TIMEOUT=0.2
IS_PARALLEL_READ=True
IS_READ_PARALLEL_MAX=False
IS_CLASSIC_WRITE=True
IS_ML_TRAINING=False
CASE_ID=1
IS_TEST_COMMUNICATION=False
MASTER_IP="172.31.0.186"
SLAVE_IPS="[\"172.31.0.148\",\"172.31.0.149\",\"172.31.0.168\",\"172.31.0.137\"]"
LISTENING_PORT=45000
SIZE=3072
COLLECT_BEST=False
All_BEST=False
ENABLE_LOGS=False
for i in 172.31.0.186 172.31.0.148 172.31.0.149 172.31.0.168 172.31.0.137
do 
  echo "COPYING config.py to  ...$i"
  cp FILES/config.py .
  sed -i "s/<is_adaptive_mode>/$is_adaptive_mode/" /home/gchandrasekara/AUTOMATE-SCRIPTS/PROXY-SETTINGS/config.py
  sed -i "s/<IS_ML_ENABLED>/$IS_ML_ENABLED/" /home/gchandrasekara/AUTOMATE-SCRIPTS/PROXY-SETTINGS/config.py
  sed -i "s/<IS_STATIC_POLICY_ENABLED>/$IS_STATIC_POLICY_ENABLED/" /home/gchandrasekara/AUTOMATE-SCRIPTS/PROXY-SETTINGS/config.py
  sed -i "s/<topk_ip>/$topk_ip/" /home/gchandrasekara/AUTOMATE-SCRIPTS/PROXY-SETTINGS/config.py
  sed -i "s/<topk_port>/$topk_port/" /home/gchandrasekara/AUTOMATE-SCRIPTS/PROXY-SETTINGS/config.py
  sed -i "s/<oracle_loop_time>/$oracle_loop_time/" /home/gchandrasekara/AUTOMATE-SCRIPTS/PROXY-SETTINGS/config.py
  sed -i "s/<socket_receive_byte>/$socket_receive_byte/" /home/gchandrasekara/AUTOMATE-SCRIPTS/PROXY-SETTINGS/config.py
  sed -i "s/<DEFAULT_READ_QUORUM>/$DEFAULT_READ_QUORUM/" /home/gchandrasekara/AUTOMATE-SCRIPTS/PROXY-SETTINGS/config.py
  sed -i "s/<DEFAULT_WRITE_QUORUM>/$DEFAULT_WRITE_QUORUM/" /home/gchandrasekara/AUTOMATE-SCRIPTS/PROXY-SETTINGS/config.py
  sed -i "s/<REPLICA_COUNT>/$REPLICA_COUNT/" /home/gchandrasekara/AUTOMATE-SCRIPTS/PROXY-SETTINGS/config.py
  sed -i "s/<TOPK_ERROR_THRESHOLD_PERCENTAGE>/$TOPK_ERROR_THRESHOLD_PERCENTAGE/" /home/gchandrasekara/AUTOMATE-SCRIPTS/PROXY-SETTINGS/config.py
  sed -i "s/<ML_IP>/$ML_IP/" /home/gchandrasekara/AUTOMATE-SCRIPTS/PROXY-SETTINGS/config.py
  sed -i "s/<ML_PORT>/$ML_PORT/" /home/gchandrasekara/AUTOMATE-SCRIPTS/PROXY-SETTINGS/config.py
  sed -i "s/<PENDING_REQ_MONITOR_TIMEOUT>/$PENDING_REQ_MONITOR_TIMEOUT/" /home/gchandrasekara/AUTOMATE-SCRIPTS/PROXY-SETTINGS/config.py
  sed -i "s/<IS_PARALLEL_READ>/$IS_PARALLEL_READ/" /home/gchandrasekara/AUTOMATE-SCRIPTS/PROXY-SETTINGS/config.py
  sed -i "s/<IS_READ_PARALLEL_MAX>/$IS_READ_PARALLEL_MAX/" /home/gchandrasekara/AUTOMATE-SCRIPTS/PROXY-SETTINGS/config.py
  sed -i "s/<IS_CLASSIC_WRITE>/$IS_CLASSIC_WRITE/" /home/gchandrasekara/AUTOMATE-SCRIPTS/PROXY-SETTINGS/config.py
  sed -i "s/<IS_ML_TRAINING>/$IS_ML_TRAINING/" /home/gchandrasekara/AUTOMATE-SCRIPTS/PROXY-SETTINGS/config.py
  sed -i "s/<CASE_ID>/$CASE_ID/" /home/gchandrasekara/AUTOMATE-SCRIPTS/PROXY-SETTINGS/config.py
  sed -i "s/<IS_TEST_COMMUNICATION>/$IS_TEST_COMMUNICATION/" /home/gchandrasekara/AUTOMATE-SCRIPTS/PROXY-SETTINGS/config.py
  sed -i "s/<CURRENT_IP>/$i/" /home/gchandrasekara/AUTOMATE-SCRIPTS/PROXY-SETTINGS/config.py
  sed -i "s/<MASTER_IP>/$MASTER_IP/" /home/gchandrasekara/AUTOMATE-SCRIPTS/PROXY-SETTINGS/config.py
  sed -i "s/<LISTENING_PORT>/$LISTENING_PORT/" /home/gchandrasekara/AUTOMATE-SCRIPTS/PROXY-SETTINGS/config.py
  sed -i "s/<SIZE>/$SIZE/" /home/gchandrasekara/AUTOMATE-SCRIPTS/PROXY-SETTINGS/config.py
  sed -i "s/<COLLECT_BEST>/$COLLECT_BEST/" /home/gchandrasekara/AUTOMATE-SCRIPTS/PROXY-SETTINGS/config.py
  sed -i "s/<All_BEST>/$All_BEST/" /home/gchandrasekara/AUTOMATE-SCRIPTS/PROXY-SETTINGS/config.py
  sed -i "s/<ENABLE_LOGS>/$ENABLE_LOGS/" /home/gchandrasekara/AUTOMATE-SCRIPTS/PROXY-SETTINGS/config.py


  if [ $i == $MASTER_IP ]
  then
   sed -i "s/<IS_MASTER>/True/" /home/gchandrasekara/AUTOMATE-SCRIPTS/PROXY-SETTINGS/config.py
   sed -i "s/<SLAVE_IPS>/$SLAVE_IPS/" /home/gchandrasekara/AUTOMATE-SCRIPTS/PROXY-SETTINGS/config.py
  else
   sed -i "s/<IS_MASTER>/False/" /home/gchandrasekara/AUTOMATE-SCRIPTS/PROXY-SETTINGS/config.py
   sed -i "s/<SLAVE_IPS>/[]/" /home/gchandrasekara/AUTOMATE-SCRIPTS/PROXY-SETTINGS/config.py
  fi
  
  scp -i /home/gchandrasekara/AUTOMATE-SCRIPTS/gayana-keypair.pem config.py ubuntu@$i:/home/ubuntu/swift/swift/oracle_plus/config.py  

done
