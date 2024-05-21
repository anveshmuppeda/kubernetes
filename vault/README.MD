# Vault in Kubernetes  

## Create Vault Secret   
```
kubectl create ns vault
```  

## Install Vault  
Let's install latest version of vault using a helm chart   

#### Add the Hashicorp helm repository   
```bash
$ helm repo add hashicorp https://helm.releases.hashicorp.com
"hashicorp" has been added to your repositories
```  

We can install in two ways
#### 1. Directly running helm install using artifact hub helm repo.  
#### 2. By downloading the helm chart and install.

### 1. Directly running helm install using artifact hub helm repo. 
```bash
helm install vault hashicorp/vault \
       --set='server.dev.enabled=true' \
       --set='server.ui.enabled=true' \
       --set='server.ui.serviceType=LoadBalancer' \
       --namespace vault
```

### 2. By downloading the helm chart and install.  
```bash
helm install vault \
       --set='server.dev.enabled=true' \
       --set='server.ui.enabled=true' \
       --set='server.ui.serviceType=LoadBalancer' \
       --namespace vault \
       ./vault-chart 
```  

Using the above fields we are installing the vault in dev mode and enabling the UI to access the vault to create the secrets. 

## Configure Vault  
Connect to the vault pod:  
```bash
kubectl exec -it vault-0 /bin/sh
```  

Next, lets configure a policy that we can then attach a role to (used for accessing secrets from a Kubernetes service account).  

```bash
cat <<EOF > /home/vault/app-policy.hcl
path "secret*" {
  capabilities = ["read"]
}
EOF
```

Then, lets apply the policy.   

```bash
vault policy write app /home/vault/app-policy.hcl
```  

Next, enable the kubernetes auth method.  
```bash
vault auth enable kubernetes
```  

Next, lets configure the kubernetes auth method, so it can communicate with Kubernetes.  
```bash
vault write auth/kubernetes/config \
   token_reviewer_jwt="$(cat /var/run/secrets/kubernetes.io/serviceaccount/token)" \
   kubernetes_host=https://${KUBERNETES_PORT_443_TCP_ADDR}:443 \
   kubernetes_ca_cert=@/var/run/secrets/kubernetes.io/serviceaccount/ca.crt
```

Next, lets connect the policy we created earlier to a myapp role. This will be used in a minute when we create our Kubernetes service account for our demo apps so they are allowed to pull down secrets from Vault.  

```bash
vault write auth/kubernetes/role/myapp \
   bound_service_account_names=app \
   bound_service_account_namespaces=demo \
   policies=app \
   ttl=1h  
```

Next, lets create some secrets.  
```bash
vault kv put secret/login username=anvesh password=anveshpassword
```  

You can list the secrets by running vault kv list secret.  

```bash
Keys
----
login
```   




