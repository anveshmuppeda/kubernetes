---
// filepath: kubernetes/docs/cluster-setup/minikube.md
sidebar_position: 3
sidebar_label: "Minikube Cluster Setup"
---  

# 🐳 Getting Started with Minikube  
### Spin up a local Kubernetes cluster in one command

Minikube makes it super easy to run Kubernetes locally by spinning up a single‑node cluster inside a Docker container or VM. Perfect for learning, development, and testing!

---

## 📋 Prerequisites

Before you start, make sure you have:

- **2 CPUs** or more  
- **2 GB RAM** minimum free memory  
- **20 GB disk** free space  
- **Internet connection**  
- A container or VM driver, e.g.:  
  - Docker  
  - Podman  
  - VirtualBox  
  - Hyperkit (macOS)  
  - Hyper‑V (Windows)  
  - KVM/QEMU (Linux)  

---

## 1️⃣ Install Minikube

Choose your platform:

### macOS (Homebrew)

```bash
brew install minikube
```

If you have an old binary linked, run:

```bash
brew unlink minikube
brew link   minikube
```

### Linux (binary download)

```bash
curl -Lo minikube https://storage.googleapis.com/minikube/releases/latest/minikube-linux-amd64
chmod +x minikube
sudo mv minikube /usr/local/bin/
```

### Windows (PowerShell)

```powershell
curl.exe -Lo minikube.exe https://storage.googleapis.com/minikube/releases/latest/minikube-windows-amd64.exe
Move-Item .\minikube.exe C:\tools\minikube.exe
```

For other installers or architectures, see the [official releases page](https://github.com/kubernetes/minikube/releases).

---

## 2️⃣ Start Your Cluster

From a terminal (with permissions to run Docker or your chosen driver), simply run:

```bash
minikube start
```

Minikube will:

1. Download the latest Kubernetes ISO.  
2. Launch a container or VM for the control plane.  
3. Configure your `kubectl` context automatically.

> **Tip:** If you have multiple VM/driver options installed, you can specify one:  
> ```bash
> minikube start --driver=virtualbox
> ```

---

## 3️⃣ Interact with Kubernetes

Use your existing `kubectl` (or let Minikube download one for you):

```bash
# If you have kubectl:
kubectl get po -A

# Or via Minikube’s bundled kubectl:
minikube kubectl -- get po -A

# Make life easier—add an alias:
alias kubectl="minikube kubectl --"
```

Check cluster status with:

```bash
minikube status
```

---

## 4️⃣ Deploy a Sample App

Create and expose a simple HTTP server:

```bash
kubectl create deployment hello-minikube --image=kicbase/echo-server:1.0
kubectl expose deployment hello-minikube --type=NodePort --port=8080
kubectl get svc hello-minikube
```

Open it in your browser:

```bash
minikube service hello-minikube
```

Or forward a port:

```bash
kubectl port-forward service/hello-minikube 7080:8080
# Visit http://localhost:7080
```

---

## 5️⃣ Explore the Dashboard

Minikube bundles the official Kubernetes Dashboard:

```bash
minikube dashboard
```

A browser tab will open so you can view workloads, logs, and more.

---

## 6️⃣ Advanced Management

- **Pause / Unpause cluster**  
  ```bash
  minikube pause
  minikube unpause
  ```
- **Stop / Delete cluster**  
  ```bash
  minikube stop
  minikube delete
  ```
- **Change default resource limits**  
  ```bash
  minikube config set memory 4GB
  minikube config set cpus   4
  ```
- **Browse addons catalog**  
  ```bash
  minikube addons list
  ```
- **Run older Kubernetes versions**  
  ```bash
  minikube start -p old-cluster --kubernetes-version=v1.16.1
  ```

---

## 🚀 Next Steps

- Try out different [Minikube addons](https://minikube.sigs.k8s.io/docs/handbook/addons/).  
- Build & test your own Kubernetes manifests and Helm charts.  
- Automate cluster creation in CI by scripting `minikube start` and `minikube delete`.

---  

## References

- [Minikube start](https://minikube.sigs.k8s.io/docs/start/?arch=%2Fmacos%2Fx86-64%2Fstable%2Fhomebrew)

Happy local k8s hacking! 🐳✨  
```