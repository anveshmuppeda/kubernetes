#  Quality of Service (QoS)  

In Kubernetes, Quality of Service (QoS) is a mechanism to prioritize the allocation of resources such as CPU and memory among different Pods running on a node. Kubernetes defines three QoS classes for Pods:  

1. **Guaranteed**: Pods that have specified both a CPU and memory request, and they match their limit. These Pods are ensured to be allocated the requested resources, and they are not subject to being evicted due to resource shortages.  

2. **Burstable**: Pods that have specified both a CPU and memory request, but they may exceed their requests for burstable periods. These Pods can consume resources beyond their requests but are limited by their specified limits. They are subject to being evicted if the node experiences resource contention.  

3. **BestEffort**: Pods that do not have any resource requests or limits. These Pods are not guaranteed any specific amount of resources and are the first to be evicted when the node runs out of resources.  

Kubernetes uses these QoS classes to make decisions about scheduling, eviction, and scaling. For example, when a node is under resource pressure, Kubernetes may first evict BestEffort Pods to free up resources, followed by Burstable Pods, and only evict Guaranteed Pods as a last resort. Additionally, QoS information can be useful for cluster administrators to understand how resource-intensive different workloads are and to optimize resource allocation accordingly.  

## Retrieve the QoS class for a Pod  
Rather than see all the fields, you can view just the field you need:  
```bash
kubectl --namespace=qos-example get pod qos-demo-4 -o jsonpath='{ .status.qosClass}{"\n"}'  
```
