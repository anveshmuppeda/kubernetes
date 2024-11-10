# Kubernetes Probes - Overview and Best Practices

Kubernetes uses **Probes** to monitor the health of containers running inside Pods. Probes are essential for ensuring that your containers are operating correctly and can handle traffic. They are a key part of Kubernetes’ self-healing capabilities, enabling automatic restarts, load balancing, and health checks.

In Kubernetes, there are three primary types of probes:
1. **Liveness Probe**
2. **Readiness Probe**
3. **Startup Probe**

Each probe serves a unique purpose in the lifecycle of a container. This README provides a comprehensive overview of these probes, their uses, and differences.

---

## Table of Contents

1. [What are Kubernetes Probes?](#what-are-kubernetes-probes)
2. [Types of Probes](#types-of-probes)
   - [Liveness Probe](#liveness-probe)
   - [Readiness Probe](#readiness-probe)
   - [Startup Probe](#startup-probe)
3. [Why Do We Use Probes?](#why-do-we-use-probes)
4. [Differences Between Probes](#differences-between-probes)
5. [Best Practices for Probes](#best-practices-for-probes)
6. [Conclusion](#conclusion)

---

## What Are Kubernetes Probes?

Probes in Kubernetes are checks that the container must pass to confirm that it is in a healthy state. Probes help Kubernetes determine if a container is functioning correctly, whether it should be restarted, or if it's ready to serve traffic.

Probes provide Kubernetes with the information to:
- Automatically restart failed containers.
- Ensure containers are properly initialized and serving traffic.
- Avoid sending traffic to containers that are not ready to handle it.

There are **three types of probes**:
1. **Liveness Probe** – Checks if the container is still running.
2. **Readiness Probe** – Checks if the container is ready to accept traffic.
3. **Startup Probe** – Checks if the container has successfully started.

---

## Types of Probes

### Liveness Probe

**Definition**: The **Liveness Probe** determines whether a container is still running. If a container fails the liveness check, Kubernetes will restart the container.

- **Use Case**: It is used to detect and remedy situations where an application is running but stuck in a non-recoverable state.
- **How it works**: It could be an HTTP request, TCP check, or an execution of a command within the container.
- **Example Use Case**: If an application crashes or hangs, Kubernetes will detect the issue and restart the container to restore it to a working state.

You can find the detailed hands-on examples and best practices for **Liveness Probes** [here](./liveness/README.MD).

---

### Readiness Probe

**Definition**: The **Readiness Probe** checks whether a container is ready to accept traffic. Kubernetes only routes traffic to containers that pass the readiness check.

- **Use Case**: It is crucial for containers that take a longer time to initialize or have dependencies on other services before they can accept traffic.
- **How it works**: Similar to the liveness probe, it can be an HTTP request, TCP check, or an exec command, but it checks the application’s readiness to serve requests.
- **Example Use Case**: When a web server or database needs to initialize connections, or pre-load data before serving requests.

You can find the detailed hands-on examples and best practices for **Readiness Probes** [here](./readiness/README.MD).

---

### Startup Probe

**Definition**: The **Startup Probe** is used to check if a container has started correctly. It ensures that Kubernetes doesn’t prematurely kill a container that might take a long time to initialize. If the startup probe fails, Kubernetes will attempt to restart the container.

- **Use Case**: It is beneficial for applications that require extended startup time or have a slow initialization process.
- **How it works**: Like the other probes, it can be an HTTP request, TCP check, or command execution, but it only monitors the container during its startup phase.
- **Example Use Case**: Applications like databases or complex services that may take longer to load should benefit from a startup probe to avoid Kubernetes from terminating them too soon.

You can find the detailed hands-on examples and best practices for **Startup Probes** [here](./startup/README.MD).

---

## Why Do We Use Probes?

Probes are essential for the **self-healing** capabilities of Kubernetes. They enable Kubernetes to:
- **Detect Unhealthy Containers**: By continuously checking the health of a container, Kubernetes can detect when something goes wrong and restart the container.
- **Prevent Traffic to Unready Containers**: With readiness probes, Kubernetes can ensure that only containers that are ready to handle traffic are included in the load balancing pool.
- **Manage Long Initialization Times**: Startup probes help ensure containers that require more time to initialize are not prematurely killed, which is particularly useful for containers that take longer to set up and become operational.

**Why use probes?**  
- **Reliability**: Probes ensure that your containerized applications are robust and resilient.
- **Automation**: Probes automate container health checks and management, removing the need for manual intervention.
- **Efficient Scaling**: Kubernetes can efficiently manage container scaling, restarts, and traffic routing based on the probe results.

---

## Differences Between Probes

| **Probe Type**      | **Purpose**                                  | **Checks**                            | **Timing**                        |
|---------------------|----------------------------------------------|---------------------------------------|-----------------------------------|
| **Liveness Probe**   | Checks if the container is still running     | Application status (e.g., HTTP, TCP, exec) | Continuous, during runtime       |
| **Readiness Probe**  | Checks if the container is ready to serve traffic | Application readiness (e.g., HTTP, TCP, exec) | Continuous, before traffic is routed |
| **Startup Probe**    | Checks if the container has started successfully | Container initialization (e.g., HTTP, TCP, exec) | Only during startup phase        |

**Key Differences**:
- **Liveness Probe** monitors if a container is still running correctly. If it fails, Kubernetes restarts the container.
- **Readiness Probe** ensures the container is ready to handle traffic. If it fails, Kubernetes will not route traffic to the container.
- **Startup Probe** focuses on the startup phase of a container, ensuring that long initialization processes do not cause premature restarts.

---

## Best Practices for Probes

1. **Choose the Right Probe for Your Container**:
   - Use **liveness probes** for ongoing health checks.
   - Use **readiness probes** for containers that need initialization time or depend on other services.
   - Use **startup probes** for containers that require a long time to start up.

2. **Set Proper Delays**:
   - Use `initialDelaySeconds` to give your container enough time to start or initialize.
   - Configure `periodSeconds` and `failureThreshold` to balance between responsiveness and avoiding false positives.

3. **Be Specific with Your Probes**:
   - Use custom health check endpoints (like `/healthz`) for more accurate checks.
   - For complex applications, use the `exec` probe type to run custom startup checks.

4. **Monitor Probe Results**:
   - Regularly check the logs of your probes (`kubectl describe pod <pod-name>`) to ensure probes are functioning as expected.

---

## Conclusion

Kubernetes probes—**Liveness**, **Readiness**, and **Startup**—are crucial components in managing the health and lifecycle of containers. They ensure that containers are running properly, are ready to accept traffic, and are started correctly. By configuring probes effectively, you can improve the reliability and stability of your Kubernetes deployments.

For more details on each individual probe type and hands-on examples:
- [Liveness Probe](./liveness/README.MD)
- [Readiness Probe](./readiness/README.MD)
- [Startup Probe](./startup/README.MD)

Understanding and using probes will help ensure that your Kubernetes workloads are resilient, self-healing, and performant in production.