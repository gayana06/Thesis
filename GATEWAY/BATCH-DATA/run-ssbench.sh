for i in 172.31.0.106
do
   echo "Connecting to $i"
   ssh -i gayana-keypair.pem ubuntu@$i "cd /home/ubuntu;./run-ssbench.sh"
   echo "Done"
done
