# Kubernetes-based Event Driven Autoscaler
## What is KEDA?
KEDA is a Kubernetes-based Event Driven Autoscaler. With KEDA, you can drive the scaling of any container in Kubernetes based on the number of events needing to be processed.

KEDA is a single-purpose and lightweight component that can be added into any Kubernetes cluster. KEDA works alongside standard Kubernetes components like the Horizontal Pod Autoscaler and can extend functionality without overwriting or duplication. With KEDA you can explicitly map the apps you want to use event-driven scale, with other apps continuing to function. This makes KEDA a flexible and safe option to run alongside any number of any other Kubernetes applications or frameworks.
## Deploying KEDA with Helm {#helm}

### Install

Deploying KEDA with Helm is very simple:

1. Add Helm repo

    ```sh
    helm repo add kedacore https://kedacore.github.io/charts
    ```

2. Update Helm repo

    ```sh
    helm repo update
    ```

3. Install `keda` Helm chart

    **Helm 3**

    ```sh
    kubectl create namespace keda
    helm install keda kedacore/keda --namespace keda
    ```
Ref:   
https://github.com/kedacore/keda/blob/main/tests/scalers/memory/memory_test.go  
https://keda.sh/docs/2.10/scalers/memory/
