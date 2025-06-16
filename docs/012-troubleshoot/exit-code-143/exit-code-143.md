---
// filepath: kubernetes/docs/012-troubleshoot/exit-code-143/exit-code-143.md
sidebar_label: "Exit Code 143"
sidebar_id: "exit-code-143"
sidebar_position: 15
---

## Exit Code 143: Graceful Termination (SIGTERM)

### What is Exit Code 143?
Exit Code 143 indicates that a container was terminated gracefully by receiving a SIGTERM signal. This is commonly observed when a pod is deleted, or when Kubernetes decides to restart the container due to failing health checks. The process can handle this termination request, allowing for cleanup operations before exiting.

### Why Do We Get This Error?
Exit Code 143 typically occurs under the following circumstances:

- **Pod Deletion**: When a pod is manually deleted or terminated by a controller (like during updates or scaling).
- **Liveness Probe Failures**: If a liveness probe fails, Kubernetes sends a SIGTERM to the pod, allowing it to gracefully handle the shutdown.
- **Resource Constraints**: If a node runs out of resources, Kubernetes may evict pods, sending a SIGTERM before termination.
  
Understanding these scenarios can help you implement strategies to handle graceful terminations properly.

### Simulation of Exit Code 143

1. **Pod Configuration**:
   This configuration simulates a scenario where a long-running process in a pod is terminated due to a failing liveness probe, resulting in an Exit Code 143.

   **File Name**: `exit-code-143-simulation.yaml`

   ```yaml
   apiVersion: v1
   kind: Pod
   metadata:
     name: exit-code-143-simulation
   spec:
     terminationGracePeriodSeconds: 10  # Allows time for SIGTERM trap to execute
     containers:
     - name: exit-code-143
       image: alpine:latest
       command:
         - /bin/sh
         - -c
         - |
           trap 'echo "SIGTERM caught, exiting with 143"; exit 143' TERM
           echo "Starting long-running process..."
           while true; do sleep 1; done  # Simulates a long-running process
       livenessProbe:
         httpGet:
           path: /non-existent-path  # Deliberately incorrect path to fail liveness probe
           port: 8080
         initialDelaySeconds: 5
         periodSeconds: 5
         failureThreshold: 1  # Fail the probe quickly
       lifecycle:
         preStop:
           exec:
             command: ["/bin/sh", "-c", "kill -s TERM 1"]  # Send SIGTERM to main process
     restartPolicy: OnFailure
   ```

2. **Deploy the Simulation**:
   To deploy this configuration, run the following command:
   ```bash
   kubectl apply -f exit-code-143-simulation.yaml
   ```

3. **Expected Outcome**:
   After deployment, the liveness probe will fail after the initial delay, causing Kubernetes to send a SIGTERM signal to the pod. The `trap` command will catch this signal, print a message, and exit with code 143. To check the exit code, run:
   ```bash
   kubectl get pod exit-code-143-simulation -o jsonpath='{.status.containerStatuses[0].state.terminated.exitCode}'
   ```
   The output should indicate `143`, confirming the graceful termination.

### Fixing Exit Code 143

If you find that your application is exiting with code 143 unexpectedly, you can address it by ensuring that your application correctly handles termination signals.

1. **Ensure Proper Signal Handling**:
   Modify your application to handle the SIGTERM signal effectively. In the provided simulation, the `trap` command demonstrates how to catch the signal and perform cleanup before exiting.

2. **Review Liveness Probes**:
   Adjust your liveness probes to ensure they accurately reflect the health of your application. Avoid unnecessary terminations by ensuring the probe paths and parameters are valid.

3. **Testing and Monitoring**:
   Implement tests and monitoring tools to identify when and why your pods are receiving SIGTERM signals. This will help you fine-tune the behavior of your applications under various conditions.

### How to Prevent Unplanned Exit Code 143 Terminations

To minimize unplanned occurrences of Exit Code 143, consider the following practices:

- **Graceful Shutdown Logic**: Implement signal handling to gracefully shut down your application, ensuring all resources are released.
- **Adjust Resource Limits**: Set appropriate resource requests and limits to prevent your pods from being evicted due to insufficient resources.
- **Set a Suitable Grace Period**: Define a reasonable `terminationGracePeriodSeconds` to allow enough time for your applications to finish their processes upon receiving SIGTERM.
- **Health Check Accuracy**: Regularly review and test your health check configurations to ensure they function as expected, reducing the likelihood of false negatives.

### Conclusion
Exit Code 143 is an important aspect of Kubernetes container management, indicating a graceful termination of a pod. By simulating this scenario and implementing best practices, you can ensure that your applications handle terminations properly, leading to smoother operations and better resource management. The provided configuration serves as a helpful example to guide you in implementing graceful shutdowns within your Kubernetes deployments.