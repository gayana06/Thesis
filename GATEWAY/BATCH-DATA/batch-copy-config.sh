for i in  172.31.0.186 172.31.0.148 172.31.0.149 172.31.0.168 172.31.0.137
do
   echo "Sending to $i"
   #scp -r -i gayana-keypair.pem /home/gchandrasekara/DEPLOYMENT/swift/* ubuntu@$i:/home/ubuntu/swift
   cp config.py config-ip.py
   sed -i "s/<CURRENT_IP>/$i/" config-ip.py
   scp -i gayana-keypair.pem config-ip.py ubuntu@$i:/home/ubuntu/swift/swift/oracle_plus/config.py
   ssh -i gayana-keypair.pem ubuntu@$i "cd /home/ubuntu;./start-proxy.sh"
   echo "Done"
done
