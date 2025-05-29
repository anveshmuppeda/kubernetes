# ⎈ Azure DevOps — Self Hosted Agents on Kubernetes — PART-5 ⎈
#### *Deploy Linux, Windows, DinD Self-Hosted Agents using Helm Charts 🐳*

![img](./img/helm-charts.png.gif)

Welcome to Part-5.
 In our journey towards optimizing our CI/CD workflows, we’ve explored setting up Linux, Windows, and Docker-in-Docker (DinD) self-hosted agents, integrating them into Kubernetes, and ensuring seamless connections with Azure DevOps. However, managing these agents individually through manifest files can become cumbersome in real-world projects. To streamline this process, we’re introducing Helm charts for deploying these agents.
### Introducing Helm Charts
Helm charts offer a convenient way to manage the deployment of complex applications and services on Kubernetes. By encapsulating the configuration details into reusable templates, Helm charts simplify the deployment process and enable better control over various components.

### Helm Chart Structure

```yaml
az-selfhosted-agents/
  ├── charts/
  ├── templates/
  │   ├── dind-deploy.yaml
  │   ├── windows-deploy.yaml
  │   ├── linux-deploy.yaml
  │   ├── secret.yaml
  │   ├── sysbox-install.yaml
  │   ├── _helpers.tpl
  ├── values.yaml
  ├── .helmignore
  ├── Chart.yaml
  ├── LICENSE
  └── README.md
```

In our Helm chart, we’ve consolidated the deployment manifest files for all three types of agents(Linux, Windows, and DinD) along with the necessary configurations for secrets and Sysbox setup.

### Deploying Agents with Helm Charts 

In this part, we’ll deploy Linux, Windows, and DinD agents using a single Helm chart. The flexibility of Helm allows us to selectively install or skip specific Self-Hosted Agents based on our project requirements.

By default, all three types of agents (Linux, Windows, and DinD) are disabled in the Helm chart. To install specific agents, we can use the following command:


Example: Linux

```yaml
helm install az-selfhosted-agents ./az-selfhosted-agents \
 --set linux.enabled=true \
 --create-namespace -n az-devops
```
This command creates a new namespace az-devops and installs the specified agents i.e., Linux Agent.

Alternatively, if you want to install all agents, you can use the following command:

```yaml
helm install az-selfhosted-agents ./az-selfhosted-agents \
 --set windows.enabled=true \
 --set linux.enabled=true \
 --set dind.enabled=true \
 --create-namespace -n az-devops
```

## Conclusion
With Helm charts, managing the deployment of self-hosted agents becomes more efficient and scalable. By leveraging Helm’s capabilities, we can easily configure and deploy agents according to our project requirements, simplifying the CI/CD pipeline setup process.
