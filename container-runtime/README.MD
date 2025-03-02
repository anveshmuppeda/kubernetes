# **Building a Container Runtime from Scratch Using `chroot`**  
*Learn how Docker works under the hood by creating a minimalist runtime called **MiniDocker**.*  

---

## **Table of Contents**  
1. [Introduction](#introduction)  
2. [Docker Runtimes Explained Simply](#docker-runtimes-explained-simply)  
3. [Understanding `chroot`](#understanding-chroot)  
4. [Hands-On Guide with MiniDocker](#hands-on-guide-with-minidocker)  
   - [Step 1: Pull and Extract NGINX Files](#step-1-pull-and-extract-nginx-files)  
   - [Step 2: Fix Missing System Files](#step-2-fix-missing-system-files)  
   - [Step 3: Run NGINX in a `chroot` Jail](#step-3-run-nginx-in-a-chroot-jail)  
   - [Step 4: Check if NGINX Is Running](#step-4-check-if-nginx-is-running)  
   - [Step 5: Check Which Port NGINX Is Using](#step-5-check-which-port-nginx-is-using)  
   - [Step 6: Check Which Filesystem NGINX Is Using](#step-6-check-which-filesystem-nginx-is-using)  
   - [Step 7: Connect to New Filesystem and Run Some Basic Commands](#step-7-connect-to-new-filesystem-and-run-some-basic-commands)  
   - [Step 8: Stop the NGINX Service](#step-8-stop-the-nginx-service)  
5. [Create MiniDocker](#create-minidocker)  
   - [Step 1: Create MiniDocker (Go Program)](#step-1-create-minidocker-go-program)  
   - [Step 2: Build MiniDocker (Go Program)](#step-2-build-minidocker)  
   - [Step 3: Pull Image Using MiniDocker](#step-3-pull-image-using-minidocker)  
   - [Step 4: Run Image Using MiniDocker](#step-4-run-image-using-minidocker)  
5. [Limitations](#limitations)  
6. [Conclusion](#conclusion)  
7. [Appendix](#appendix)  

---

## **1. Introduction**  
Docker has revolutionized software development, but its core concepts are often misunderstood. In this guide, we’ll demystify containers by building **MiniDocker**, a minimalist runtime using `chroot`, and explain how Docker itself works under the hood.

---

## **2. Docker Runtimes Explained Simply**  
Docker uses three key components to run containers:  

1. **Containerd**: Manages container lifecycle (start/stop/delete).  
2. **Runc**: Creates containers using Linux features like `chroot`, namespaces, and cgroups.  
3. **OverlayFS**: Layers filesystems for efficient image storage.  

### **Analogy**:  
- **Docker Image**: A blueprint (e.g., NGINX with config files).  
- **Docker Container**: A house built from the blueprint.  
- **Runc**: The construction crew that builds the house.  
- **`chroot`**: The fence around the house (filesystem isolation).  

---

## **3. Understanding `chroot`**  
`chroot` ("change root") locks a process into a directory, making it think that directory is the **entire filesystem**.  

#### **Example**:  
- **Host Filesystem**:  
  ```
  /home
  /etc
  /usr
  ```  
- **After `chroot` to `/jail`**:  
  ```
  /jail   <-- New root ("/")
    ├── bin
    └── etc  
  ```  
The process can’t see anything outside `/jail`!  

---

## **4. Hands-On Guide with MiniDocker**  
### **Step 1: Pull and Extract NGINX Files**  
1. **Pull the NGINX image**:  
   ```bash
   docker pull nginx
   ```  

2. **Export its filesystem**:  
   ```bash
   docker create --name nginx-container nginx
   docker export nginx-container -o nginx.tar
   docker stop nginx-container
   docker rm nginx-container
   ```  

3. **Extract the tarball**:  
   ```bash
   mkdir /tmp/nginx_root
   tar -xf nginx.tar -C /tmp/nginx_root
   ```  

---

### **Step 2: Fix Missing System Files**  
NGINX needs `/dev/null` (a virtual device). Create it:  
```bash
sudo mkdir -p /tmp/nginx_root/dev
sudo mknod -m 666 /tmp/nginx_root/dev/null c 1 3
```  

---

### **Step 3: Run NGINX in a `chroot` Jail**  
```bash
sudo chroot /tmp/nginx_root /usr/sbin/nginx
```  
- **What’s happening?**  
  - `chroot /tmp/nginx_root`: Changes the root directory to `nginx_root`.  
  - `/usr/sbin/nginx`: Runs NGINX **inside** the jail.  

**Test it**: Open `http://localhost:80` in your browser.  

---

### **Step 4: Check If NGINX Is Running**
#### **Method 1: Use `ps`**
```bash
ps aux | grep nginx
```
- **Output**:  
  ```
  root     12345  0.0  0.1  12345  6789 ?        S    12:34   0:00 /usr/sbin/nginx
  ```
  - The process ID (PID) here is `12345`.

#### **Method 2: Use `pgrep`**
```bash
pgrep nginx
```
- **Output**:  
  ```
  12345
  ```

### **Step 5: Check Which Port NGINX Is Using**
NGINX uses **port 80** by default. To confirm:
#### **Method 1: Use `netstat`**
```bash
sudo netstat -tulpn | grep nginx
```
- **Output**:  
  ```
  tcp   0    0 0.0.0.0:80    0.0.0.0:*    LISTEN    12345/nginx
  ```
  - `0.0.0.0:80` means NGINX is listening on **port 80**.

#### **Method 2: Use `ss` (modern alternative to `netstat`)**  
```bash
sudo ss -tulpn | grep nginx
```


### **Step 6: Check Which Filesystem NGINX Is Using**
#### **Step 1: Find the Process’s Root Directory**
```bash
ls -l /proc/12345/root
```
- **Output**:  
  ```
  lrwxrwxrwx 1 root root 0 Oct 31 12:34 /proc/12345/root -> /path/to/nginx_root
  ```
  - This shows the process is using `/path/to/nginx_root` as its root (`/`).

#### **Step 2: Inspect Files Inside the Jail**
```bash
sudo chroot /path/to/nginx_root /bin/sh
# Inside the jail:
ls /etc/nginx/nginx.conf  # View config file
exit
```

### **Step 7: Connect to New Filesystem and Run Some Basic Commands**  
```bash
chroot nginx_root /bin/sh
# service nginx status
nginx is running.
# 
# ls
bin  boot  dev	docker-entrypoint.d  docker-entrypoint.sh  etc	home  lib  lib64  media  mnt  opt  proc  root  run  sbin  srv  sys  tmp  usr  var
#
```  

### **Step 8. Stop the NGINX Service**
#### **Method 1: Kill by PID**
```bash
sudo kill 12345
```

#### **Method 2: Kill by Name**
```bash
sudo pkill nginx
```


---

### **Step 4: Create MiniDocker (Go Program)**  
Automate this with a Go program named `minidocker.go`:  

```go
package main

import (
    "os"
    "os/exec"
    "syscall"
)

func main() {
    // 1. Path to the jail directory
    rootDir := "./nginx_root"

    // 2. Command to run inside the jail
    cmd := exec.Command("/usr/sbin/nginx")

    // 3. Attach input/output to the terminal
    cmd.Stdin = os.Stdin
    cmd.Stdout = os.Stdout
    cmd.Stderr = os.Stderr

    // 4. Change root to the jail
    if err := syscall.Chroot(rootDir); err != nil {
        panic(err)
    }

    // 5. Run the command
    if err := cmd.Run(); err != nil {
        panic(err)
    }
}
```  

**Build and Run**:  
```bash
go build minidocker.go
sudo ./minidocker
```  

---

## **5. Limitations**  
| MiniDocker          | Docker               |  
|---------------------|----------------------|  
| ❌ No network isolation | ✅ Uses network namespaces |  
| ❌ No process isolation | ✅ Uses PID namespaces |  
| ❌ No resource limits | ✅ Uses cgroups |  

---

## **6. Conclusion**  
You’ve built **MiniDocker**, a minimalist container runtime! While Docker adds layers like networking and security, the core idea—**isolating processes with `chroot`**—remains simple.  

**Try Next**:  
- Add network isolation with `ip netns`.  
- Use cgroups to limit CPU/memory.  
- Experiment with Redis or Python apps!  

---

## **7. Appendix**  
### **Full Commands**  
```bash
# Extract NGINX filesystem
docker pull nginx
docker create --name nginx-container nginx
docker export nginx-container -o nginx.tar
tar -xf nginx.tar -C nginx_root

# Fix /dev/null
sudo mkdir -p nginx_root/dev
sudo mknod -m 666 nginx_root/dev/null c 1 3

# Run MiniDocker
go build minidocker.go
sudo ./minidocker

# Check if running
ps aux | grep nginx
sudo netstat -tulpn | grep nginx

# Stop NGINX
sudo pkill nginx
```  