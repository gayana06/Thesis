object_chunk_size=65536
client_chunk_size=65536
number_of_replicas=5
average_window_size=20
use_adaptation=False
initial_write_quorum_size=3
initial_read_quorum_size=3
master_ip=172.31.0.186
slave_ips=172.31.0.148,172.31.0.149,172.31.0.168,172.31.0.137
replica_reconciliation_timeout=2
for i in  172.31.0.186 172.31.0.148 172.31.0.149 172.31.0.168 172.31.0.137
do
  echo "COPYING proxy-server.conf to  ...$i"
  cp FILES/proxy-server.conf .
  sed -i "s/<bind_ip>/$i/" /home/gchandrasekara/AUTOMATE-SCRIPTS/PROXY-SETTINGS/proxy-server.conf
  sed -i "s/<object_chunk_size>/$object_chunk_size/" /home/gchandrasekara/AUTOMATE-SCRIPTS/PROXY-SETTINGS/proxy-server.conf
  sed -i "s/<client_chunk_size>/$client_chunk_size/" /home/gchandrasekara/AUTOMATE-SCRIPTS/PROXY-SETTINGS/proxy-server.conf
  sed -i "s/<number_of_replicas>/$number_of_replicas/" /home/gchandrasekara/AUTOMATE-SCRIPTS/PROXY-SETTINGS/proxy-server.conf
  sed -i "s/<average_window_size>/$average_window_size/" /home/gchandrasekara/AUTOMATE-SCRIPTS/PROXY-SETTINGS/proxy-server.conf
  sed -i "s/<use_adaptation>/$use_adaptation/" /home/gchandrasekara/AUTOMATE-SCRIPTS/PROXY-SETTINGS/proxy-server.conf
  sed -i "s/<initial_write_quorum_size>/$initial_write_quorum_size/" /home/gchandrasekara/AUTOMATE-SCRIPTS/PROXY-SETTINGS/proxy-server.conf
  sed -i "s/<initial_read_quorum_size>/$initial_read_quorum_size/" /home/gchandrasekara/AUTOMATE-SCRIPTS/PROXY-SETTINGS/proxy-server.conf
  sed -i "s/<ip>/$i/" /home/gchandrasekara/AUTOMATE-SCRIPTS/PROXY-SETTINGS/proxy-server.conf
  sed -i "s/<master_ip>/$master_ip/" /home/gchandrasekara/AUTOMATE-SCRIPTS/PROXY-SETTINGS/proxy-server.conf
  sed -i "s/<replica_reconciliation_timeout>/$replica_reconciliation_timeout/" /home/gchandrasekara/AUTOMATE-SCRIPTS/PROXY-SETTINGS/proxy-server.conf
  
  if [ $i == $master_ip ]
  then
   sed -i "s/<slave_ips>/$slave_ips/" /home/gchandrasekara/AUTOMATE-SCRIPTS/PROXY-SETTINGS/proxy-server.conf
  else
   sed -i "s/<slave_ips>//" /home/gchandrasekara/AUTOMATE-SCRIPTS/PROXY-SETTINGS/proxy-server.conf
  fi
    
  scp -i /home/gchandrasekara/AUTOMATE-SCRIPTS/gayana-keypair.pem proxy-server.conf ubuntu@$i:/etc/swift/proxy-server.conf  
  echo "Done"
done
