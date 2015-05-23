rm /home/gchandrasekara/DEPLOYMENT/swift/swift/oracle_plus/config.py

for i in 172.31.0.186 172.31.0.148 172.31.0.149 172.31.0.168 172.31.0.169  
do
echo "Starting deployment in $i"
scp -r -i /home/gchandrasekara/AUTOMATE-SCRIPTS/gayana-keypair.pem /home/gchandrasekara/DEPLOYMENT/swift/* ubuntu@$i:/home/ubuntu/swift
ssh -i /home/gchandrasekara/AUTOMATE-SCRIPTS/gayana-keypair.pem ubuntu@$i "cd /home/ubuntu;rm Writes*;rm Read*;./start-proxy.sh"
echo "done"
done

