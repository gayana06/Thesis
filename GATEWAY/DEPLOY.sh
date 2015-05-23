for i in  172.31.0.186 172.31.0.148 172.31.0.149 172.31.0.168 172.31.0.137
#for i in  172.31.0.137
do
scp -r -i .ssh/gayana-keypair.pem DEPLOYMENT/swift/* ubuntu@$i:/home/ubuntu/swift
done
