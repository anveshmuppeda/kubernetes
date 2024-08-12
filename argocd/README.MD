# Argo CD 

Argo CD, a declarative, GitOps continuous delivery tool for Kubernetes.

Source code can be found here:

* <https://github.com/argoproj/argo-helm/tree/main/charts/argo-cd>
* <https://github.com/argoproj/argo-cd>

## Installing Argo CD using the Helm Chart with custom values  

To install the chart with the release name `my-release`:  

```console
$ helm repo add argo https://argoproj.github.io/argo-helm
"argo" has been added to your repositories

$ helm install argocd-demo argo-cd/ -f argocd-custom-values.yaml  
NAME: my-release
...  
```


## Installing Argo CD using the Manifest Files  
```sh
kubectl create namespace argocd
kubectl apply -n argocd -f https://raw.githubusercontent.com/argoproj/argo-cd/stable/manifests/install.yaml
```  

## Troubleshoot 
```sh
$ helm install argocd-demo argo-cd/ -f argocd-custom-values.yaml
Error: INSTALLATION FAILED: An error occurred while checking for chart dependencies. You may need to run `helm dependency build` to fetch missing dependencies: found in Chart.yaml, but missing in charts/ directory: redis-ha
```  
If you face above issue follow the below steps to resolve it: 
1. Add the dandydevelope chart using the below command:
```sh
helm repo add dandy https://dandydeveloper.github.io/charts/
```
2. Run the following command to fetch the missing dependencies: 
```sh
helm dependency build argo-cd
```
3. Extract the redis-ha chart using the below command under sub charts section. 
```sh
tar -ztvf redis-ha-4.26.1.tgz
```  
3. Then proceed with the installation of the argocd helm chart.  

