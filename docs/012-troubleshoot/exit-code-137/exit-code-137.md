---
// filepath: kubernetes/docs/012-troubleshoot/exit-code-137/exit-code-137.md
sidebar_label: "Exit Code 137"
sidebar_id: "exit-code-137"
sidebar_position: 11
---

## Exit Code 137: Container Killed (SIGKILL)

### What is Exit Code 137?
Exit Code 137 indicates that a container was forcibly terminated by the operating system after receiving a SIGKILL signal. This usually occurs when the container exceeds its memory limits and is killed by the Kubernetes scheduler, or it is manually stopped.

### Why Do We Get This Error?
Common reasons for encountering Exit Code 137 include:

- **Out of Memory (OOM)**: The container consumes more memory than allocated, prompting the Linux Out Of Memory (OOM) killer to terminate it.
- **Manual Termination**: The container may be manually stopped by a user or automated process sending a SIGKILL signal.
- **Resource Constraints**: Kubernetes might kill a container to reclaim resources for other containers.

### Simulation of Exit Code 137

1. **Pod Configuration**:
   The following Kubernetes Pod configuration will run a memory-intensive process that intentionally exceeds its memory limit, simulating a SIGKILL situation.

   **File Name**: `exit-code-137-simulation.yaml`  
   **Configuration**:
   ```yaml
   apiVersion: v1
   kind: Pod
   metadata:
     name: exit-code-137-simulation
   spec:
     containers:
     - name: exit-code-137
       image: alpine:latest
       command: ["/bin/sh", "-c", "echo 'Allocating memory...'; apk add stress-ng; stress-ng --vm 1 --vm-bytes 1G --timeout 10"]
       resources:
         limits:
           memory: "50Mi"  # Set a memory limit to trigger OOM
     restartPolicy: OnFailure
   ```

2. **Deploy the Simulation**:
   To deploy the above configuration, run the following command:
   ```bash
   kubectl apply -f exit-code-137-simulation.yaml
   ```

3. **Expected Outcome**:
   After deploying the Pod, it should be terminated due to exceeding its memory limit, resulting in an Exit Code 137. You can check the status with:
   ```bash
   kubectl describe pod exit-code-137-simulation
   ```
   In the events section, you should see an indication that the container was killed due to memory limits being exceeded.

### Fixing Exit Code 137

To resolve Exit Code 137, you'll need to ensure your containers have appropriate resource allocations.

1. **Updated Pod Configuration**:
   Here’s the updated configuration with adjusted resource limits.

   **File Name**: `exit-code-137-fix.yaml`  
   **Configuration**:
   ```yaml
   apiVersion: v1
   kind: Pod
   metadata:
     name: exit-code-137-fix
   spec:
     containers:
     - name: exit-code-137
       image: alpine:latest
       command: ["/bin/sh", "-c", "echo 'Allocating memory...'; apk add stress-ng; stress-ng --vm 1 --vm-bytes 1G --timeout 10"]
       resources:
         limits:
           memory: "1G"  # Adjusted limit to prevent OOM
     restartPolicy: OnFailure
   ```

2. **Deploy the Fixed Configuration**:
   To deploy the fixed configuration, run the following command:
   ```bash
   kubectl apply -f exit-code-137-fix.yaml
   ```

3. **Expected Outcome**:
   With this configuration, when you apply it, you should see the successful execution of the memory allocation without encountering Exit Code 137. The Pod should complete its task without being killed.

### Preventing Exit Code 137 in the Future

To avoid encountering Exit Code 137 in future deployments, consider these best practices:

- **Set Appropriate Resource Limits**: Always define memory and CPU limits for your containers based on anticipated workloads.
- **Monitor Resource Usage**: Use monitoring tools to keep track of resource consumption and adjust limits as needed.
- **Use Horizontal Pod Autoscaling**: This feature allows your application to scale based on demand, effectively distributing the load.
- **Test Under Load**: Conduct stress testing to understand how your application behaves under high loads and adjust resource requests and limits accordingly.

### Conclusion
Exit Code 137 signifies that a container was killed due to memory overuse. By carefully managing resource allocations and optimizing your applications, you can prevent this issue from disrupting your Kubernetes deployments. This guide provided a simulation of the error, troubleshooting steps, and strategies to help ensure smoother operations in the future.
