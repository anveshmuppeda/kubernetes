## Create a new user in Kubernetes Cluster  
To test RBAC we need to a user, so first create a new user. Below is the step-by-step guide to creating a new user named Anvesh in a Kubernetes cluster.  

### Step 1: Generate Certificates for the User  
1. Generate a private key for Anvesh using RSA algorithm (4096 bits):  
```bash
openssl genrsa -out anvesh.pem
```  
This command will generate an RSA private key.   

2. Create a Certificate Signing Request (CSR) for Anvesh:  
```bash
openssl req -new -key anvesh.pem -out anvesh.csr -subj "/CN=anvesh"  
```  

### Step 2: Create a Certificate Signing Request (CSR)  
1. Obtain the base64-encoded representation of the CSR:  
```bash
cat anvesh.csr | base64 | tr -d "\n"
```  
Here we encode the CSR to be used in the CertificateSigningRequest.  

2. Use the output to create a CertificateSigningRequest resource:  
```bash
cat <<EOF | kubectl apply -f -
apiVersion: certificates.k8s.io/v1
kind: CertificateSigningRequest
metadata:
  name: anvesh
spec:
  request: <base64_encoded_csr>
  signerName: kubernetes.io/kube-apiserver-client
  expirationSeconds: 86400  # one day
  usages:
  - digital signature
  - key encipherment
  - client auth
EOF  
```  

#### CSR status  
```bash
$ kubectl get csr
NAME     AGE   SIGNERNAME                            REQUESTOR                    REQUESTEDDURATION   CONDITION
anvesh   9s    kubernetes.io/kube-apiserver-client   anveshmuppeda@gmail.com      24h                 Pending
```  

### Step 3: Sign the Certificate Using the Cluster Certificate Authority  
1. Approve the CertificateSigningRequest for Anvesh:  
```bash
$ kubectl certificate approve anvesh
certificatesigningrequest.certificates.k8s.io/anvesh approved  
```  

2. Check the CSR status:  
```bash
$ kubectl describe csr/anvesh
$ kubectl get csr                         
NAME     AGE   SIGNERNAME                            REQUESTOR                    REQUESTEDDURATION   CONDITION
anvesh   31s   kubernetes.io/kube-apiserver-client   anveshmuppeda@gmail.com      24h                 Approved,Issued  
```  


### Step 4: Create a Configuration Specific to the User  
1. Extract the signed certificate from the CertificateSigningRequest:
```bash
kubectl get csr/anvesh -o jsonpath="{.status.certificate}" | base64 -d > anvesh.crt
```  

2. Create new user config file:  
Use the kubectl config set-cluster command to set up the cluster information:  
```bash
kubectl --kubeconfig ~/.kube/config-anvesh config set-cluster preprod --insecure-skip-tls-verify=true --server=https://KUBERNETES-API-ADDRESS
```  
Replace KUBERNETES-API-ADDRESS with the actual API server address of your Kubernetes cluster.  

3. Set user credentials:  
Use the kubectl config set-credentials command to set up the user credentials:  
```bash
kubectl --kubeconfig ~/.kube/config-anvesh config set-credentials anvesh --client-certificate=anvesh-user.crt --client-key=anvesh.pem --embed-certs=true
```
Replace anvesh-user.crt and anvesh.pem with the paths to your user certificate and private key files respectively.  

4. Set context information:  
Use the kubectl config set-context command to set up the context information:  
```bash
kubectl --kubeconfig ~/.kube/config-anvesh config set-context default --cluster=preprod --user=anvesh
```  

5. Use the context:  
Finally, use the kubectl config use-context command to use the newly created context:  
```bash
kubectl --kubeconfig ~/.kube/config-anvesh config use-context default
```
Now, your config-anvesh file is configured with the necessary cluster, user, and context information. You can use it with kubectl commands by passing --kubeconfig ~/.kube/config-anvesh. Make sure to replace placeholder values with your actual configuration details.   
Example:  
```bash 
kubectl --kubeconfig ~/.kube/config-anvesh get pods
```
We've successfully created a new user named "anvesh". However, when we try to access the pods using this user, we encounter a Forbidden error:   
```bash
$ kubectl --kubeconfig ~/.kube/config-anvesh get pods
Error from server (Forbidden): pods is forbidden: User "anvesh" cannot list resource "pods" in API group "" in the namespace "default"
```  
This error occurs because we haven't assigned any permissions to the "anvesh" user yet; we've only created the user.  