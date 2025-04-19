# FluxCD  

Install the Flux CLI
The Flux CLI is available as a binary executable for all major platforms, the binaries can be downloaded from GitHub releases page.

With Homebrew for macOS and Linux:
brew install fluxcd/tap/flux

With Bash for macOS and Linux:
curl -s https://fluxcd.io/install.sh | sudo bash

Now we can run flux --help to see its installed

Check our cluster
flux check --pre

> flux check --pre
► checking prerequisites
✔ Kubernetes 1.30.11 >=1.30.0-0
✔ prerequisites checks passed


Get Started with Flux
This tutorial shows you how to bootstrap Flux to a Kubernetes cluster and deploy a sample application in a GitOps manner.

Before you begin
To follow the guide, you need the following:

A Kubernetes cluster. We recommend Kubernetes kind for trying Flux out in a local development environment.
A GitHub personal access token with repo permissions. See the GitHub documentation on creating a personal access token.
Note that for production use, it is recommended to have a dedicated GitHub account for Flux and use fine-grained access tokens with the minimum required permissions.



Objectives
Bootstrap Flux on a Kubernetes Cluster.
Deploy a sample application using Flux.
Customize application configuration through Kustomize patches.


Export your credentials
Export your GitHub personal access token:

export GITHUB_TOKEN=<your-token>


Install Flux onto your cluster
For information on how to bootstrap using a GitHub org, Gitlab and other git providers, see Bootstrapping.

Run the bootstrap command:
flux bootstrap github \
  --owner=anveshmuppeda \
  --repository=kubernetes \
  --branch=fluxcd \
  --path=./fluxcd/repos/infra-repo/clusters/dev \
  --personal

> flux check
► checking prerequisites
✔ Kubernetes 1.30.11-eks-bcf3d70 >=1.30.0-0
► checking version in cluster
✔ distribution: flux-v2.5.1
✔ bootstrapped: true
► checking controllers
✔ helm-controller: deployment ready
► ghcr.io/fluxcd/helm-controller:v1.2.0
✔ kustomize-controller: deployment ready
► ghcr.io/fluxcd/kustomize-controller:v1.5.1
✔ notification-controller: deployment ready
► ghcr.io/fluxcd/notification-controller:v1.5.0
✔ source-controller: deployment ready
► ghcr.io/fluxcd/source-controller:v1.5.0
► checking crds
✔ alerts.notification.toolkit.fluxcd.io/v1beta3
✔ buckets.source.toolkit.fluxcd.io/v1
✔ gitrepositories.source.toolkit.fluxcd.io/v1
✔ helmcharts.source.toolkit.fluxcd.io/v1
✔ helmreleases.helm.toolkit.fluxcd.io/v2
✔ helmrepositories.source.toolkit.fluxcd.io/v1
✔ kustomizations.kustomize.toolkit.fluxcd.io/v1
✔ ocirepositories.source.toolkit.fluxcd.io/v1beta2
✔ providers.notification.toolkit.fluxcd.io/v1beta3
✔ receivers.notification.toolkit.fluxcd.io/v1
✔ all checks passed
> kubectl -n flux-system get GitRepository
kubectl -n flux-system get Kustomization
NAME          URL                                             AGE    READY   STATUS
flux-system   ssh://git@github.com/anveshmuppeda/kubernetes   5m3s   True    stored artifact for revision 'fluxcd@sha1:d21d876dca90685dfcbfb8546f73710f1ec9b2f2'
NAME          AGE    READY   STATUS
flux-system   5m4s   True    Applied revision: fluxcd@sha1:d21d876dca90685dfcbfb8546f73710f1ec9b2f2


Understanding GitOps Repository structures
Generally, in GitOps you have a dedicated repo for infrastructure templates.


Example structure (kustomize overlays):

```bash
├── apps
│   ├── base
│   ├── production 
│   └── staging
├── infrastructure
│   ├── base
│   ├── production 
│   └── staging
└── clusters
    ├── production
    └── staging
```

Each cluster state is defined in a dedicated dir e.g. clusters/production where the specific apps and infrastructure overlays are referenced.

So in my case my structure like below 

```
```

So now all the requirements are ready now let's start with our actual exmaple 
lets build app1 from the repos/app1/ diretory

# go to our "git repo"
cd fluxcd/repos/app1
# check the files
ls

Login to dockerhub or any other repo:
docker login -u <username>

cd src
docker build . -t fluxcd-demo-app1:v1.0.0

tag image
docker tag fluxcd-demo-app1:v1.0.0 anvesh35/fluxcd-demo-app1:v1.0.0

Push image to docker hub 
docker push anvesh35/fluxcd-demo-app1:v1.0.0

Create namespace fluxcd-demo
> k create ns fluxcd-demo
namespace/fluxcd-demo created

# check deployed resources
kubectl -n fluxcd-demo get all

kubectl -n fluxcd-demo port-forward svc/app1 80:80


Now I am able to see the app with version v1.0.0

Now let's try to update the version of the app to v2.0.0 by updating the source code and build docker image with new version 

cd src
docker build . -t fluxcd-demo-app1:v2.0.0

tag image
docker tag fluxcd-demo-app1:v2.0.0 anvesh35/fluxcd-demo-app1:v2.0.0

Push image to docker hub 
docker push anvesh35/fluxcd-demo-app1:v2.0.0

Now update our kubernetes deployment YAML image tag under /fluxcd/repos/app1/app1-deployment.yaml 

Then git commit  & git push to fluxcd branch!

Now check the pods status 
# check deployed resources
kubectl -n fluxcd-demo get all

kubectl -n fluxcd-demo port-forward svc/app1 80:80

we can latest version pods are now deployed to cluster 
and you can see the latest version on the app.

Even I have automated above docker build and updating the manifest files step using below steps:

Here's a concise step-by-step explanation :

### CI/CD Workflow Steps

1. **Trigger Conditions**:
   - Runs when code is pushed to `main` or `fluxcd` branches
   - Also runs when new version tags (`v*`) are created

2. **Build Process**:
   - Checks out the repository code
   - Determines version:
     - Uses tag name for version tags (e.g., `v1.0.0`)
     - Uses first 8 characters of commit SHA for branch pushes
   - Builds Docker image from:
     ```
     fluxcd/repos/app1/src/Dockerfile
     ```
   - Tags image with format: `anvesh35/fluxcd-demo-app1:<version>`
   - Pushes image to Docker Hub

3. **Manifest Update**:
   - Updates deployment YAML with new image tag:
     ```
     fluxcd/repos/app1/deploy/app1-deployment.yaml
     ```
   - Commits the change to `fluxcd` branch with message:
     ```
     "Update image to <version>"
     ```

4. **Required Setup**:
   - Repository secrets needed:
     - `DOCKERHUB_USERNAME` - Your Docker Hub username
     - `DOCKERHUB_TOKEN` - Docker Hub access token
   - Repository permissions:
     - GitHub Actions must have write permissions
     - Branch protection rules must allow Actions to push to `fluxcd` branch

5. **Directory Structure**:
   ```
   /fluxcd/repos/app1/
     ├── src/
     │   └── Dockerfile      # Source Dockerfile
     └── deploy/
         └── app1-deployment.yaml  # Deployment manifest
   ```

This workflow automatically keeps your deployment manifests synchronized with your built images, pushing all changes to the `fluxcd` branch where Flux can detect and apply them.




