Workers=20

 #for i in 172.31.0.142 172.31.0.147 172.31.0.145 172.31.0.146 172.31.0.144
 for i in 172.31.0.108 172.31.0.115 172.31.0.117 172.31.0.118 172.31.0.124
 do
   cp /home/gchandrasekara/FINAL_SYSTEM_BATCH/object/1.conf /home/gchandrasekara/FINAL_SYSTEM_BATCH
   sed -i "s/<IP>/$i/" /home/gchandrasekara/FINAL_SYSTEM_BATCH/1.conf
   sed -i "s/<WORKERS>/$Workers/" /home/gchandrasekara/FINAL_SYSTEM_BATCH/1.conf
   scp -i gayana-keypair.pem 1.conf  ubuntu@$i:/etc/swift/object-server/1.conf 

   cp /home/gchandrasekara/FINAL_SYSTEM_BATCH/account/1.conf /home/gchandrasekara/FINAL_SYSTEM_BATCH
   sed -i "s/<IP>/$i/" /home/gchandrasekara/FINAL_SYSTEM_BATCH/1.conf
   sed -i "s/<WORKERS>/$Workers/" /home/gchandrasekara/FINAL_SYSTEM_BATCH/1.conf
   scp -i gayana-keypair.pem 1.conf  ubuntu@$i:/etc/swift/account-server/1.conf

   cp /home/gchandrasekara/FINAL_SYSTEM_BATCH/container/1.conf /home/gchandrasekara/FINAL_SYSTEM_BATCH
   sed -i "s/<IP>/$i/" /home/gchandrasekara/FINAL_SYSTEM_BATCH/1.conf
   sed -i "s/<WORKERS>/$Workers/" /home/gchandrasekara/FINAL_SYSTEM_BATCH/1.conf
   scp -i gayana-keypair.pem 1.conf  ubuntu@$i:/etc/swift/container-server/1.conf
   #scp -i gayana-keypair.pem /home/gchandrasekara/STORAGE-DEP/swift/swift/obj/server.py  ubuntu@$i:/home/ubuntu/swift/swift/obj/server.py
   ssh -i gayana-keypair.pem ubuntu@$i "cd /home/ubuntu/bin;./startmain"
 done

