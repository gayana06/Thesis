ZIPFIAN_CONSTANT=0.00
for i in 172.31.0.106 172.31.0.154 172.31.0.161 172.31.0.163 172.31.0.157
do
echo "Copying zipf file to... $i"
  cp FILES/ZipfDistribution.py .
  sed -i "s/<ZIPFIAN_CONSTANT>/$ZIPFIAN_CONSTANT/" /home/gchandrasekara/AUTOMATE-SCRIPTS/SSBENCH-SETTINGS/ZipfDistribution.py
  scp -i /home/gchandrasekara/AUTOMATE-SCRIPTS/gayana-keypair.pem ZipfDistribution.py ubuntu@$i:/home/ubuntu/ssbench-deployment/ssbench/ssbench/ZipfDistribution.py
  ssh -i /home/gchandrasekara/AUTOMATE-SCRIPTS/gayana-keypair.pem  ubuntu@$i "cd /home/ubuntu;./deploy.sh" 
echo "Done"
done
