---
// filepath: /Users/anveshmuppeda/Desktop/anvesh/tech/git/kubernetes/docs/012-troubleshoot/exit-code-0/exit-code-0.md
sidebar_label: "Exit Code 0"
sidebar_id: "exit-code-0"
sidebar_position: 2
---

## Exit Code 0: Successful Execution

### What is Exit Code 0?
Exit Code 0 is a standard exit code that signifies **successful execution**. When a process or command in a container (or any other environment) completes all its operations without encountering errors, it exits with code 0.

### Why Do We Get This Code?
Receiving an exit code of 0 means that the command executed without any issues. Common reasons for getting this code include:

- **Successful Command Completion**: All commands or operations in the container ran without encountering any errors.
- **Expected Output**: Any output generated was handled as anticipated, with no need for error handling.
- **Clean Exit from Script**: In scripts, the `exit 0` command is often explicitly used to indicate successful completion.

### Simulation of Exit Code 0

1. **Pod Configuration**:
   We’ll create a Kubernetes pod that runs a simple command, completing successfully with an exit code of 0.

   **File Name**: `exit-code-0-simulation.yaml`

   ```yaml
   apiVersion: v1
   kind: Pod
   metadata:
     name: exit-code-0-simulation
   spec:
     containers:
     - name: exit-code-0
       image: alpine:latest
       command:
         - /bin/sh
         - -c
         - |
           echo "This command will complete successfully."
     restartPolicy: Never  # Do not restart after successful completion
   ```

2. **Deploy the Simulation**:
   To deploy this configuration, run:
   ```bash
   kubectl apply -f exit-code-0-simulation.yaml
   ```

3. **Expected Outcome**:
   After applying this configuration, the pod should complete with an exit code of 0, indicating success. To verify, check the pod’s status:
   ```bash
   kubectl get pod exit-code-0-simulation -o jsonpath='{.status.containerStatuses[0].state.terminated.exitCode}'
   ```
   This should return `0`.

### How to Confirm and Use Exit Code 0 in Scripts and Containers

If you frequently work with scripts and want to ensure that operations complete successfully:

1. **Use `exit 0` Explicitly**:
   In scripts, you can include `exit 0` at the end to make it clear that the script is expected to complete without errors.

2. **Conditional Checks for Success**:
   In automation or CI/CD pipelines, you can check for an exit code of 0 to confirm successful execution before proceeding to the next steps. This is often used to prevent further actions from being taken if previous steps failed.

3. **Monitoring**:
   Regularly monitor and review logs and exit codes, especially in long-running or critical applications, to ensure processes complete as expected without unhandled errors.

### Conclusion
Exit Code 0 is the ideal result when running commands, scripts, or applications in containers, as it signals that everything executed correctly. By explicitly managing exit codes in your scripts and confirming successful completion, you can ensure the smooth operation of your Kubernetes applications. This configuration example illustrates how to simulate a clean exit with code 0, confirming that your applications can signal success effectively.