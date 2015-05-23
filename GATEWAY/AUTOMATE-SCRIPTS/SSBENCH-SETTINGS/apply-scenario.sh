size_min=5000
size_max=50000
file_count=4000
Is_Mix_Workload_Mode=True
wa_set="[0,100,0,0]"
wb_set="[0,0,100,0]"
run_seconds=1800
crud_profile="[0,0,100,0]"
container_count=100
container_concurrency=10
namecount=1
basecount=1
for i in 172.31.0.106 172.31.0.154 172.31.0.161 172.31.0.163 172.31.0.157
do
  echo "Copying scenario file to... $i" 
  cp FILES/very_small.scenario .
  sed -i "s/<size_min>/$size_min/" /home/gchandrasekara/AUTOMATE-SCRIPTS/SSBENCH-SETTINGS/very_small.scenario 
  sed -i "s/<size_max>/$size_max/" /home/gchandrasekara/AUTOMATE-SCRIPTS/SSBENCH-SETTINGS/very_small.scenario
  sed -i "s/<file_count>/$file_count/" /home/gchandrasekara/AUTOMATE-SCRIPTS/SSBENCH-SETTINGS/very_small.scenario
  sed -i "s/<Is_Mix_Workload_Mode>/$Is_Mix_Workload_Mode/" /home/gchandrasekara/AUTOMATE-SCRIPTS/SSBENCH-SETTINGS/very_small.scenario
  wa_name="w$namecount"
  namecount=$((namecount + 1))  
  wb_name="w$namecount"
  namecount=$((namecount + 1))
  sed -i "s/<wa_name>/$wa_name/" /home/gchandrasekara/AUTOMATE-SCRIPTS/SSBENCH-SETTINGS/very_small.scenario
  sed -i "s/<wa_set>/$wa_set/" /home/gchandrasekara/AUTOMATE-SCRIPTS/SSBENCH-SETTINGS/very_small.scenario
  sed -i "s/<wb_name>/$wb_name/" /home/gchandrasekara/AUTOMATE-SCRIPTS/SSBENCH-SETTINGS/very_small.scenario
  sed -i "s/<wb_set>/$wb_set/" /home/gchandrasekara/AUTOMATE-SCRIPTS/SSBENCH-SETTINGS/very_small.scenario  
  sed -i "s/<run_seconds>/$run_seconds/" /home/gchandrasekara/AUTOMATE-SCRIPTS/SSBENCH-SETTINGS/very_small.scenario
  sed -i "s/<crud_profile>/$crud_profile/" /home/gchandrasekara/AUTOMATE-SCRIPTS/SSBENCH-SETTINGS/very_small.scenario
  container_base="w$basecount"
  basecount=$((basecount + 1))
  sed -i "s/<container_base>/$container_base/" /home/gchandrasekara/AUTOMATE-SCRIPTS/SSBENCH-SETTINGS/very_small.scenario
  sed -i "s/<container_count>/$container_count/" /home/gchandrasekara/AUTOMATE-SCRIPTS/SSBENCH-SETTINGS/very_small.scenario
  sed -i "s/<container_concurrency>/$container_concurrency/" /home/gchandrasekara/AUTOMATE-SCRIPTS/SSBENCH-SETTINGS/very_small.scenario

  scp -i /home/gchandrasekara/AUTOMATE-SCRIPTS/gayana-keypair.pem very_small.scenario ubuntu@$i:/home/ubuntu/very_small.scenario
  echo "Done"  
done

