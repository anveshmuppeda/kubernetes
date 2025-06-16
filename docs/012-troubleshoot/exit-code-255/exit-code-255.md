---
// filepath: kubernetes/docs/012-troubleshoot/exit-code-255/exit-code-255.md
sidebar_label: "Exit Code 255"
sidebar_id: "exit-code-255"
sidebar_position: 16
---

## Exit Code 255: Exit Status Out Of Range

### What is Exit Code 255?
Exit Code 255 is a generic error code indicating that a command exited with a status that is out of the normal range. This can occur due to various reasons, including the failure of a command or script, or executing an invalid command.

### Why Do We Get This Error?
Exit Code 255 can occur for several reasons:

- **Command Failure**: The command executed within the container failed, returning an exit status that is not valid.
- **Invalid Command Execution**: If a command does not exist or is incorrectly specified, the shell may exit with 255.
- **Scripting Issues**: Unhandled errors or improper exit codes in shell scripts can result in this exit status.

### Simulation of Exit Code 255

1. **Pod Configuration**:
   This configuration simulates a scenario where an attempt is made to run a non-existent command, resulting in an exit code of 255.

   **File Name**: `exit-code-255-simulation.yaml`

   ```yaml
   apiVersion: v1
   kind: Pod
   metadata:
     name: exit-code-255-simulation
     labels:
       pod-name: exit-code-255
   spec:
     containers:
     - name: exit-code-255
       image: alpine:latest
       command:
         - /bin/sh
         - -c
         - |
           echo "Attempting to execute a command that will fail..."
           # Simulate a failure by trying to run a non-existent command
           non_existent_command || exit 255  # This will cause the pod to exit with code 255
       terminationMessagePath: /dev/termination-log
       terminationMessagePolicy: File
       tty: true
     restartPolicy: Never  # Do not restart on failure
   ```

2. **Deploy the Simulation**:
   To deploy this configuration, run the following command:
   ```bash
   kubectl apply -f exit-code-255-simulation.yaml
   ```

3. **Expected Outcome**:
   When you deploy this pod, it will attempt to execute a command that does not exist, resulting in an exit code of 255. To check the exit code, run:
   ```bash
   kubectl get pod exit-code-255-simulation -o jsonpath='{.status.containerStatuses[0].state.terminated.exitCode}'
   ```
   The output should indicate `255`, confirming the error.

### Fixing Exit Code 255

If you encounter Exit Code 255, consider the following steps to resolve the issue:

1. **Check Command Syntax**:
   Ensure that the command being executed is correct and properly formed. Look for typos or invalid arguments.

2. **Debugging**:
   Utilize logging and debugging to understand where the command is failing. Consider adding echo statements or logging to capture more context about the execution.

3. **Review Environment Configuration**:
   Verify that all required dependencies are present and correctly configured in the container environment. This includes checking paths, permissions, and installed packages.

4. **Error Handling in Scripts**:
   If you are running a script, implement proper error handling to catch and manage errors gracefully, rather than allowing them to bubble up and result in a generic exit code.

### How to Prevent Exit Code 255 in the Future

To reduce the likelihood of encountering Exit Code 255 in your Kubernetes pods, consider the following best practices:

- **Implement Robust Error Handling**: Make sure that your scripts handle errors effectively. Use commands like `set -e` to stop on errors or handle specific error conditions gracefully.
- **Testing**: Run your commands or scripts locally or in a development environment before deploying them to production, to catch potential issues early.
- **Use Liveness and Readiness Probes**: Implement health checks to ensure your application is running correctly, which can help identify issues before they result in container failures.
- **Logging**: Incorporate logging throughout your application to provide visibility into its operations, making it easier to diagnose failures when they occur.

### Conclusion
Exit Code 255 is a non-specific error that can arise from various issues within your containerized applications. By simulating this exit code, identifying its root causes, and following best practices, you can better manage and mitigate errors in your Kubernetes deployments. The provided configuration serves as an example to help you understand and address issues that may lead to an exit status out of range.