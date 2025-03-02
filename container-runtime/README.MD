# **Build a Docker-like Tool from Scratch: Create Your Own Container Runtime with Go 🐳🛠️**  
### **A Hands-On Guide to Linux Isolation, Process Jails, and MiniDocker Internals 🔍👨💻**
*Learn how Docker works under the hood by creating a minimalist runtime called **MiniDocker**.*  

---

## **Table of Contents**  
1. [Introduction](#1.introduction)  
   - [Why This Guide?](#why-this-guide?)  
   - [What is the Use of This Guide?](#what-is-the-use-of-this-guide?)  
   - [Who is this for?](#who-is-this-for?)  
2. [Docker Runtimes Explained Simply](#docker-runtimes-explained-simply)  
3. [Understanding `chroot`](#understanding-chroot)  
4. [Hands-On Guide to Run Container in New Runtime](#hands-on-guide-to-run-container-in-new-runtime)  
   - [Step 1: Pull and Extract NGINX Files](#step-1-pull-and-extract-nginx-files)  
   - [Step 2: Fix Missing System Files](#step-2-fix-missing-system-files)  
   - [Step 3: Run NGINX in a `chroot` Jail](#step-3-run-nginx-in-a-chroot-jail)  
   - [Step 4: Check if NGINX Is Running](#step-4-check-if-nginx-is-running)  
   - [Step 5: Check Which Port NGINX Is Using](#step-5-check-which-port-nginx-is-using)  
   - [Step 6: Check Which Filesystem NGINX Is Using](#step-6-check-which-filesystem-nginx-is-using)  
   - [Step 7: Connect to New Filesystem and Run Some Basic Commands](#step-7-connect-to-new-filesystem-and-run-some-basic-commands)  
   - [Step 8: Stop the NGINX Service](#step-8-stop-the-nginx-service)  
5. [Create MiniDocker](#5-create-minidocker)  
   - [Step 1: Create MiniDocker (Go Program)](#step-1-create-minidocker-go-program)  
   - [Step 2: Build MiniDocker (Go Program)](#step-2-build-minidocker-go-program)  
   - [Step 3: Pull Image Using MiniDocker](#step-3-pull-image-using-minidocker)  
   - [Step 4: Run Container Using MiniDocker](#step-4-run-container-using-minidocker)  
   - [Step 5: Usage Example](#step-5-usage-example)  
5. [Limitations](#limitations)  
6. [Conclusion](#conclusion)  
7. [Appendix](#appendix)  

---

## **1. Introduction**  
### Why This Guide?  
Containers are everywhere, but most explanations stop at calling them "lightweight VMs" or "isolated processes." This leaves developers wondering:

* How do containers actually isolate filesystems?
* What happens when you run docker run nginx?
* Could I build something like Docker myself?

This guide bridges the gap between theory and practice. Instead of abstract concepts, we’ll build a minimalist container runtime using chroot, a 40-year-old Linux feature. By the end, you’ll see containers not as magic, but as clever combinations of Linux primitives.  

### What is the Use of This Guide?  
1. Demystify Containers: Learn how Docker isolates filesystems using chroot and why tools like runc exist.  
2. Hands-On Learning: Run NGINX in a chroot jail and build your own MiniDocker runtime in Go.
3. Debugging Skills: Understand container internals to troubleshoot issues like missing files or ports.
4. Foundation for Advanced Topics: Grasp the basics before diving into Kubernetes, serverless, or edge computing.

### Who is this for?

1. Developers curious about container internals.
2. DevOps engineers who want to debug containers effectively.
3. Tech enthusiasts who enjoy "building from scratch."

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

## **4. Hands-On Guide to Run Container in New Runtime**  
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

### **Step 2: Fix Missing System Files**  
NGINX needs `/dev/null` (a virtual device). Create it:  
```bash
sudo mkdir -p /tmp/nginx_root/dev
sudo mknod -m 666 /tmp/nginx_root/dev/null c 1 3
```  

### **Step 3: Run NGINX in a `chroot` Jail**  
```bash
sudo chroot /tmp/nginx_root /usr/sbin/nginx
```  
- **What’s happening?**  
  - `chroot /tmp/nginx_root`: Changes the root directory to `nginx_root`.  
  - `/usr/sbin/nginx`: Runs NGINX **inside** the jail.  

**Test it**: Open `http://localhost:80` in your browser.  


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

## **5. Create MiniDocker**  

### **Step 1: Create MiniDocker (Go Program)**  
Automate this with a Go program named `minidocker.go`:  

```go
package main

import (
	"fmt"
	"os"
	"os/exec"
	"path/filepath"
	"syscall"
)

const ImageBaseDir = "./imagesource"

func main() {
	if len(os.Args) < 2 {
		printHelp()
		os.Exit(1)
	}

	switch os.Args[1] {
	case "pull":
		if len(os.Args) != 3 {
			fmt.Println("Usage: minidocker pull <image-name>")
			os.Exit(1)
		}
		pullImage(os.Args[2])

	case "run":
		if len(os.Args) < 4 {
			fmt.Println("Usage: minidocker run <image-name> <command> [args...]")
			os.Exit(1)
		}
		runContainer(os.Args[2], os.Args[3:])

	default:
		printHelp()
		os.Exit(1)
	}
}

func printHelp() {
	fmt.Println(`MiniDocker - A simple container runtime
Commands:
  pull <image-name>   Download and prepare a Docker image
  run <image-name> <command>  Run a command in the container
Example:
  minidocker pull nginx
  minidocker run nginx /usr/sbin/nginx`)
}

func pullImage(imageName string) {
	// Create image directory
	imageDir := filepath.Join(ImageBaseDir, imageName+"-root")
	if err := os.MkdirAll(imageDir, 0755); err != nil {
		fmt.Printf("Error creating image directory: %v\n", err)
		os.Exit(1)
	}

	// Docker commands
	fmt.Printf("Pulling image %s...\n", imageName)
	runCommand("docker", "pull", imageName)

	fmt.Printf("Creating temporary container...\n")
	containerID := runCommand("docker", "create", imageName)

	fmt.Printf("Exporting filesystem to %s...\n", imageDir)
	runCommand("docker", "export", containerID, "-o", filepath.Join(imageDir, "image.tar"))
	runCommand("tar", "-xf", filepath.Join(imageDir, "image.tar"), "-C", imageDir)

	// Cleanup
	os.Remove(filepath.Join(imageDir, "image.tar"))
	runCommand("docker", "stop", containerID)
	runCommand("docker", "rm", containerID)

	fmt.Printf("Successfully pulled %s to %s\n", imageName, imageDir)
}

func runContainer(imageName string, command []string) {
	imageDir := filepath.Join(ImageBaseDir, imageName+"-root")
	if _, err := os.Stat(imageDir); os.IsNotExist(err) {
		fmt.Printf("Image %s not found. Pull it first.\n", imageName)
		os.Exit(1)
	}

	// Create temporary runtime directory
	tempDir, err := os.MkdirTemp("", "minidocker-")
	if err != nil {
		fmt.Printf("Error creating temp directory: %v\n", err)
		os.Exit(1)
	}
	defer os.RemoveAll(tempDir)

	// Copy image files
	fmt.Printf("Preparing container filesystem...\n")
	runCommand("cp", "-a", imageDir+"/.", tempDir)

	// Create essential device files
	devDir := filepath.Join(tempDir, "dev")
	if err := os.MkdirAll(devDir, 0755); err != nil {
		fmt.Printf("Error creating dev directory: %v\n", err)
		os.Exit(1)
	}
	runCommand("sudo", "mknod", "-m", "666", filepath.Join(devDir, "null"), "c", "1", "3")

	// Run command in chroot
	fmt.Printf("Starting container...\n")
	cmd := exec.Command(command[0], command[1:]...)
	cmd.Stdin = os.Stdin
	cmd.Stdout = os.Stdout
	cmd.Stderr = os.Stderr

	syscall.Chroot(tempDir)
	cmd.Run()
}

func runCommand(name string, arg ...string) string {
	cmd := exec.Command(name, arg...)
	output, err := cmd.CombinedOutput()
	if err != nil {
		fmt.Printf("Error running command: %s %v\n", name, arg)
		fmt.Printf("%s\n", output)
		os.Exit(1)
	}
	return string(output)
}
```  

### **Step 2: Build MiniDocker (Go Program)**  
**Build and Run**:  
```bash
go build minidocker.go
```  

### **Step 3: Pull Image Using MiniDocker**  
```bash
./minidocker pull nginx
```  

1. Creates ./imagesource/nginx-root  
2. Uses Docker to pull image and export its filesystem  
3. Extracts files to nginx-root  

### **Step 4: Run Container Using MiniDocker**  
```bash
sudo ./minidocker run nginx /usr/sbin/nginx
````  

1. Creates temporary copy of nginx-root  
    ```bash
    $ ls /tmp/minidocker-2945932407
    bin  boot  dev  docker-entrypoint.d  docker-entrypoint.sh  etc  home  lib  lib64  media  mnt  opt  proc  root  run  sbin  srv  sys  tmp  usr  var
    ```
2. Creates essential device files (/dev/null)  
3. Runs command in chroot environment  

### **Step 5: Usage Example**   
```bash
# Pull NGINX image
./minidocker pull nginx

# Run NGINX server (requires sudo for chroot)
sudo ./minidocker run nginx /usr/sbin/nginx

# Verify it's running
curl localhost:80

# Check processes
ps aux | grep nginx

# Stop server
sudo pkill nginx
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
# Pull NGINX image
./minidocker pull nginx

# Run NGINX server (requires sudo for chroot)
sudo ./minidocker run nginx /usr/sbin/nginx

# Verify it's running
curl localhost:80

# Check processes
ps aux | grep nginx

# Stop server
sudo pkill nginx
```  