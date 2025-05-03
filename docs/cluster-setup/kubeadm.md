---
// filepath: /Users/anveshmuppeda/Desktop/anvesh/tech/git/kubernetes/docs/cluster-setup/kubeadm.md
sidebar_position: 2
sidebar_label: "Kubeadm Cluster Setup"
---  

## Step-by-Step Guide: Setting Up a Kubernetes Cluster on AWS EC2 Using kubeadm

This guide demonstrates how to set up a Kubernetes cluster with one control plane and one worker node on AWS EC2 instances. It covers EC2 instance configuration, Kubernetes installation, and deploying a sample application.

![Kubernetes Cluster Setup](./../../assets/kubeadm-cluster-setup.png)
### Introduction  
Kubernetes has become the backbone of modern container orchestration, making it essential for developers and system administrators alike. Setting up a Kubernetes cluster can seem daunting, but with tools like kubeadm, it's more straightforward than ever.

In this guide, we'll walk you through creating a Kubernetes cluster on AWS EC2 using Amazon Linux 2, kubeadm, Docker, and Calico. We'll also tackle common errors and debugging tips to ensure a smooth setup.

---

### **1. Launch EC2 Instances**

1. **Launch Two EC2 Instances:**
   - **Control Plane Node**: Manages the Kubernetes cluster.
   - **Worker Node**: Hosts application workloads.

2. **Create Security Groups with the Following Rules:**

#### **Control Plane Security Group**
| Protocol | Direction | Port Range  | Purpose                      |
|----------|-----------|-------------|------------------------------|
| TCP      | Inbound   | 6443        | Kubernetes API Server        |
| TCP      | Inbound   | 2379-2380   | etcd client API              |
| TCP      | Inbound   | 10250       | Kubelet API                  |
| TCP      | Inbound   | 10259       | kube-scheduler               |
| TCP      | Inbound   | 10257       | kube-controller-manager      |

#### **Worker Node Security Group**
| Protocol | Direction | Port Range  | Purpose                      |
|----------|-----------|-------------|------------------------------|
| TCP      | Inbound   | 10250       | Kubelet API                  |
| TCP      | Inbound   | 10256       | kube-proxy                   |
| TCP      | Inbound   | 30000-32767 | NodePort Services            |

---

### **2. Set Up the Control Plane Node**

1. **SSH Into the Instance**:
   ```bash
   ssh -i k8s-key.pem ec2-user@<control-plane-public-ip>
   sudo su
   ```

2. **Update the System**:
   ```bash
   yum update -y
   ```

3. **Install Docker**:
   ```bash
   yum install -y docker
   systemctl enable --now docker
   ```

4. **Disable SELinux**:
   ```bash
   setenforce 0
   sed -i 's/^SELINUX=enforcing$/SELINUX=permissive/' /etc/selinux/config
   ```

5. **Add Kubernetes Repository**:
   ```bash
   cat <<EOF | tee /etc/yum.repos.d/kubernetes.repo
   [kubernetes]
   name=Kubernetes
   baseurl=https://pkgs.k8s.io/core:/stable:/v1.29/rpm/
   enabled=1
   gpgcheck=1
   gpgkey=https://pkgs.k8s.io/core:/stable:/v1.29/rpm/repodata/repomd.xml.key
   exclude=kubelet kubeadm kubectl cri-tools kubernetes-cni
   EOF
   ```

6. **Install Kubernetes Components**:
   ```bash
   yum install -y kubelet kubeadm kubectl --disableexcludes=kubernetes
   systemctl enable --now kubelet
   ```

7. **Initialize the Control Plane**:
   ```bash
   kubeadm init --apiserver-advertise-address=<private-ip-of-control-plane> --pod-network-cidr=192.168.0.0/16
   ```

   Save the output of this command, which includes a `kubeadm join` command for adding worker nodes.

8. **Configure kubectl for the Admin User**:
   ```bash
   mkdir -p $HOME/.kube
   cp -i /etc/kubernetes/admin.conf $HOME/.kube/config
   chown $(id -u):$(id -g) $HOME/.kube/config
   ```

9. **Verify the Control Plane Node**:
   ```bash
   kubectl get nodes
   ```

   The control plane node will be in a `NotReady` state until the network plugin is installed.

---

### **3. Set Up the Worker Node**

1. **SSH Into the Worker Node**:
   ```bash
   ssh -i k8s-key.pem ec2-user@<worker-node-public-ip>
   sudo su
   ```

2. **Update the System**:
   ```bash
   yum update -y
   ```

3. **Install Docker**:
   ```bash
   yum install -y docker
   systemctl enable --now docker
   ```

4. **Disable SELinux**:
   ```bash
   setenforce 0
   sed -i 's/^SELINUX=enforcing$/SELINUX=permissive/' /etc/selinux/config
   ```

5. **Add Kubernetes Repository**:
   Repeat the same steps as for the control plane node to add the Kubernetes repository.

6. **Install Kubernetes Components**:
   ```bash
   yum install -y kubelet kubeadm kubectl --disableexcludes=kubernetes
   systemctl enable --now kubelet
   ```

7. **Join the Worker Node to the Cluster**:
   Use the `kubeadm join` command from the control plane initialization step:
   ```bash
   kubeadm join <control-plane-private-ip>:6443 --token <token> --discovery-token-ca-cert-hash sha256:<hash>
   ```

8. **Verify the Worker Node is Joined**:
   SSH back into the control plane node and run:
   ```bash
   kubectl get nodes
   ```

   The worker node will appear but may still show as `NotReady`.

---

### **4. Install a Network Plugin**

1. **Download and Apply Calico**:
   ```bash
   curl -O https://raw.githubusercontent.com/projectcalico/calico/v3.29.0/manifests/calico.yaml
   kubectl apply -f calico.yaml
   ```

2. **Verify the Nodes**:
   Wait a few seconds and check the node statuses:
   ```bash
   kubectl get nodes
   ```

   Both nodes should now show `Ready`.

---

### **5. Deploy a Sample Application**

1. **Create an Nginx Pod**:
   ```bash
   kubectl create deployment nginx --image=nginx
   kubectl expose deployment nginx --type=NodePort --port=80
   ```

2. **Access the Application**:
   Retrieve the NodePort of the service:
   ```bash
   kubectl get svc nginx
   ```

   Access the application using the control plane's public IP and the NodePort:
   ```
   http://<control-plane-public-ip>:<NodePort>
   ```

---

### **Conclusion**

By following this guide, you have successfully set up a Kubernetes cluster on AWS EC2 instances. You can now use the cluster to deploy and manage containerized applications. For further information, refer to the [official Kubernetes documentation](https://kubernetes.io/docs/home/).  

---

### **References**

- [Install kubeadm](https://kubernetes.io/docs/setup/production-environment/tools/kubeadm/install-kubeadm/)
- [Create a cluster with kubeadm](https://v1-29.docs.kubernetes.io/docs/setup/production-environment/tools/kubeadm/create-cluster-kubeadm/)
- [Install Docker as a container runtime](https://kubernetes.io/docs/setup/production-environment/container-runtimes/#docker)
- [Install Calico for networking](https://docs.tigera.io/calico/latest/getting-started/kubernetes/self-managed-onprem/onpremises#install-calico-with-kubernetes-api-datastore-50-nodes-or-less)

---

### Debug Guide: Resolving Common Kubernetes Installation Issues on AWS EC2

When setting up Kubernetes on AWS EC2, you may encounter several challenges. Below is a guide to troubleshooting and resolving common issues, using your experience as an example.

---

### **1. Issue: Dependency Resolution Error During Kubernetes Installation**

#### **Symptom**
While installing Kubernetes components (`kubelet`, `kubeadm`, `kubectl`), the following error occurs:

```plaintext
Error: Package: kubeadm-1.31.2-150500.1.1.x86_64 (kubernetes)
           Requires: cri-tools >= 1.30.0
```

#### **Root Cause**
The `cri-tools` package version in the Amazon Linux 2 repository is outdated or incompatible with the Kubernetes version you are installing.

#### **Resolution Steps**
1. **Check Available Versions of cri-tools**:
   ```bash
   yum list available cri-tools
   ```

   Identify a version of `cri-tools` that satisfies the dependency.

2. **Install the Compatible Version**:
   ```bash
   yum install -y cri-tools
   ```

   If this fails, you may install an alternative compatible runtime like CRI-O:
   ```bash
   yum install -y cri-o cri-tools
   ```

3. **Retry Installing Kubernetes**:
   After resolving the dependency, rerun:
   ```bash
   yum install -y kubelet kubeadm kubectl --disableexcludes=kubernetes
   ```

4. **Verification**:
   Ensure all required components are installed:
   ```bash
   kubeadm version
   kubectl version --client
   kubelet --version
   ```

---

### **2. Issue: Nodes Show `NotReady` State**

#### **Symptom**
After joining the cluster, the nodes show `NotReady` when running:
```bash
kubectl get nodes
```

#### **Root Cause**
This usually occurs due to a missing or misconfigured network plugin (CNI).

#### **Resolution Steps**
1. **Install a Network Plugin**:
   Install Calico as an example:
   ```bash
   curl -O https://raw.githubusercontent.com/projectcalico/calico/v3.29.0/manifests/calico.yaml
   kubectl apply -f calico.yaml
   ```

2. **Verify Node Status**:
   Check again after a few minutes:
   ```bash
   kubectl get nodes
   ```

3. **Check Pod Logs for Issues**:
   ```bash
   kubectl logs -n kube-system <pod-name>
   ```

---

### **3. Issue: kubeadm Join Command Fails**

#### **Symptom**
Running `kubeadm join` on the worker node results in an error such as:
```plaintext
[ERROR] unable to connect to the API server
```

#### **Root Cause**
- Network connectivity between the worker and control plane nodes is blocked.
- The token or CA certificate hash is incorrect.

#### **Resolution Steps**
1. **Verify Control Plane Reachability**:
   Ensure the worker node can reach the control plane:
   ```bash
   telnet <control-plane-private-ip> 6443
   ```

2. **Ensure Security Group Configuration**:
   Update the security group for the control plane to allow traffic on port `6443` from the worker node.

3. **Regenerate the Token if Needed**:
   If the token has expired, generate a new one on the control plane:
   ```bash
   kubeadm token create --print-join-command
   ```

4. **Retry the Join Command**:
   Run the updated `kubeadm join` command on the worker node.

---

### **4. Issue: Docker Installation Issues**

#### **Symptom**
Docker fails to start, or commands like `docker ps` do not work.

#### **Root Cause**
Docker may not be properly installed, or the `docker` service is not running.

#### **Resolution Steps**
1. **Reinstall Docker**:
   ```bash
   yum remove -y docker
   yum install -y docker
   ```

2. **Start and Enable Docker**:
   ```bash
   systemctl start docker
   systemctl enable docker
   ```

3. **Verify Installation**:
   ```bash
   docker --version
   ```

4. **Test Docker**:
   Run a test container:
   ```bash
   docker run hello-world
   ```

---

### **5. Issue: kubelet Service Fails to Start**

#### **Symptom**
The `kubelet` service fails with an error:
```plaintext
Failed to start kubelet: Misconfiguration
```

#### **Root Cause**
- Incomplete configuration in `/etc/kubernetes/kubelet.conf`.
- Missing network plugin.

#### **Resolution Steps**
1. **Check Logs**:
   ```bash
   journalctl -xeu kubelet
   ```

2. **Restart kubelet**:
   After fixing the configuration:
   ```bash
   systemctl restart kubelet
   ```

3. **Verify Status**:
   ```bash
   systemctl status kubelet
   ```

---

### **6. General Debugging Tools**

1. **Check Kubernetes Logs**:
   ```bash
   kubectl logs -n kube-system <pod-name>
   ```

2. **Verify Pod and Service States**:
   ```bash
   kubectl get pods -A
   kubectl get svc -A
   ```

3. **Inspect Events for Errors**:
   ```bash
   kubectl describe nodes
   kubectl describe pods -n kube-system
   ```

4. **Use cURL to Test API Server**:
   Ensure the API server is reachable:
   ```bash
   curl -k https://<control-plane-private-ip>:6443/version
   ```

---

### **Conclusion**
This debug guide provides solutions to common Kubernetes installation issues, such as dependency errors, node readiness problems, and network connectivity. Always refer to the Kubernetes documentation for more details:
- [Install kubeadm](https://kubernetes.io/docs/setup/production-environment/tools/kubeadm/install-kubeadm/)
- [Network Plugins](https://kubernetes.io/docs/concepts/cluster-administration/addons/)