for i in  172.31.0.186 172.31.0.148 172.31.0.149 172.31.0.168 172.31.0.137
do
   echo "Removing to $i"
#   ssh -i /home/gchandrasekara/AUTOMATE-SCRIPTS/gayana-keypair.pem ubuntu@$i "cd /home/ubuntu; rm RSTORAGE.txt; rm WSTORAGE.txt;rm WSTORAGE1.txt"
   ssh -i /home/gchandrasekara/AUTOMATE-SCRIPTS/gayana-keypair.pem ubuntu@$i "cd /home/ubuntu;rm ml_q.txt"
   echo "Done"
done

for i in 172.31.0.106 172.31.0.154 172.31.0.161 172.31.0.163 172.31.0.157
do 
  echo "Rmove job.txt at $i"
  ssh -i /home/gchandrasekara/AUTOMATE-SCRIPTS/gayana-keypair.pem ubuntu@$i "cd /home/ubuntu;rm job.txt"
   echo "Done"
done

