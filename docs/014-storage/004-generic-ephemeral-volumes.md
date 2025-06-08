---
// filepath: /Users/anveshmuppeda/Desktop/anvesh/tech/git/kubernetes/docs/014-storage/002-generic-ephemeral-volumes.md
title: "Generic Ephemeral Volumes"
description: "Understanding Generic Ephemeral Volumes in Kubernetes"
sidebar_label: "Generic Ephemeral Volumes"
sidebar_id: "generic-ephemeral-volumes"
sidebar_position: 1
---  

# A Guide to Generic Ephemeral Volumes in Kubernetes

:::tip
Use the [manifest templates](https://github.com/anveshmuppeda/kubernetes/tree/feature/docs_update/docs/014-storage/manifests) to create your own Kubernetes resources which can be used in the examples below.
:::

What if you need temporary storage for a Pod, but `emptyDir` isn't enough? Maybe you need more space than the local node provides, better performance, or a specific storage type. On the other hand, creating and managing `PersistentVolumeClaims` manually for temporary data feels like too much overhead.

Enter **Generic Ephemeral Volumes**. This powerful feature combines the convenience of ephemeral, Pod-bound storage with the power and flexibility of any standard storage driver that supports dynamic provisioning.

This guide will walk you through what they are and how to use them with a practical example using the AWS EBS CSI driver.

## What are Generic Ephemeral Volumes?

A Generic Ephemeral Volume is a type of volume specified directly inside a Pod's manifest. When you create the Pod, Kubernetes automatically creates a `PersistentVolumeClaim` (PVC) on your behalf based on a template you provide. This PVC then triggers the dynamic provisioning of a real storage volume (like an AWS EBS volume).

The key is the lifecycle management:

  * **Creation:** The volume is created when the Pod is created.
  * **Deletion:** When the Pod is deleted, Kubernetes automatically deletes the PVC, which in turn deletes the underlying storage volume.

This gives you the "fire and forget" convenience of an ephemeral volume, but with the features of a persistent one, such as network-attached storage, specific size limits, and your choice of storage performance (e.g., `gp3`, `io2`).

### Prerequisites

This guide uses the AWS Elastic Block Store (EBS) as an example. To follow along, you will need:

  * A Kubernetes cluster running on AWS.
  * The [AWS EBS CSI driver](https://github.com/kubernetes-sigs/aws-ebs-csi-driver) installed and configured in your cluster.

-----

## Hands-On: An EBS-Backed Ephemeral Volume

Let's build a Pod that uses a temporary, 1GiB EBS volume for its data.

### Step 1: Create the Storage Profile (The `StorageClass`)

First, we need to tell Kubernetes *how* to provision our ephemeral EBS volumes. We do this by creating a `StorageClass`.

Create a file named `storageclass-ephemeral.yaml`:

```yaml
# storageclass-ephemeral.yaml
apiVersion: storage.k8s.io/v1
kind: StorageClass
metadata:
  name: ebs-ephemeral-storage
provisioner: ebs.csi.aws.com
allowVolumeExpansion: true
reclaimPolicy: Delete
volumeBindingMode: WaitForFirstConsumer
parameters:
  type: gp3
  fsType: ext4
```

Let's break this down:

  * `provisioner: ebs.csi.aws.com`: Specifies that the AWS EBS CSI driver will handle the provisioning.
  * `reclaimPolicy: Delete`: This is crucial. It ensures that when the associated PVC is deleted, the underlying EBS volume is also deleted from your AWS account.
  * `volumeBindingMode: WaitForFirstConsumer`: This is the recommended setting. It tells Kubernetes to wait until a Pod actually needs the volume before creating it. This allows the scheduler to pick the best node first, ensuring the EBS volume is created in the same Availability Zone as the Pod, which is a requirement for EBS.

Now, apply it to your cluster:

```bash
kubectl apply -f storageclass-ephemeral.yaml
```

### Step 2: Create the Pod with an Ephemeral Volume

Next, we define our Pod. The magic happens in the `.spec.volumes` section. Instead of a `persistentVolumeClaim`, we use `ephemeral`.

Create a file named `pod-ephemeral.yaml`:

```yaml
# pod-ephemeral.yaml
apiVersion: v1
kind: Pod
metadata:
  name: app-ephemeral
spec:
  containers:
    - name: app
      image: public.ecr.aws/amazonlinux/amazonlinux
      command: ["/bin/sh"]
      args: ["-c", "while true; do echo $(date -u) >> /data/out.txt; sleep 5; done"]
      volumeMounts:
        - name: ephemeral-storage
          mountPath: /data
  volumes:
    - name: ephemeral-storage
      ephemeral:
        volumeClaimTemplate:
          spec:
            accessModes: ["ReadWriteOnce"]
            storageClassName: ebs-ephemeral-storage
            resources:
              requests:
                storage: 1Gi
```

The key section here is **`ephemeral.volumeClaimTemplate`**. This is a blueprint for the PVC that Kubernetes will create for us. It looks exactly like a normal PVC manifest, specifying the access mode, the `storageClassName` to use, and the size of the volume.

### Step 3: Deploy and Verify

Now, deploy the Pod:

```bash
kubectl apply -f pod-ephemeral.yaml
```

Wait a minute for the Pod to start and the EBS volume to be provisioned and attached. Then, check the status of your Kubernetes objects.

```bash
kubectl get pods,pvc,pv
```

You will see something amazing in the output:

```
NAME                READY   STATUS    RESTARTS   AGE
pod/app-ephemeral   1/1     Running   0          65s

NAME                                                      STATUS   VOLUME                                     CAPACITY   ACCESS MODES   STORAGECLASS          AGE
persistentvolumeclaim/app-ephemeral-ephemeral-storage   Bound    pvc-1a2b3c4d-5e6f-7a8b-9c0d-1e2f3a4b5c6d   1Gi        RWO            ebs-ephemeral-storage   64s

NAME                                                        CAPACITY   ACCESS MODES   RECLAIM POLICY   STATUS   CLAIM                                     STORAGECLASS          REASON   AGE
persistentvolume/pvc-1a2b3c4d-5e6f-7a8b-9c0d-1e2f3a4b5c6d   1Gi        RWO            Delete           Bound    default/app-ephemeral-ephemeral-storage   ebs-ephemeral-storage            62s
```

Notice that a PVC named `app-ephemeral-ephemeral-storage` was created automatically\! Kubernetes generates the name from the pattern `<Pod Name>-<Volume Name>`. This PVC is "owned" by the `app-ephemeral` Pod.

### Step 4: Validate Functionality

Let's confirm that our application can write to its new EBS volume.

```bash
kubectl exec app-ephemeral -- cat /data/out.txt
```

You should see a list of timestamps, confirming the volume is mounted and writable.

### Step 5: The Ephemeral Lifecycle in Action

Now for the final test. What happens when we delete the Pod?

```bash
kubectl delete pod app-ephemeral
```

Wait a few moments, and check your PVCs again:

```bash
kubectl get pvc
```

**Output:**

```
No resources found in default namespace.
```

The PVC is gone\! Because the Pod was its owner, the Kubernetes garbage collector deleted the PVC. And because our `StorageClass` has `reclaimPolicy: Delete`, the EBS CSI driver proceeded to delete the actual EBS volume from your AWS account, ensuring there are no orphaned resources or unexpected costs.

Finally, clean up the `StorageClass`:

```bash
kubectl delete sc ebs-ephemeral-storage
```

## When to Use Generic Ephemeral Volumes

This pattern is incredibly useful for:

  * **Caching Services:** When you need a large, high-performance cache that exceeds the capacity of a node's local disk (`emptyDir`).
  * **Temporary Workspaces:** For data processing or CI/CD jobs that need a reliable, sized workspace but don't need to persist the data after the job is complete.
  * **Simplified Application Deployment:** When you want the benefits of managed, dynamic storage without the operational overhead of creating and managing PVCs separately from your application's lifecycle.
