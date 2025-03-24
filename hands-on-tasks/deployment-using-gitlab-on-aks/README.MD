### In this simple example we will learn how we deploy a simple a simple nginx server on aks cluster

### Prerequisites
#### **GitLab Project: Create a GitLab project to store your code and CI/CD configuration.** 
#### AKS Cluster: Ensure you have an AKS cluster set up and accessible. 
#### Docker: Install Docker locally to build the Nginx image. 
#### kubectl: Install and configure kubectl to interact with your AKS cluster.
#### Container Registry: You'll need a container registry (like Azure Container Registry) to store the Nginx image.
In this example fisrtly you have to create a simple aks cluster with resource group after creating the cluster you need to create a gitlab project in that gitlab project you push your code and create .gitlab-ci.yaml file and configure the pipeline, in this demo the file which i created has two stages only build and deploy ,in the build stage i give the user credintial to my docker registry to push the image i use docker image to run docker commands (docker client and docker deamon configured using that image) ,in the deploy stage you need to give your cluster credintials (kubeconfig file) and in the scripts section you need to run ```kubectl create dployment``` to create deployment.


####  step 1:  Get Cluster Credentials
run :
```bash
az aks get-credentials --resource-group myResourceGroup --name myAKSCluster
```
This allows kubectl to access the cluster

####  step 2: Configure GitLab CI/CD 

### Add Variables: In your GitLab project settings, add the following variables:
1. CI_REGISTRY_USER: Your container registry username. 
2. CI_REGISTRY_PASSWORD: Your container registry password. 
3. CI_REGISTRY_IMAGE: Your container registry image path (e.g., your_registry/your_project). 
4. KUBECONFIG: The content of your kubeconfig file (base64 encoded). 
5. KUBECONFIG_CONTEXT: The context of your AKS cluster(you created before) in the kubeconfig file. 

####  step 3: push your code and trigger pipeline 
  1. Push your code (including the Dockerfile, .gitlab-ci.yml, and deployment.yaml) to your GitLab project.
  2. The pipeline will automatically trigger and build, push, and deploy the Nginx image to your AKS cluster. 

####  step 3: verify and check 
  run this on cloudshell to check if the nginx server is deployed or not:
  ```bash
  kubectl get deployment
  ```  
this will return the created deployment
