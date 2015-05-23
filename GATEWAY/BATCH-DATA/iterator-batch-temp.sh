#!/bin/bash 
min_size=5000
max_size=50000
objcount=4000
proxycount=5
r0w100="[0,5,95,0]"
r10w90="[0,15,85,0]"
r20w80="[0,25,75,0]"
r30w70="[0,35,65,0]"
r40w60="[0,45,55,0]"
r50w50="[0,55,45,0]"
r60w40="[0,65,35,0]"
r70w30="[0,75,25,0]"
r80w20="[0,85,15,0]"
r90w10="[0,95,5,0]"
r100w0="[0,100,0,0]"
p=0

for (( i=56; i <= 105; i++ ))
do
 
 cp /home/gchandrasekara/BATCH-DATA/Template/config.py /home/gchandrasekara/BATCH-DATA/config.py
 if [ $p -eq 0 ]
 then
   pt=$r0w100
   echo "$pt"
 elif [ $p -eq 1 ]
 then
   pt=$r10w90
   echo "$pt"
 elif [ $p -eq 2 ]
 then
   pt=$r20w80
   echo "$pt"
 elif [ $p -eq 3 ]
 then
   pt=$r30w70
   echo "$pt"
 elif [ $p -eq 4 ]
 then
   pt=$r40w60
   echo "$pt"
 elif [ $p -eq 5 ]
 then
   pt=$r50w50
   echo "$pt"
 elif [ $p -eq 6 ]
 then
   pt=$r60w40
   echo "$pt"
 elif [ $p -eq 7 ]
 then
   pt=$r70w30
   echo "$pt"
 elif [ $p -eq 8 ]
 then
   pt=$r80w20
   echo "$pt"
 elif [ $p -eq 9 ]
 then
   pt=$r90w10
   echo "$pt"
 else
   pt=$r100w0
   echo "$pt"
 fi 

 remainder=$((i%5)) 
 if [ $remainder -eq 1 ]
 then 
   readq=5
   writeq=1
 elif [ $remainder -eq 2 ]
 then
   readq=4
   writeq=2
 elif [ $remainder -eq 3 ]
 then
   readq=3
   writeq=3
 elif [ $remainder -eq 4 ]
 then
   readq=2
   writeq=4
 else
   readq=1
   writeq=5
   p=$((p + 1))
   if [ $p -eq 11 ]
   then
     p=0
     echo "------"
   fi
 fi
  
 #echo "READ = $readq"
 #echo "WRITE = $writeq "

 sed -i "s/<ID>/$i/" /home/gchandrasekara/BATCH-DATA/config.py
 sed -i "s/<READQ>/$readq/" /home/gchandrasekara/BATCH-DATA/config.py
 sed -i "s/<WRITEQ>/$writeq/" /home/gchandrasekara/BATCH-DATA/config.py
 
 

 for (( k=1; k <= $proxycount; k++ ))
 do
   cp /home/gchandrasekara/BATCH-DATA/Template/very_small.scenario /home/gchandrasekara/BATCH-DATA/SCENARIOS/$k/very_small.scenario
   sed -i "s/<MIN>/$min_size/" /home/gchandrasekara/BATCH-DATA/SCENARIOS/$k/very_small.scenario
   sed -i "s/<MAX>/$max_size/" /home/gchandrasekara/BATCH-DATA/SCENARIOS/$k/very_small.scenario
   sed -i "s/<COUNT>/$objcount/" /home/gchandrasekara/BATCH-DATA/SCENARIOS/$k/very_small.scenario
   sed -i "s/<CRUD>/$pt/" /home/gchandrasekara/BATCH-DATA/SCENARIOS/$k/very_small.scenario
   sed -i "s/<NAME>/w$k/" /home/gchandrasekara/BATCH-DATA/SCENARIOS/$k/very_small.scenario


 done
 ./batch-copy-config.sh
 ./batch-copy-scenario.sh
 sleep 1s
 ./run-ssbench.sh
 echo "Long sleep 180 seconds"
 sleep 180s

 ./get-output-files.sh
 ./get-output-files.sh
 mkdir /home/gchandrasekara/BATCH-DATA/ML_DATASET/$i
 cp /home/gchandrasekara/BATCH-DATA/output/* /home/gchandrasekara/BATCH-DATA/ML_DATASET/$i
  
 echo "Completed run $i of $pt Read = $readq Write = $writeq"
 
done

echo "Full run completed"

