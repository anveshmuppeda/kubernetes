# External Secret Manager  

### To create a secret  
```bash
echo -n 'ACCESS_KEY' > ./access-key
echo -n 'SECRET_KEY' > ./secret-access-key
kubectl create secret generic aws-iam-secret --from-file=./access-key --from-file=./secret-access-key
```