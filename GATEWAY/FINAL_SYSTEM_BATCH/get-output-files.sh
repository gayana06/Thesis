rm output/*
rm ../BATCH-DATA/output/*
#for i in 172.31.0.106 172.31.0.163 172.31.0.168 172.31.0.170 172.31.0.171 172.31.0.172 172.31.0.173 172.31.0.174 172.31.0.5 172.31.0.169
for i in  172.31.0.106 172.31.0.170 172.31.0.171 172.31.0.154 172.31.0.161
do
   echo "Connecting to $i "
   scp -i gayana-keypair.pem  ubuntu@$i:/home/ubuntu/ssbench-output.txt    /home/gchandrasekara/BATCH-DATA/output/$i-ssbench.txt
   #mv /home/gchandrasekara/BATCH-DATA/output/ssbench-output.txt /home/gchandrasekara/BATCH-DATA/output/so-$i.txt
   echo "Done"
done


#for i in 172.31.0.107 172.31.0.164 172.31.0.175 172.31.0.176 172.31.0.177 172.31.0.178 172.31.0.179 172.31.0.161 172.31.0.166 172.31.0.167
#or i in  172.31.0.186 172.31.0.108 172.31.0.115 172.31.0.148 172.31.0.149 172.31.0.163 172.31.0.164 172.31.0.168 172.31.0.169 
for i in 172.31.0.169 172.31.0.168 172.31.0.149 172.31.0.148 172.31.0.186
do
   echo "Connecting to $i "
   scp -i gayana-keypair.pem  ubuntu@$i:/home/ubuntu/performace.txt    /home/gchandrasekara/BATCH-DATA/output/$i-performace.txt
#   scp -i gayana-keypair.pem  ubuntu@$i:/home/ubuntu/quorum_map.txt    /home/gchandrasekara/BATCH-DATA/output/$i-quorum_map.txt
#   scp -i gayana-keypair.pem  ubuntu@$i:/home/ubuntu/sent.txt    /home/gchandrasekara/BATCH-DATA/output/$i-sent.txt
#   scp -i gayana-keypair.pem  ubuntu@$i:/home/ubuntu/processed.txt    /home/gchandrasekara/BATCH-DATA/output/$i-processed.txt
#   scp -i gayana-keypair.pem  ubuntu@$i:/home/ubuntu/oracle_plus.txt    /home/gchandrasekara/BATCH-DATA/output/$i-oracle_plus.txt
#   scp -i gayana-keypair.pem  ubuntu@$i:/home/ubuntu/ml_q.txt    /home/gchandrasekara/BATCH-DATA/output/$i-ml_q.txt
#   scp -i gayana-keypair.pem  ubuntu@$i:/home/ubuntu/WritesA.txt    /home/gchandrasekara/BATCH-DATA/output/$i-writesA.txt
#   scp -i gayana-keypair.pem  ubuntu@$i:/home/ubuntu/WritesB.txt    /home/gchandrasekara/BATCH-DATA/output/$i-writesB.txt
#   scp -i gayana-keypair.pem  ubuntu@$i:/home/ubuntu/WritesC.txt    /home/gchandrasekara/BATCH-DATA/output/$i-writesC.txt
#   scp -i gayana-keypair.pem  ubuntu@$i:/home/ubuntu/WritesD.txt    /home/gchandrasekara/BATCH-DATA/output/$i-writesD.txt
#   scp -i gayana-keypair.pem  ubuntu@$i:/home/ubuntu/WritesE.txt    /home/gchandrasekara/BATCH-DATA/output/$i-writesE.txt
#   scp -i gayana-keypair.pem  ubuntu@$i:/home/ubuntu/Read.txt    /home/gchandrasekara/BATCH-DATA/output/$i-Read.txt
#scp -i gayana-keypair.pem  ubuntu@$i:/home/ubuntu/ReadA.txt    /home/gchandrasekara/BATCH-DATA/output/$i-readA.txt

   #mv /home/gchandrasekara/BATCH-DATA/output/ssbench-output.txt /home/gchandrasekara/BATCH-DATA/output/so-$i.txt
   echo "Done"
done

cp /home/gchandrasekara/BATCH-DATA/output/* /home/gchandrasekara/FINAL_SYSTEM_BATCH/output/
#./get-storage-logs.sh

