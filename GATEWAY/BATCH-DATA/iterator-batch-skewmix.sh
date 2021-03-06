#!/bin/bash 
min_size=5000
max_size=50000
objcount=2000
proxycount=5
r0w100="[0,0,100,0]"
r10w90="[0,10,90,0]"
r20w80="[0,20,80,0]"
r30w70="[0,30,70,0]"
r40w60="[0,40,60,0]"
r50w50="[0,50,50,0]"
r60w40="[0,60,40,0]"
r70w30="[0,70,30,0]"
r80w20="[0,80,20,0]"
r90w10="[0,90,10,0]"
r100w0="[0,100,0,0]"
p=0

for (( i=1; i <= 55; i++ ))
do
 
 cp /home/gchandrasekara/BATCH-DATA/Template/config.py /home/gchandrasekara/BATCH-DATA/config.py
 if [ $p -eq 0 ]
 then
   pt=$r0w100
   pt1=$r0w100
   pt2=$r100w0
   echo "$pt1 and $pt2"
 elif [ $p -eq 1 ]
 then
   pt=$r10w90
   pt1=$r10w90
   pt2=$r90w10
   echo "$pt1 and $pt2"
 elif [ $p -eq 2 ]
 then
   pt=$r20w80
   pt1=$r20w80
   pt2=$r80w20
   echo "$pt1 and $pt2"
 elif [ $p -eq 3 ]
 then
   pt=$r30w70
   pt1=$r30w70
   pt2=$r70w30
   echo "$pt1 and $pt2"
 elif [ $p -eq 4 ]
 then
   pt=$r40w60
   pt1=$r40w60
   pt2=$r60w40
   echo "$pt1 and $pt2"
 elif [ $p -eq 5 ]
 then
   pt=$r50w50
   pt1=$r50w50
   pt2=$r50w50
   echo "$pt1 and $pt2"
 elif [ $p -eq 6 ]
 then
   pt=$r60w40
   pt1=$r60w40
   pt2=$r40w60
   echo "$pt1 and $pt2"
 elif [ $p -eq 7 ]
 then
   pt=$r70w30
   pt1=$r70w30
   pt2=$r30w70
   echo "$pt1 and $pt2"
 elif [ $p -eq 8 ]
 then
   pt=$r80w20
   pt1=$r80w20
   pt2=$r20w80
   echo "$pt1 and $pt2"
 elif [ $p -eq 9 ]
 then
   pt=$r90w10
   pt1=$r90w10
   pt2=$r10w90
   echo "$pt1 and $pt2"
 else
   pt=$r100w0
   pt1=$r100w0
   pt2=$r0w100
   echo "$pt1 and $pt2"
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
 
 
 count=1
 for (( k=1; k <= $proxycount; k++ ))
 do
   cp /home/gchandrasekara/BATCH-DATA/Template/very_small.scenario /home/gchandrasekara/BATCH-DATA/SCENARIOS/$k/very_small.scenario
   sed -i "s/<MIN>/$min_size/" /home/gchandrasekara/BATCH-DATA/SCENARIOS/$k/very_small.scenario
   sed -i "s/<MAX>/$max_size/" /home/gchandrasekara/BATCH-DATA/SCENARIOS/$k/very_small.scenario
   sed -i "s/<COUNT>/$objcount/" /home/gchandrasekara/BATCH-DATA/SCENARIOS/$k/very_small.scenario
   sed -i "s/<CRUD>/$pt/" /home/gchandrasekara/BATCH-DATA/SCENARIOS/$k/very_small.scenario
   sed -i "s/<CRUD1>/$pt1/" /home/gchandrasekara/BATCH-DATA/SCENARIOS/$k/very_small.scenario
   sed -i "s/<CRUD2>/$pt2/" /home/gchandrasekara/BATCH-DATA/SCENARIOS/$k/very_small.scenario
   sed -i "s/<NAME>/w$k/" /home/gchandrasekara/BATCH-DATA/SCENARIOS/$k/very_small.scenario
   sed -i "s/<NAME1>/w$count/" /home/gchandrasekara/BATCH-DATA/SCENARIOS/$k/very_small.scenario
   count=$((count + 1))   
   sed -i "s/<NAME2>/w$count/" /home/gchandrasekara/BATCH-DATA/SCENARIOS/$k/very_small.scenario
   count=$((count + 1))
 done
 ./batch-copy-config.sh
 ./batch-copy-scenario.sh
 sleep 1s
 ./run-ssbench.sh
 echo "Long sleep 240 seconds"
 sleep 185s

 ./get-output-files.sh
 ./get-output-files.sh
 mkdir /home/gchandrasekara/BATCH-DATA/ML_DATASET/$i
 cp /home/gchandrasekara/BATCH-DATA/output/* /home/gchandrasekara/BATCH-DATA/ML_DATASET/$i
  
 echo "Completed run $i of $pt Read = $readq Write = $writeq"
 
done

echo "Full run completed"

