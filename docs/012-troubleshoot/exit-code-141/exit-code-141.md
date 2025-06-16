---
// filepath: kubernetes/docs/012-troubleshoot/exit-code-141/exit-code-141.md
sidebar_label: "Exit Code 141"
sidebar_id: "exit-code-141"
sidebar_position: 14
---

## Exit Code 141: Broken Pipe (SIGPIPE)

### What is Exit Code 141?
Exit Code 141 indicates that a process received a SIGPIPE signal, which typically occurs when a process attempts to write to a pipe where the reading end has already been closed. This signal can cause the process to terminate abnormally.

### Why Do We Get This Error?
The SIGPIPE signal can be triggered by several situations, including:
- **Pipeline Failure**: When a command in a pipeline terminates before the previous command finishes writing to it. For instance, if the reader of the pipe exits, the writer receives a SIGPIPE when trying to write to it.
- **Subshell Termination**: If a subshell or background process writing to the pipe terminates, the main process can receive a SIGPIPE.

### Simulation of Exit Code 141

1. **Pod Configuration**:
   We will create a Kubernetes Pod that demonstrates the SIGPIPE error.

   **File Name**: `exit-code-141-simulation.yaml`
   **Configuration**:
   ```yaml
   apiVersion: v1
   kind: Pod
   metadata:
     name: exit-code-141-simulation
   spec:
     containers:
     - name: exit-code-141
       image: alpine:latest
       command:
         - /bin/sh
         - -c
         - |
           echo "Generating a SIGPIPE error..."
           (echo hello; sleep 1; echo world) | tee >(echo yo)
     restartPolicy: Never
   ```

2. **Deploy the Simulation**:
   To deploy the above configuration, run the following command:
   ```bash
   kubectl apply -f exit-code-141-simulation.yaml
   ```

3. **Expected Outcome**:
   When you apply this configuration, the Pod will terminate due to the SIGPIPE signal, resulting in an exit code of 141. You can check the logs with:
   ```bash
   kubectl logs exit-code-141-simulation
   ```
   You should see output indicating that the process generated a SIGPIPE error.

### Fixing Exit Code 141

To avoid the SIGPIPE error, we can modify the command to handle the termination of the reader process more gracefully.

1. **Updated Pod Configuration**:
   Here’s the updated configuration that handles the SIGPIPE error.

   **File Name**: `exit-code-141-fix.yaml`
   **Configuration**:
   ```yaml
   apiVersion: v1
   kind: Pod
   metadata:
     name: exit-code-141-fix
   spec:
     containers:
     - name: exit-code-141
       image: alpine:latest
       command:
         - /bin/sh
         - -c
         - |
           echo "Generating a SIGPIPE error gracefully..."
           (echo hello; sleep 1; echo world) | {
             tee > /dev/null || echo "Reader process terminated; handling gracefully."
           }
     restartPolicy: Never
   ```

2. **Deploy the Fix**:
   To deploy the fixed configuration, run the following command:
   ```bash
   kubectl apply -f exit-code-141-fix.yaml
   ```

3. **Expected Outcome**:
   After deploying the fixed configuration, check the status of the pod:
   ```bash
   kubectl get pod exit-code-141-fix
   kubectl describe pod exit-code-141-fix
   ```
   This time, the pod should exit gracefully without generating a SIGPIPE error, and you should see output indicating that the reader process was terminated gracefully.

### How to Prevent Exit Code 141 in the Future
To avoid encountering Exit Code 141 in future deployments, consider the following best practices:
- **Handle SIGPIPE Signals**: Implement signal handling in your scripts or commands to manage situations where a pipe may be closed unexpectedly.
- **Check Process Status**: Before writing to a pipe, check if the reading process is still active to prevent writing to a closed pipe.
- **Test Pipelines Thoroughly**: When constructing complex pipelines, test them to ensure they handle data flow correctly and avoid premature termination.
- **Use `set -o pipefail`**: In your shell scripts, use `set -o pipefail` to catch failures in the pipeline and handle them appropriately.

### Conclusion
Exit Code 141 is a common issue that arises from SIGPIPE signals caused by pipeline failures. By handling SIGPIPE signals gracefully and implementing robust checks in your scripts, you can improve the reliability of your Kubernetes applications. This guide provided both a simulation of the error and a straightforward fix, along with strategies to help you avoid this issue in the future.