# Install kubectl binary with curl on Linux  
### 1. Download the latest release with the command  
```bash
    curl -LO "https://dl.k8s.io/release/$(curl -L -s https://dl.k8s.io/release/stable.txt)/bin/linux/amd64/kubectl"
```  
### 2. Download the kubectl checksum file  
```bash 
   curl -LO "https://dl.k8s.io/release/$(curl -L -s https://dl.k8s.io/release/stable.txt)/bin/linux/amd64/kubectl.sha256"
``` 
 > [!NOTE]
 > Note: Download the same version of the binary and checksum.  

### 3. Install kubectl 
```bash
    sudo install -o root -g root -m 0755 kubectl /usr/local/bin/kubectl
```  

### 4. Test to ensure the version you installed is up-to-date  
```bash 
    kubectl version --client --output=yaml
```


### Reference:  
#### https://kubernetes.io/docs/tasks/tools/  