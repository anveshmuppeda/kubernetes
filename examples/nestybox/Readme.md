# Nestybox Sysbox  


## Create Public Node Group   
eksctl create nodegroup --cluster=eksdemo \
                       --region=us-east-1 \
                       --name=sysbox-ng \
                       --node-ami-family=Ubuntu2004 \
                       --node-type=t3.xlarge \
                       --nodes=2 \
                       --nodes-min=2 \
                       --nodes-max=4 \
                       --node-volume-size=200 \
                       --ssh-access \
                       --ssh-public-key=us-east-1 \
                       --managed \
                       --asg-access \
                       --external-dns-access \
                       --full-ecr-access \
                       --appmesh-access \
                       --alb-ingress-access 


## label nodes  
```
kubectl label nodes ip-192-168-29-114.ec2.internal sysbox-install=yes-
kubectl label nodes ip-192-168-29-114.ec2.internal sysbox-runtime=running-
```