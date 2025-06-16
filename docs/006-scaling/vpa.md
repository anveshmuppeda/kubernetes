---
// filepath: kubernetes/docs/scaling/vpa.md
sidebar_label: "Vertical Pod Autoscaler (VPA)"
sidebar_id: "vpa"
sidebar_position: 2
---

# Vertical Pod Autoscaler (VPA)

The Vertical Pod Autoscaler (VPA) is a Kubernetes feature that automatically adjusts the resource requests and limits of pods based on observed usage. This ensures that your applications have the resources they need to run efficiently without over-provisioning. This guide provides an overview of VPA, its benefits, and how to configure it in a Kubernetes cluster.

---

<div style={{ backgroundColor: '#f9f9f9', borderLeft: '4px solid #0078d4', padding: '1rem', margin: '1rem 0', borderRadius: '5px' }}>
    <h2 style={{ marginTop: 0 }}>🚧 Work in Progress</h2>
    <p>This page is currently under construction. Please check back later for detailed information about VPA setup and usage in Kubernetes.</p>
</div>

---

## Table of Contents
- [Introduction](#introduction)
- [Why Use VPA?](#why-use-vpa)
- [How VPA Works](#how-vpa-works)
- [Configuration](#configuration)
- [Best Practices](#best-practices)

---

## Introduction
The Vertical Pod Autoscaler (VPA) adjusts the CPU and memory resource requests and limits for pods in a Kubernetes cluster. Unlike the Horizontal Pod Autoscaler (HPA), which scales the number of pods, VPA focuses on optimizing the resource allocation for individual pods.

---

## Why Use VPA?
- **Resource Optimization**: Ensures that pods have the right amount of CPU and memory to handle their workloads.
- **Reduced Over-Provisioning**: Prevents over-allocation of resources, saving costs in cloud environments.
- **Improved Performance**: Helps avoid resource starvation by dynamically adjusting resource requests.

---

## How VPA Works
1. **Metrics Collection**: VPA collects resource usage metrics from the Kubernetes Metrics Server.
2. **Recommendation**: Based on observed usage, VPA provides recommendations for CPU and memory requests and limits.
3. **Scaling Action**: VPA can automatically apply the recommendations by restarting pods with updated resource configurations.

---

## Configuration
To configure VPA, you need to define a VerticalPodAutoscaler resource. Example configuration:

```yaml
apiVersion: autoscaling.k8s.io/v1
kind: VerticalPodAutoscaler
metadata:
  name: my-app-vpa
  namespace: default
spec:
  targetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: my-app
  updatePolicy:
    updateMode: "Auto"
```

### Key Fields:
- `targetRef`: Specifies the target workload (e.g., Deployment, StatefulSet) for which VPA will provide recommendations.
- `updatePolicy`: Defines how VPA will apply the recommendations. Options include `Auto` (automatic updates) or `Off` (manual updates). 
   * `Auto` will automatically update the resource requests and limits of the pods based on the recommendations.
   * `Off` will only provide recommendations without applying them automatically.

## Best Practices
- **Monitor Resource Usage**: Regularly monitor the resource usage of your applications to ensure that VPA is providing accurate recommendations.
- **Test Recommendations**: Before applying VPA recommendations in production, test them in a staging environment to ensure they do not negatively impact application performance.
- **Use with HPA**: VPA can be used in conjunction with HPA to optimize both resource allocation and scaling based on workload demand.
- **Set Resource Limits**: Always set resource limits for your pods to prevent them from consuming excessive resources and affecting other workloads in the cluster.
- **Review Recommendations**: Periodically review VPA recommendations to ensure they align with your application's performance and resource requirements.

---

Stay tuned for updates as we continue to enhance this guide!
