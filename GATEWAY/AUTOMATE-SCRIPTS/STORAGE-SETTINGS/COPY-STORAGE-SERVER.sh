for i in 172.31.0.142 172.31.0.147 172.31.0.145 172.31.0.146 172.31.0.144 172.31.0.108 172.31.0.115 172.31.0.117 172.31.0.118 172.31.0.124 
do

scp -i /home/gchandrasekara/AUTOMATE-SCRIPTS/gayana-keypair.pem /home/gchandrasekara/STORAGE-DEP/swift/swift/obj/server.py  ubuntu@$i:/home/ubuntu/swift/swift/obj/server.py
#   ssh -i /home/gchandrasekara/AUTOMATE-SCRIPTS/gayana-keypair.pem ubuntu@$i "cd /home/ubuntu/bin;./startmain"

done
