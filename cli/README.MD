# Install CLIs for Kuberntes environment.
## kubectl
Download the linux OS based package. 

```
curl -LO https://storage.googleapis.com/kubernetes-release/release/$(curl -s https://storage.googleapis.com/kubernetes-release/release/stable.txt)/bin/linux/amd64/kubectl
```

Add executable permissions to kubectl  
```
chmod +x kubectl
```

Move kubectl to the /usr/local/bin/  
```
sudo mv kubectl /usr/local/bin/
```
