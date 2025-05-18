---
// filepath: /Users/anveshmuppeda/Desktop/anvesh/tech/git/kubernetes/docs/012-troubleshoot/exit-code-126/exit-code-126.md
sidebar_label: "Exit Code 126"
sidebar_id: "exit-code-126"
sidebar_position: 6
---

## Exit Code 126 in Kubernetes

#### What is Exit Code 126?
Exit Code 126 occurs when a command in a container is found but cannot be executed. This usually indicates a permission issue, where the script or command lacks executable permissions.

#### Why Do We Get This Error?
The primary reason for encountering Exit Code 126 is due to permission restrictions on the script or command that you are trying to execute. Here are some specific causes:

- **Missing Executable Permissions**: The script may not have been granted executable permissions, preventing it from being run by the shell.
- **Incorrect Command Path**: If the specified path to the script or command is incorrect, it might not execute properly, although this typically results in a different exit code.
- **Volume Configuration Issues**: When mounting scripts or files from ConfigMaps or other volume types, they may not inherit the correct permissions needed to execute.

#### Simulation of Exit Code 126

1. **Pod Configuration**:
   We will create a Kubernetes Pod that runs a script from a ConfigMap that is not executable.

   **File Name**: `exit-code-126-simulation.yaml`
   **Configuration**:
   ```yaml
   apiVersion: v1
   kind: ConfigMap
   metadata:
     name: non-executable-script
   data:
     non-executable-script.sh: |
       #! /bin/sh
       echo "This script is not executable."
   ---
   apiVersion: v1
   kind: Pod
   metadata:
     name: exit-code-126-simulation
   spec:
     containers:
     - name: exit-code-126
       image: alpine:latest
       command: ["/bin/sh", "-c", "/non-executable-script.sh"]
       volumeMounts:
         - name: script-volume
           mountPath: /non-executable-script.sh
           subPath: non-executable-script.sh
     volumes:
       - name: script-volume
         configMap:
           name: non-executable-script
     restartPolicy: OnFailure
   ```

2. **Deploy the Simulation**:
   To deploy the above configuration, run the following command:
   ```bash
   kubectl apply -f exit-code-126-simulation.yaml
   ```

3. **Expected Outcome**:
   When you apply this configuration, the Pod will fail to start due to the script not being executable, leading to a `CrashLoopBackOff` state. You can check the logs with:
   ```bash
   kubectl logs exit-code-126-simulation
   ```
   The output will indicate a permission denied error:
   ```
   /bin/sh: /non-executable-script.sh: Permission denied
   ```

#### Fixing Exit Code 126

To resolve the exit code 126 error, we need to ensure that the script in the ConfigMap is executable.

1. **Updated Pod Configuration**:
   Here’s the updated configuration that allows the script to execute correctly.

   **File Name**: `exit-code-126-fix.yaml`
   **Configuration**:
   ```yaml
   apiVersion: v1
   kind: ConfigMap
   metadata:
     name: executable-script
   data:
     executable-script.sh: |
       #! /bin/sh
       echo "This script is executable."
   ---
   apiVersion: v1
   kind: Pod
   metadata:
     name: exit-code-126-fix
   spec:
     containers:
     - name: exit-code-126
       image: alpine:latest
       command: ["/bin/sh", "-c", "/executable-script.sh"]
       volumeMounts:
         - name: script-volume
           mountPath: /executable-script.sh
           subPath: executable-script.sh
     volumes:
       - name: script-volume
         configMap:
           name: executable-script
           defaultMode: 0500  # Set the permissions to be executable
     restartPolicy: OnFailure
   ```

2. **Deploy the Fix**:
   To deploy the fixed configuration, run the following command:
   ```bash
   kubectl apply -f exit-code-126-fix.yaml
   ```

3. **Expected Outcome**:
   With this configuration, when you apply it and check the logs, you will see the successful execution of the script:
   ```bash
   kubectl logs exit-code-126-fix
   ```
   The output will be:
   ```
   This script is executable.
   ```

#### How to Prevent Exit Code 126 in the Future
To avoid encountering Exit Code 126 in future deployments, consider the following best practices:

- **Always Set Executable Permissions**: When creating scripts that will be executed inside a container, ensure they have executable permissions. You can do this by setting the `defaultMode` in your ConfigMap or using a Dockerfile to set permissions when building an image.
- **Verify Script Paths**: Double-check the paths used to execute scripts to ensure they are correct and point to the intended files.
- **Testing Before Deployment**: Test scripts in a local environment or a testing cluster to ensure they execute without permission errors before deploying them to production.
- **Use Init Containers**: If you have specific initialization logic that requires setting permissions, consider using an init container to set up the environment before your main container starts.

#### Conclusion
Exit Code 126 is a common issue caused by permission problems when trying to run scripts in Kubernetes Pods. By setting the correct permissions in your ConfigMap and following best practices, you can ensure that your scripts execute as intended. This guide has provided both a simulation of the error and a straightforward fix, along with strategies to help you avoid this issue in the future.