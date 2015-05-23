is_ram=False
for i in 172.31.0.142 172.31.0.147 172.31.0.145 172.31.0.146 172.31.0.144 172.31.0.108 172.31.0.115 172.31.0.124 172.31.0.118 172.31.0.117
do
  echo "Keep original disk writes in Storage $i"
  cp FILES/diskfile.py .
  sed -i "s/<is_ram>/$is_ram/" /home/gchandrasekara/AUTOMATE-SCRIPTS/STORAGE-SETTINGS/diskfile.py
  scp -i /home/gchandrasekara/AUTOMATE-SCRIPTS/gayana-keypair.pem diskfile.py  ubuntu@$i:/home/ubuntu/swift/swift/obj/diskfile.py
  echo "Done"
done
