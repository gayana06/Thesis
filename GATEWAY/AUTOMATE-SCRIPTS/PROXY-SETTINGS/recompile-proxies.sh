for i in  172.31.0.186 172.31.0.148 172.31.0.149 172.31.0.168 172.31.0.137
do
  ssh -i /home/gchandrasekara/AUTOMATE-SCRIPTS/gayana-keypair.pem  ubuntu@$i "cd /home/ubuntu;./start-proxy.sh"  
done
./remove-logs.sh
