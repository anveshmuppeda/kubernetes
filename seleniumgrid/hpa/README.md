## Kubernetes HPA(Horizontal Pod Autoscaling)
### Kubernetes autoscaling basics
Before we go in-depth on HPA, we need to review Kubernetes autoscaling in general. Autoscaling is a method of automatically scaling K8s workloads up or down based on historical resource usage. Autoscaling in Kubernetes has three dimensions:

1. Horizontal Pod Autoscaler (HPA):adjusts the number of replicas of an application.
2. Cluster Autoscaler:adjusts the number of nodes of a cluster.
3. Vertical Pod Autoscaler (VPA):adjusts the resource requests and limits of a container.

The different autoscalers work at one of two Kubernetes layers
- Pod level:The HPA and VPA methods take place at the pod level. Both HPA and VPA will scale the available resources or instances of the container.
- Cluster level:The Cluster Autoscaler falls under the Cluster level, where it scales up or down the number of nodes inside your cluster.

## What is HPA?
HPA is a form of autoscaling that increases or decreases the number of pods in a replication controller, deployment, replica set, or stateful set based on CPU utilization—the scaling is horizontal because it affects the number of instances rather than the resources allocated to a single container.

## How does HPA work?
In simple terms, HPA works in a “check, update, check again” style loop. Here’s how each of the steps in that loop work.

1. HPA continuously monitors the metrics server for resource usage.
2. Based on the collected resource usage, HPA will calculate the desired number of replicas required.
3. Then, HPA decides to scale up the application to the desired number of replicas.
4. Finally, HPA changes the desired number of replicas.
5. Since HPA is continuously monitoring, the process repeats from Step 1.

## Limitations of HPA
While HPA is a powerful tool, it’s not ideal for every use case and can’t address every cluster resource issue. Here are the most common examples:

1. One of HPA’s most well-known limitations is that it does not work with DaemonSets.
2. If you don’t efficiently set CPU and memory limits on pods, your pods may terminate frequently or, on the other end of the spectrum, you’ll waste resources.
3. If the cluster is out of capacity, HPA can’t scale up until new nodes are added to the cluster. Cluster Autoscaler (CA) can automate this process. We have an article dedicated to CA; however, below is a quick contextual explanation.

### Command to generate load against the php-apache service 
```sh
 kubectl run -n anvesh -i --tty load-generator --rm --image=busybox:1.28 --restart=Never -- //bin//sh -c "while sleep 0.01; do wget -q -O- php-apache; done"
```
