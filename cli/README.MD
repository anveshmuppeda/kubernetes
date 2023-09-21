# Install CLIs for Kuberntes environment.
## kubectl
Download the linux OS based package. 

```
curl -LO https://storage.googleapis.com/kubernetes-release/release/$(curl -s https://storage.googleapis.com/kubernetes-release/release/stable.txt)/bin/linux/amd64/kubectl

OR

curl -LO https://storage.googleapis.com/kubernetes-release/release/v1.23.6/bin/linux/amd64/kubectl
```

Add executable permissions to kubectl  
```
chmod +x kubectl
```

Move kubectl to the /usr/local/bin/  
```
sudo mv kubectl /usr/local/bin/
```
---

## Helm

To install helm with version 3.8.2
```
curl -L https://git.io/get_helm.sh | bash -s -- --version v3.8.2
```
