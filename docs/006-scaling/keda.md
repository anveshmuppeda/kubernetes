---
// filepath: kubernetes/docs/scaling/keda.md
sidebar_label: "KEDA (Kubernetes Event-Driven Autoscaling)"
sidebar_id: "keda"
sidebar_position: 3
---

# KEDA (Kubernetes Event-Driven Autoscaling)

KEDA (Kubernetes Event-Driven Autoscaling) is a Kubernetes-based component that provides event-driven autoscaling for workloads. It allows you to scale your applications based on custom metrics or external event sources, such as message queues, databases, or cloud services. This guide provides an overview of KEDA, its benefits, and how to configure it in a Kubernetes cluster.

---

<div style={{ backgroundColor: '#f9f9f9', borderLeft: '4px solid #0078d4', padding: '1rem', margin: '1rem 0', borderRadius: '5px' }}>
    <h2 style={{ marginTop: 0 }}>🚧 Work in Progress</h2>
    <p>This page is currently under construction. Please check back later for detailed information about KEDA setup and usage in Kubernetes.</p>
</div>

---

## Table of Contents
- [Introduction](#introduction)
- [Why Use KEDA?](#why-use-keda)
- [How KEDA Works](#how-keda-works)
- [Configuration](#configuration)
- [Best Practices](#best-practices)

---

## Introduction
KEDA extends Kubernetes' native autoscaling capabilities by enabling event-driven scaling. It integrates seamlessly with Kubernetes and supports a wide range of event sources, making it ideal for scaling workloads based on real-time demand.

---

## Why Use KEDA?
- **Event-Driven Scaling**: Scale workloads based on external events, such as messages in a queue or database activity.
- **Custom Metrics**: Supports scaling based on custom metrics or external triggers.
- **Seamless Integration**: Works alongside Kubernetes' native Horizontal Pod Autoscaler (HPA).
- **Wide Compatibility**: Supports multiple event sources, including Kafka, RabbitMQ, Azure Event Hubs, AWS SQS, and more.

---

## How KEDA Works
1. **Event Source Integration**: KEDA connects to external event sources using scalers.
2. **Metrics Adapter**: KEDA exposes custom metrics to Kubernetes' HPA.
3. **Autoscaling**: Based on the metrics, Kubernetes scales the number of pods in the target workload.

---

## Configuration
To configure KEDA, you need to define a `ScaledObject` resource. Example configuration:

```yaml
apiVersion: keda.sh/v1alpha1
kind: ScaledObject
metadata:
  name: my-app-scaledobject
  namespace: default
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: my-app
  minReplicaCount: 1
  maxReplicaCount: 10
  triggers:
    - type: rabbitmq
      metadata:
        queueName: my-queue
        host: RabbitMQConnectionString
```  

### Key Fields:
- `scaleTargetRef`: Specifies the target workload (e.g., Deployment, StatefulSet) for which KEDA will provide scaling.
- `minReplicaCount`: Minimum number of replicas for the target workload.
- `maxReplicaCount`: Maximum number of replicas for the target workload.
- `triggers`: Defines the event source and scaling criteria. In this example, it uses RabbitMQ as the event source.

## Best Practices
- **Monitor Event Sources**: Regularly monitor the performance of your event sources to ensure they are functioning correctly.
- **Test Scaling Behavior**: Test KEDA's scaling behavior in a staging environment before deploying to production.
- **Use Multiple Triggers**: Consider using multiple triggers for more complex scaling scenarios.
- **Optimize Resource Requests**: Set appropriate resource requests and limits for your workloads to ensure efficient scaling.
- **Documentation**: Refer to the [KEDA documentation](https://keda.sh/docs/) for detailed information on supported event sources and configuration options.

---
Stay tuned for more detailed information on setting up and using KEDA in Kubernetes!