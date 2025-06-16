---
// filepath: kubernetes/docs/eks/008-eks-node-viewer.md
sidebar_label: "EKS Node Viewer"
sidebar_position: 8
---  

# EKS Node Viewer: A Hands-On Guide
#### *Visualize and optimize your EKS node usage with this open-source CLI tool.*

![EKS Node Viewer](./img/eks-node-viewer.gif)

## Summary
EKS Node Viewer is an open‑source CLI tool for visualizing scheduled pod resource requests against a node’s allocatable capacity in Amazon EKS clusters, originally built at AWS to showcase workload consolidation with Karpenter. It helps identify under‑ and over‑utilized nodes, driving cost and performance optimization. Installation is straightforward via Homebrew or a Go install, and its rich flag set lets you tailor context, resource types, labels, sorting, and even on‑the‑fly pricing lookups. Key use‑cases include rightsizing clusters, validating consolidation strategies, and enhancing SRE visibility into node utilization.

---

## Introduction

EKS Node Viewer is a CLI tool for visualizing dynamic node usage within a Kubernetes cluster by comparing scheduled pod resource requests to each node’s allocatable capacity, without measuring actual consumption .
It was originally developed as an internal AWS tool to demonstrate consolidation capabilities in Karpenter before being open‑sourced .

---

## Why Use EKS Node Viewer

1. **Immediate Utilization Insights**
   Quickly spot nodes that are under‑utilized (wasting resources) or over‑utilized (risking performance issues) by viewing request vs. capacity .

2. **Optimize Cost and Performance**
   By identifying consolidation opportunities, you can safely reduce node counts or reclaim unused capacity, complementing Karpenter’s autoscaling and spot instance workflows.

3. **Enhanced SRE Visibility**
   Provides a clear, real‑time overview of cluster footprint, aiding incident response and capacity planning.

---

## What It Is & Key Use Cases

* **Visualization of Scheduled Requests**: Shows CPU, memory (and optionally other resources) requests on each node versus what’s allocatable .
* **Consolidation Validation**: Confirm that Karpenter’s consolidation logic places pods optimally and safely drains nodes when needed.
* **Cost Auditing**: With optional pricing lookups, estimate the cost impact of node usage in real‑time (can be disabled if AWS credentials aren’t available) .

---

## Installation

### Homebrew

```bash
brew tap aws/tap
brew install eks-node-viewer
```

This installs the latest stable version via the AWS Homebrew tap .

### Manual (Go)

```bash
go install github.com/awslabs/eks-node-viewer/cmd/eks-node-viewer@latest
```

By default this places the binary in your `GOBIN` (e.g., `~/go/bin`) .

---

## Usage

Run without arguments to inspect all nodes in your current context:

```bash
eks-node-viewer
```

### Key Flags

```bash
Usage of ./eks-node-viewer:
  -attribution
    	Show the Open Source Attribution
  -context string
    	Name of the kubernetes context to use
  -disable-pricing
    	Disable pricing lookups
  -extra-labels string
    	A comma separated set of extra node labels to display
  -kubeconfig string
    	Absolute path to the kubeconfig file (default "~/.kube/config")
  -node-selector string
    	Node label selector used to filter nodes, if empty all nodes are selected
  -node-sort string
    	Sort order for the nodes, either 'creation' or a label name. The sort order can be controlled by appending =asc or =dsc to the value. (default "creation")
  -resources string
    	List of comma separated resources to monitor (default "cpu")
  -style string
    	Three color to use for styling 'good','ok' and 'bad' values. These are also used in the gradients displayed from bad -> good. (default "#04B575,#FFFF00,#FF0000")
  -v	Display eks-node-viewer version
  -version
    	Display eks-node-viewer version
```  

### Examples

```bash
# Standard usage
eks-node-viewer
# Karpenter nodes only
eks-node-viewer --node-selector karpenter.sh/nodepool
# Display both CPU and Memory Usage
eks-node-viewer --resources cpu,memory
# Display extra labels, i.e. AZ
eks-node-viewer --extra-labels topology.kubernetes.io/zone
# Sort by CPU usage in descending order
eks-node-viewer --node-sort=eks-node-viewer/node-cpu-usage=dsc
# Specify a particular AWS profile and region
AWS_PROFILE=myprofile AWS_REGION=us-west-2
```

#### Computed Labels

Use built‑in computed labels to display node metadata:

- `eks-node-viewer/node-age`  
- `eks-node-viewer/node-cpu-usage`  
- `eks-node-viewer/node-memory-usage`  
- `eks-node-viewer/node-pods-usage`  
- `eks-node-viewer/node-ephemeral-storage-usage`

#### Default Options

Create a `~/.eks-node-viewer` file to persist your preferred flags:

```text
# select only Karpenter managed nodes
node-selector=karpenter.sh/nodepool

# display both CPU and memory
resources=cpu,memory

# show the zone and nodepool name by default
extra-labels=topology.kubernetes.io/zone,karpenter.sh/nodepool

# sort so that the newest nodes are first
node-sort=creation=asc

# change default color style
style=#2E91D2,#ffff00,#D55E00
```

---

## Troubleshooting

NoCredentialProviders: no valid providers in chain. Deprecated.
This CLI relies on AWS credentials to access pricing data if you don't use the `--disable-pricing` option. You must have credentials configured via `~/aws/credentials`, `~/.aws/config`, environment variables, or some other credential provider chain.

---

## References
* [GitHub - eks-node-viewer](https://github.com/awslabs/eks-node-viewer) 
* [Containers from the Couch: Workload Consolidation with Karpenter](https://www.youtube.com/watch?v=BnksdJ3oOEs)
* [AWS re:Invent 2022 - Kubernetes virtually anywhere, for everyone](https://www.youtube.com/watch?v=OB7IZolZk78)

