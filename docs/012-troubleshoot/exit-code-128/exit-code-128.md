---
// filepath: /Users/anveshmuppeda/Desktop/anvesh/tech/git/kubernetes/docs/012-troubleshoot/exit-code-128/exit-code-128.md
sidebar_label: "Exit Code 128"
sidebar_id: "exit-code-128"
sidebar_position: 1
---

## Exit Code 128 in Kubernetes

#### What is Exit Code 128?
Exit Code 128 typically indicates an error that occurs when the command you are trying to run in a Kubernetes container fails to start due to an issue with the execution environment, often related to the command being invalid or the container runtime being unable to initiate the process.

#### Why Do We Get This Error?
You may encounter Exit Code 128 for several reasons:

- **Invalid Command**: The command specified does not exist in the container or is malformed.
- **Execution Context Issues**: The container runtime may not be able to create the process due to misconfiguration or resource constraints.
- **Configuration Errors**: There may be issues with how the Pod or container is defined in the Kubernetes manifest, such as incorrect volume mounts or missing files.

#### Simulation of Exit Code 128

1. **Pod Configuration**:
   We will create a Kubernetes Pod that attempts to run an invalid command.

   **File Name**: `exit-code-128-simulation.yaml`
   **Configuration**:
   ```yaml
   apiVersion: v1
   kind: Pod
   metadata:
     name: exit-code-128-simulation
   spec:
     containers:
     - name: exit-code-128
       image: alpine:latest
       command: ["non-existent-command"]  # This command does not exist
     restartPolicy: OnFailure
   ```

2. **Deploy the Simulation**:
   To deploy the above configuration, run the following command:
   ```bash
   kubectl apply -f exit-code-128-simulation.yaml
   ```

3. **Expected Outcome**:
   When you apply this configuration, the Pod will fail to start due to the invalid command. You can check the logs with:
   ```bash
   kubectl logs exit-code-128-simulation
   ```
   The output will indicate that the command was not found:
   ```
   /bin/sh: non-existent-command: not found
   ```

#### Fixing Exit Code 128

To resolve the Exit Code 128 error, you need to ensure that the command you want to run is valid and exists in the container image.

1. **Updated Pod Configuration**:
   Here’s the updated configuration that runs a valid command.

   **File Name**: `exit-code-128-fix.yaml`
   **Configuration**:
   ```yaml
   apiVersion: v1
   kind: Pod
   metadata:
     name: exit-code-128-fix
   spec:
     containers:
     - name: exit-code-128
       image: alpine:latest
       command: ["echo", "This command exists!"]  # Valid command that exists
     restartPolicy: OnFailure
   ```

2. **Deploy the Fix**:
   To deploy the fixed configuration, run the following command:
   ```bash
   kubectl apply -f exit-code-128-fix.yaml
   ```

3. **Expected Outcome**:
   With this configuration, when you apply it and check the logs, you will see the successful execution of the command:
   ```bash
   kubectl logs exit-code-128-fix
   ```
   The output will be:
   ```
   This command exists!
   ```

#### How to Prevent Exit Code 128 in the Future
To avoid encountering Exit Code 128 in future deployments, consider the following best practices:

- **Verify Command Validity**: Always check that the command you want to run is present in the container image and spelled correctly.
- **Review Container Configurations**: Ensure that your Kubernetes manifests are correctly set up and that all necessary files and commands are available.
- **Use Shell Command Validations**: If your command involves complex shell operations, consider testing them in a shell locally before deploying.
- **Check Resource Availability**: Ensure your container has adequate resources (CPU, memory) and is correctly configured to avoid runtime issues.

#### Conclusion
Exit Code 128 is a common issue caused by invalid commands or configuration errors when running a Pod in Kubernetes. By ensuring that your commands are valid and your configuration is correct, you can prevent this error from disrupting your deployments. This guide has provided a simulation of the error and a straightforward fix, along with strategies to help you avoid this issue in the future.