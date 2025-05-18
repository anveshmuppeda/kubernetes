---
// filepath: /Users/anveshmuppeda/Desktop/anvesh/tech/git/kubernetes/docs/012-troubleshoot/exit-code-2/exit-code-2.md
sidebar_label: "Exit Code 2"
sidebar_id: "exit-code-2"
sidebar_position: 4
---

## Exit Code 2: Misuse of Shell Built-ins

#### What is Exit Code 2?
Exit Code 2 is generally associated with syntax errors or the misuse of shell built-in commands. This can occur when there is incorrect syntax in a shell script or when commands are used improperly within the shell.

#### Why Do We Get This Error?
Exit Code 2 occurs due to:
- **Syntax Errors**: Commands that don’t follow the correct syntax.
- **Improper Shell Command Usage**: When a built-in command or expression is used incorrectly.

#### Simulation of Exit Code 2

This example will use an invalid `if` statement that has incorrect syntax to simulate Exit Code 2.

**File Name**: `exit-code-2-simulation.yaml`

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: exit-code-2-simulation
spec:
  containers:
  - name: exit-code-2
    image: alpine:latest
    command:
      - /bin/sh
      - -c
      - |
        echo "Starting command with intentional syntax error..."
        if [ missing_bracket  # Incorrect syntax for 'if' statement
        echo "This line won't be executed."
    restartPolicy: Never  # Do not restart on failure
```

#### Steps to Deploy and Observe

1. **Deploy the Simulation**:
   Save the configuration in `exit-code-2-simulation.yaml` and apply it:
   ```bash
   kubectl apply -f exit-code-2-simulation.yaml
   ```

2. **Check the Pod's Status**:
   The pod should fail to start due to the syntax error in the `if` statement. Check the status:
   ```bash
   kubectl get pod exit-code-2-simulation
   ```

3. **Examine Logs and Exit Code**:
   To confirm Exit Code 2, check the pod’s details:
   ```bash
   kubectl describe pod exit-code-2-simulation
   ```
   You should see `Exit Code: 2`. Alternatively, check the container’s logs to see the syntax error message:
   ```bash
   kubectl logs exit-code-2-simulation
   ```
   The logs should show an error similar to:
   ```
   /bin/sh: syntax error: unexpected end of file (expecting "then")
   ```

#### Fixing and Preventing Exit Code 2

1. **Correct the Command**:
   Ensure that all shell commands have valid syntax. Here’s an example with a corrected `if` statement:
   ```yaml
   command:
     - /bin/sh
     - -c
     - |
       echo "Starting with correct syntax..."
       if [ 1 -eq 1 ]; then
         echo "Syntax is correct!"
       fi
   ```

2. **Validation and Testing**:
   - **Test Commands Locally**: Run shell commands locally to confirm they are free from syntax errors before adding them to your Kubernetes manifests.
   - **Use Simple Scripts**: For complex commands, consider moving them into a script file that can be thoroughly tested and version-controlled before deployment.

#### Conclusion
Exit Code 2 can be avoided by ensuring valid syntax and testing shell commands thoroughly. This example provided a simulation of the error, a fix, and strategies to prevent this type of error in the future.