---
// filepath: /Users/anveshmuppeda/Desktop/anvesh/tech/git/kubernetes/docs/012-troubleshoot/exit-code-130/exit-code-130.md
sidebar_label: "Exit Code 130"
sidebar_id: "exit-code-130"
sidebar_position: 9
---

## Exit Code 130: Script Terminated by User (SIGINT)

#### What is Exit Code 130?
Exit Code 130 indicates that a process was interrupted by the user with a `SIGINT` signal (usually triggered by pressing `Ctrl+C`). This means the process was terminated by the user rather than through a failure.

#### Why Do We Get This Error?
Exit Code 130 occurs when:
- A user manually interrupts a running process with `Ctrl+C`.
- This is typical in interactive sessions where the user wants to stop execution.

### Simulation of Exit Code 130

**Steps to Demonstrate Exit Code 130:**

1. **Create the Pod Using Imperative Command**:
   Use the following command to create a pod that runs an interactive shell:
   ```bash
   kubectl run exit-code-130-simulation --image=alpine --restart=Never -it -- /bin/sh
   ```

2. **Run a Long-Running Command**:
   Inside the pod's shell, execute a long-running command. For instance, you can run a simple loop:
   ```sh
   sleep 600
   ```

3. **Interrupt the Process**:
   While the loop is running, press `Ctrl+C`. This sends a `SIGINT` signal to the process.

4. **Check the Exit Code**:
   After you interrupt the process and exit the shell, check the pod's status to see the exit code:
   ```bash
   kubectl get pod exit-code-130-simulation
   ```
   Then describe the pod to check the exit code:
   ```bash
   kubectl describe pod exit-code-130-simulation
   ```
   You should see an entry indicating that the exit code is `130`.

### Preventing Exit Code 130

To avoid unintentional exits due to user interruption:
- **User Awareness**: Inform users of the implications of sending a `SIGINT` signal during critical operations.
- **Graceful Handling**: Implement signal handling in your scripts to perform necessary cleanup or to confirm exit actions before terminating.

### Conclusion
Using the imperative command to create an interactive pod allows you to easily simulate and observe how **Exit Code 130** occurs when a user interrupts a running process with `Ctrl+C`. This method is effective for demonstrating this exit code in a practical scenario.