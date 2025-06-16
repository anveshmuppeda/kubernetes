---
// filepath: kubernetes/docs/012-troubleshoot/exit-code-125/exit-code-125.md
sidebar_label: "Exit Code 125"
sidebar_id: "exit-code-125"
sidebar_position: 5
---

## Exit Code 125: Container Failed to Run Example in Kubernetes

**Scenario**: This example demonstrates a scenario that results in an **Exit Code 125**, indicating that the command to run the container failed. This can occur due to issues like invalid command syntax, insufficient permissions, or compatibility problems.

#### YAML Configuration

Create a Kubernetes deployment YAML file named `exit-code-125-example.yaml`:

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: exit-code-125-example
spec:
  replicas: 1
  selector:
    matchLabels:
      app: exit-code-125
  template:
    metadata:
      labels:
        app: exit-code-125
    spec:
      containers:
      - name: exit-code-125
        image: ubuntu:latest  # Use a basic Ubuntu image
        command: ["invalid-command"]  # This will fail to run
```

### Steps to Deploy

1. **Apply the Deployment**:
   ```bash
   kubectl apply -f exit-code-125-example.yaml
   ```

2. **Check the Status of the Pod**:
   ```bash
   kubectl get pods
   ```

3. **Get the Logs of the Pod**:
   ```bash
   kubectl logs <pod-name>
   ```
   Replace `<pod-name>` with the actual name of the pod created by the deployment.

4. **Check the Pod Description**:
   ```bash
   kubectl describe pod <pod-name>
   ```
   Look for the **State** and **Reason** fields, which should indicate that it terminated with exit code 125.

### Understanding the Exit Code

#### Why We Get This Error
- **Error Type**: Exit Code 125 typically occurs when the container cannot start due to issues with the command specified in the Kubernetes configuration. In this case, the command `invalid-command` does not exist, which leads to the failure.
- **Common Causes**:
  - Incorrect command syntax in the `command` field.
  - The specified user does not have permission to execute the command.
  - Incompatibility between the container engine and the host environment.

#### How to Solve This in the Future
1. **Verify Command Syntax**: Always ensure that the command you intend to run is valid and correctly specified in the YAML file. Test the command locally before using it in Kubernetes.

2. **Check User Permissions**: If your command needs specific user permissions, ensure that the user defined in the container has the necessary permissions to execute the command. You can set the user in the YAML using the `securityContext`:

   ```yaml
   securityContext:
     runAsUser: 1000  # Replace with appropriate user ID
   ```

3. **Validate Container Images**: Ensure that the image used for your container is compatible with the commands you are trying to run. For example, if your command requires specific binaries, ensure they are available in the image.

4. **Log Error Messages**: Utilize logging to capture errors during container startup. You can do this by checking the output of `kubectl logs` after a failed pod starts.

5. **Compatibility Checks**: Ensure that your container engine and Kubernetes environment are compatible, and check for any versioning issues that could lead to execution failures.

### Summary
This configuration demonstrates how to create a Kubernetes deployment that fails to run a container, resulting in Exit Code 125. By understanding the causes of this exit code and following best practices, you can prevent similar issues in the future.
