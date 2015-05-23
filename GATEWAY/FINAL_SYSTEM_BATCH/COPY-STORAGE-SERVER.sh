for i in 172.31.0.115
do

#scp -i gayana-keypair.pem /home/gchandrasekara/STORAGE-DEP/swift/swift/obj/server.py  ubuntu@$i:/home/ubuntu/swift/swift/obj/server.py
#   scp -i gayana-keypair.pem /home/gchandrasekara/FINAL_SYSTEM_BATCH/startmain  ubuntu@$i:/home/ubuntu/bin/startmain
#scp -i gayana-keypair.pem /home/gchandrasekara/STORAGE-DEP/swift/swift/common/utils.py  ubuntu@$i:/home/ubuntu/swift/swift/common/utils.py
scp -i gayana-keypair.pem /home/gchandrasekara/STORAGE-DEP/swift/swift/obj/server.py  ubuntu@$i:/home/ubuntu/swift/swift/obj/server.py
   #ssh -i gayana-keypair.pem ubuntu@$i "cd /home/ubuntu/bin;./startmain"

done
