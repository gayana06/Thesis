for i in 172.31.0.106 172.31.0.163 172.31.0.168 172.31.0.170 172.31.0.171 172.31.0.172 172.31.0.173 172.31.0.174 172.31.0.5 172.31.0.169
do
   echo "Sending to $i "
   scp -i gayana-keypair.pem myscript.sh ubuntu@$i:/home/ubuntu
   echo "Done"
done
