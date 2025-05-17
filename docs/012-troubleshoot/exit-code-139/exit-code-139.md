---
// filepath: /Users/anveshmuppeda/Desktop/anvesh/tech/git/kubernetes/docs/012-troubleshoot/exit-code-139/exit-code-139.md
sidebar_label: "Exit Code 139"
sidebar_id: "exit-code-139"
sidebar_position: 1
---

## Exit Code 139: Segmentation Fault (SIGSEGV)

### What is Exit Code 139?
Exit Code 139 indicates that a process has terminated due to a segmentation fault (SIGSEGV). This is a common error that occurs when a program attempts to access memory that it is not allowed to access, leading to a crash.

### Why Do We Get This Error?
Common reasons for encountering Exit Code 139 include:

- **Dereferencing Null Pointers**: The code may be trying to access a null pointer.
- **Buffer Overflows**: Writing more data to a buffer than it can hold can corrupt memory.
- **Invalid Memory Access**: Accessing memory that has already been freed or not allocated.
- **Incorrect Compiler Optimization**: Sometimes, optimizations may lead to unexpected behavior in certain situations.

### Simulation of Exit Code 139

1. **Pod Configuration**:
   The following Kubernetes Pod configuration will run a C program that intentionally triggers a segmentation fault.

   **File Name**: `exit-code-139-simulation.yaml`  
   **Configuration**:
   ```yaml
   apiVersion: v1
   kind: Pod
   metadata:
     name: exit-code-139-simulation
   spec:
     containers:
     - name: exit-code-139
       image: alpine:latest
       command: ["/bin/sh", "-c", "apk add --no-cache gcc musl-dev; echo '#include <stdio.h>' > segfault.c; echo 'int main() { int *p = NULL; *p = 0; return 0; }' >> segfault.c; gcc segfault.c -o segfault; ./segfault"]
     restartPolicy: OnFailure
   ```

2. **Deploy the Simulation**:
   To deploy the above configuration, run the following command:
   ```bash
   kubectl apply -f exit-code-139-simulation.yaml
   ```

3. **Expected Outcome**:
   After deploying the Pod, it should terminate due to a segmentation fault, resulting in an Exit Code 139. You can check the status with:
   ```bash
   kubectl describe pod exit-code-139-simulation
   ```
   The logs will show that the program crashed due to a segmentation fault:
   ```
   Segmentation fault (core dumped)
   ```

### Fixing Exit Code 139

To resolve Exit Code 139, you need to ensure that your code does not attempt to access invalid memory.

1. **Updated Pod Configuration**:
   Here’s an updated configuration that avoids segmentation faults by checking for null pointers before dereferencing.

   **File Name**: `exit-code-139-fix.yaml`  
   **Configuration**:
   ```yaml
   apiVersion: v1
   kind: Pod
   metadata:
     name: exit-code-139-fix
   spec:
     containers:
     - name: exit-code-139
       image: alpine:latest
       command: ["/bin/sh", "-c", "apk add --no-cache gcc musl-dev; echo '#include <stdio.h>' > safe.c; echo 'int main() { int *p = NULL; if (p != NULL) { *p = 0; } return 0; }' >> safe.c; gcc safe.c -o safe; ./safe"]
     restartPolicy: OnFailure
   ```

2. **Deploy the Fixed Configuration**:
   To deploy the fixed configuration, run the following command:
   ```bash
   kubectl apply -f exit-code-139-fix.yaml
   ```

3. **Expected Outcome**:
   With this configuration, the code will run successfully without causing a segmentation fault, and you will see no errors in the logs.

### Preventing Exit Code 139 in the Future

To avoid encountering Exit Code 139 in future deployments, consider these best practices:

- **Code Review**: Regularly review code for potential segmentation faults, especially in C/C++ applications.
- **Use Static Analysis Tools**: Tools like `valgrind`, `AddressSanitizer`, or `clang` can help identify memory access issues before deploying.
- **Handle Pointers Safely**: Always check pointers before dereferencing them to prevent null pointer dereferences.
- **Testing**: Conduct thorough testing under various conditions to identify and address potential segmentation faults.

### Conclusion
Exit Code 139 indicates that a container has crashed due to a segmentation fault. By ensuring safe memory access in your code and following best practices, you can minimize the chances of encountering this issue. This guide provided a simulation of the error, a way to fix it, and strategies for prevention.