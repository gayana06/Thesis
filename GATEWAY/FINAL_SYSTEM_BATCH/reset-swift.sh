for i in  172.31.0.117 172.31.0.118 172.31.0.124 172.31.0.137 172.31.0.142 172.31.0.147 172.31.0.145 172.31.0.146 172.31.0.144 172.31.0.157
#for i in  172.31.0.179 172.31.0.176 172.31.0.177 172.31.0.178 172.31.0.175
do
   echo "Sending to $i"
   #scp -r -i gayana-keypair.pem /home/gchandrasekara/DEPLOYMENT/swift/* ubuntu@$i:/home/ubuntu/swift
   #scp -i gayana-keypair.pem config.py ubuntu@$i:/home/ubuntu/swift/swift/oracle_plus/config.py
   ssh -i gayana-keypair.pem ubuntu@$i "cd /home/ubuntu/bin;./resetswift"
   echo "Done"
done
