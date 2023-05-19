# EKS Cluster RBACs

### first create the rbac-test namespace, and then install nginx into it
```
kubectl create namespace rbac-test
```
### Deploy nginx pod on clsuster
```
kubectl create deploy nginx --image=nginx -n rbac-test
```

### To verify the test pods were properly installed
```
kubectl get all -n rbac-test
```

### Create IAM user and create access key
```
aws iam create-user --user-name rbac-user
aws iam create-access-key --user-name rbac-user
```

### We will use these set onther context with using above credentials
```
aws configure
```

### MAP AN IAM USER TO K8S
```
kubectl apply -f awsauth-cm.yaml
```

### Verify newly created user after login AND it should throw Forbidden errors
```
kubectl get pods -n rbac-test
```

### Create a role and role binding from Admin access
```
kubectl apply -f rbacuser-role.yaml
kubectl apply -f rbacuser-role-binding.yaml
```

### login with Kubernetes user again
### Verify newly created user after login AND it should Not throw any errors
```
kubectl get pods -n rbac-test
```
