# amazon-cloudwatch

A helm chart for CloudWatch Agent to Collect Cluster Metrics

## Installing the Chart

Install or upgrading the amazon-cloudwatch chart with the default configuration:

```sh
helm upgrade --install amazon-cloudwatch \
    --namespace amazon-cloudwatch helm-charts/amazon-cloudwatch \
    --set clusterName=<my-eks-cluster>
```

## Configuration

| Parameter | Description | Default | Required |
| - | - | - | -
| `agentPrefix` | Name of the agent prefix | `cloudwatch-agent` | ✔
| `fluentdPrefix` | Name of the FluentD prefix | `fluentd`
| `namespace` | Namespace where Amazon-CloudWatch is to be deployed | `amazon-cloudwatch` | ✔
| `clusterName` | Name of your cluster | `swbc_c2c_beta_eks-cluster` | ✔
| `logsRegion` | The region of the cluster | `us-east-1` |
| `agent.resources` | Resources configuration of the agent | |
| `agent.image.respository` | Image to deploy for agent | `amazon/cloudwatch-agent` | ✔
| `agent.image.tag` | Image tag to deploy for agent | `1.247346.0b249609` | ✔
| `fluentd.resources` | Resources configuration of the fluentD | |
| `fluentd.image.respository` | Image to deploy for fluentD | `fluent/fluentd-kubernetes-daemonset` | ✔
| `fluentd.image.tag` | Image tag to deploy for fluentD | `v1.7.3-debian-cloudwatch-1.0` | ✔
| `fluentd.initImage.image` | Init container Image to deploy for fluentD | `busybox` | ✔
