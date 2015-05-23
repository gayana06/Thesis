rm output/*
#for i in 172.31.0.106 172.31.0.163 172.31.0.168 172.31.0.170 172.31.0.171 172.31.0.172 172.31.0.173 172.31.0.174 172.31.0.5 172.31.0.169
for i in  172.31.0.106 172.31.0.154 172.31.0.161 172.31.0.163 172.31.0.157
do
   echo "Connecting to $i "
   scp -i gayana-keypair.pem  ubuntu@$i:/home/ubuntu/ssbench-output.txt    /home/gchandrasekara/BATCH-DATA/output/$i-ssbench.txt
   #mv /home/gchandrasekara/BATCH-DATA/output/ssbench-output.txt /home/gchandrasekara/BATCH-DATA/output/so-$i.txt
   echo "Done"
done


#for i in 172.31.0.107 172.31.0.164 172.31.0.175 172.31.0.176 172.31.0.177 172.31.0.178 172.31.0.179 172.31.0.161 172.31.0.166 172.31.0.167
for i in  172.31.0.186 172.31.0.148 172.31.0.149 172.31.0.168 172.31.0.137
do
   echo "Connecting to $i "
   scp -i gayana-keypair.pem  ubuntu@$i:/home/ubuntu/performace.txt    /home/gchandrasekara/BATCH-DATA/output/$i-performace.txt
   #scp -i gayana-keypair.pem  ubuntu@$i:/home/ubuntu/quorum_map.txt    /home/gchandrasekara/BATCH-DATA/output/$i-quorum_map.txt
   #mv /home/gchandrasekara/BATCH-DATA/output/ssbench-output.txt /home/gchandrasekara/BATCH-DATA/output/so-$i.txt
   echo "Done"
done

