rm output/*
for i in  172.31.0.106 172.31.0.163 172.31.0.157 172.31.0.154 172.31.0.161
do
   echo "Connecting to $i "
   scp -i gayana-keypair.pem  ubuntu@$i:/home/ubuntu/ssbench-output.txt    /home/gchandrasekara/AUTOMATE-SCRIPTS/output/$i-ssbench.txt
   scp -i gayana-keypair.pem  ubuntu@$i:/home/ubuntu/job.txt    /home/gchandrasekara/AUTOMATE-SCRIPTS/output/$i-job.txt
   echo "Done"
done


for i in 172.31.0.137 172.31.0.168 172.31.0.149 172.31.0.148 172.31.0.186
do
   echo "Connecting to $i "
   scp -i gayana-keypair.pem  ubuntu@$i:/home/ubuntu/performace.txt    /home/gchandrasekara/AUTOMATE-SCRIPTS/output/$i-performace.txt
   scp -i gayana-keypair.pem  ubuntu@$i:/home/ubuntu/quorum_map.txt    /home/gchandrasekara/AUTOMATE-SCRIPTS/output/$i-quorum_map.txt
   scp -i gayana-keypair.pem  ubuntu@$i:/home/ubuntu/sent.txt    /home/gchandrasekara/AUTOMATE-SCRIPTS/output/$i-sent.txt
   scp -i gayana-keypair.pem  ubuntu@$i:/home/ubuntu/processed.txt    /home/gchandrasekara/AUTOMATE-SCRIPTS/output/$i-processed.txt
   scp -i gayana-keypair.pem  ubuntu@$i:/home/ubuntu/oracle_plus.txt    /home/gchandrasekara/AUTOMATE-SCRIPTS/output/$i-oracle_plus.txt
   scp -i gayana-keypair.pem  ubuntu@$i:/home/ubuntu/ml_q.txt    /home/gchandrasekara/AUTOMATE-SCRIPTS/output/$i-ml_q.txt
#   scp -i gayana-keypair.pem  ubuntu@$i:/home/ubuntu/WritesA.txt    /home/gchandrasekara/AUTOMATE-SCRIPTS/output/$i-writesA.txt
#   scp -i gayana-keypair.pem  ubuntu@$i:/home/ubuntu/WritesB.txt    /home/gchandrasekara/AUTOMATE-SCRIPTS/output/$i-writesB.txt
#   scp -i gayana-keypair.pem  ubuntu@$i:/home/ubuntu/WritesC.txt    /home/gchandrasekara/AUTOMATE-SCRIPTS/output/$i-writesC.txt
#   scp -i gayana-keypair.pem  ubuntu@$i:/home/ubuntu/WritesD.txt    /home/gchandrasekara/AUTOMATE-SCRIPTS/output/$i-writesD.txt
#   scp -i gayana-keypair.pem  ubuntu@$i:/home/ubuntu/WritesE.txt    /home/gchandrasekara/AUTOMATE-SCRIPTS/output/$i-writesE.txt
#   scp -i gayana-keypair.pem  ubuntu@$i:/home/ubuntu/Read.txt    /home/gchandrasekara/AUTOMATE-SCRIPTS/output/$i-Read.txt
#   scp -i gayana-keypair.pem  ubuntu@$i:/home/ubuntu/ReadA.txt    /home/gchandrasekara/AUTOMATE-SCRIPTS/output/$i-readA.txt

   echo "Done"
done


