# Installing Helm with apt & script on Linux  

## From Script  
### 1. Download the script  
```bash 
    curl -fsSL -o get_helm.sh https://raw.githubusercontent.com/helm/helm/main/scripts/get-helm-3
``` 

### 2. Update the permissions of the script  
```bash 
    chmod 700 get_helm.sh
```  

### 3. Execute the script  
```bash 
    ./get_helm.sh
```  

> [!NOTE]
> Yes, you can curl https://raw.githubusercontent.com/helm/helm/main/scripts/get-helm-3 | bash if you want to live on the edge.  

## From Apt (Debian/Ubuntu)  
### 1. Install helm 
```bash
curl https://baltocdn.com/helm/signing.asc | gpg --dearmor | sudo tee /usr/share/keyrings/helm.gpg > /dev/null
sudo apt-get install apt-transport-https --yes
echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/helm.gpg] https://baltocdn.com/helm/stable/debian/ all main" | sudo tee /etc/apt/sources.list.d/helm-stable-debian.list
sudo apt-get update
sudo apt-get install helm
```

### Reference:  
#### https://helm.sh/docs/intro/install/  
