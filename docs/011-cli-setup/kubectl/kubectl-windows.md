# Install and Set Up kubectl with Chocolatey on Windows  
### 1. Install kubectl  
```bash  
    choco install kubernetes-cli
```  
### 2. Test to ensure the version you installed is up-to-date  
```bash 
    kubectl version --client
```  

### 3. Navigate to your home directory  
```bash
    # If you're using cmd.exe, run: cd %USERPROFILE%
    cd ~
```

### 4. Create the `.kube` directory 
```bash
    mkdir .kube
```

### 5. Change to the `.kube` directory you just created  
```bash
    cd .kube
```

### 6. Configure kubectl to use a remote Kubernetes cluster  
```bash
    New-Item config -type file 
``` 

### Reference:  
#### https://kubernetes.io/docs/tasks/tools/  