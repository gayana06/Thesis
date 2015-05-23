k=1
#for i in 172.31.0.106 172.31.0.163 172.31.0.168 172.31.0.170 172.31.0.171 172.31.0.172 172.31.0.173 172.31.0.174 172.31.0.5 172.31.0.169

for i in  172.31.0.106 172.31.0.154 172.31.0.161 172.31.0.163 172.31.0.157
do
   echo "Sending to $i K = $k "
   scp -i gayana-keypair.pem /home/gchandrasekara/BATCH-DATA/SCENARIOS/$k/very_small.scenario ubuntu@$i:/home/ubuntu
   k=$((k + 1))
   echo "Done"
done
