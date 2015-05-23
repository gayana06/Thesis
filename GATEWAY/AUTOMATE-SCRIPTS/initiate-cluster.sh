for i in 172.31.0.106 172.31.0.154 172.31.0.161 172.31.0.170 172.31.0.171
do 
echo "Started init for $i"
ssh -i /home/gchandrasekara/AUTOMATE-SCRIPTS/gayana-keypair.pem  ubuntu@$i "cd /home/ubuntu;./myscript.sh"
echo "Sleep 90s"
sleep 110s
echo "Done init"
done
