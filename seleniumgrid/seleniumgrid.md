# How Kubernetes Selenium Grid with KEDA works?
### The Issue
If you have any experience with Selenium Grid and Kubernetes you will probably run into an issue with **scaling**. Kubernetes (K8S) works wonders for scaling up and down applications based on their CPU and Memory usage, but it is not so straightforward when it comes down to applications like Selenium Grid.  
  
The Horizontal Pod AutoScaler (**HPA**) that is built into Kubernetes checks (by default) for resource consumption to determine if a deployment needs to be scaled up or down. This becomes an issue for Selenium Grid for a couple reasons:
 1. The browser pods use a variable amount of resources depending on the demand of the current test. This means that all your browser pods may be in use but there isn’t enough CPU usage for the HPA to decide that a scale-up is needed, **leaving tests waiting in the queue unnecessarily**.
 2. When Kubernetes decides to **scale down a deployment** it does so (for the most part) at **random**. You could have 10 tests running on 20 pods and need to scale down. More than likely at least one of the pods asked to terminate will still have a test running, resulting in connection failures
---
## How KEDA Helps
KEDA is a free and open-source Kubernetes event-driven autoscaling solution that extends the feature set of K8S’ HPA.

### Trigger Specification
This specification describes the selenium-grid trigger that scales browser nodes based on number of requests in session queue and the max sessions per grid.

```yaml
triggers:
  - type: selenium-grid
    metadata:
      url: 'http://selenium-grid-url-or-ip:4444/graphql' # Required. Can be ommitted if specified via TriggerAuthentication/ClusterTriggerAuthentication.
      browserName: 'chrome'  # Required
      browserVersion: '91.0' # Optional. Only required when supporting multiple versions of browser in your Selenium Grid.
      activationThreshold: 5 # Optional
```
### Parameter list:
- **url** - Graphql url of your Selenium Grid. Refer to the Selenium Grid’s documentation here to for more info.
- **browserName** - Name of browser that usually gets passed in the browser capability. Refer to the Selenium Grid’s and WebdriverIO’s documentation for more info.
- **browserVersion** - Version of browser that usually gets passed in the browser capability. Refer to the Selenium Grid’s and WebdriverIO’s documentation for more info. (Optional)
- **activationThreshold** - Target value for activating the scaler. Learn more about activation here.(Default: 0, Optional)

### Example
Here is a full example of scaled object definition using Selenium Grid trigger:
```yaml
apiVersion: keda.sh/v1alpha1
kind: ScaledObject
metadata:
  name: selenium-grid-chrome-scaledobject
  namespace: keda
  labels:
    deploymentName: selenium-chrome-node
spec:
  minReplicaCount: 0
  maxReplicaCount: 8
  scaleTargetRef:
    name: selenium-chrome-node
  triggers:
    - type: selenium-grid
      metadata:
        url: 'http://selenium-hub:4444/graphql'
        browserName: 'chrome'
```
**minReplicaCount** and **maxReplicaCount** are the min and maximum pod count you want to have.

The above example will create Chrome browser nodes equal to the requests pending in session queue for Chrome browser.
Which means now we can properly **scale up** based on the actual load on the Selenium Grid, but still **scaling down** doesn't work properly because the nodes are **terminating before it can finish**.  

## Fixing the scaling down issue using the PreStop and Drain  
By using the PresStop and Drain we can fix the scaling down issue.
Here we are going to use a combination of K8s **PreStop** and Selenium Grid’s **Drain** functionality.  

1. PreStop allows us to set a command or chain of commands that is run to completion before the container is told to stop.  
2. Drain tells the selenium browser pod to finish its current test and then shut down.  

Together these look like so in our browser pod yaml:
```yaml
spec:
  template:
    spec:
      ...
      ...
      containers:
        lifecycle:
          preStop:
            exec:
              command: ["/bin/sh", "-c", "curl --request POST 'localhost:5555/se/grid/node/drain' --header 'X-REGISTRATION-SECRET;'; tail --pid=$(pgrep -f '[n]ode --bind-host false --config /opt/selenium/config.toml') -f /dev/null; sleep 30s"]
```

- When the pod is told to **stop**, the **PreStop** command is ran first.  
- We **curl** the localhost of our pod to tell it to drain. The pod will no longer accept new session requests and will finish its current test.   
- We then tail the internal node process that will continue to run until the node has been drained.
- After this we give the pod 30 seconds to finish anything else before giving the full termination command.
- And with that our application can now safely scale down our selenium browser deployments!

#### Drain
Distributor passes the drain command to the appropriate node identified by the node-id. To drain the Node directly, use the cuRL command enlisted below. Drain finishes the ongoing sessions before stopping the Node. 
```
cURL --request POST 'http://<node-URL>/se/grid/node/drain' --header 'X-REGISTRATION-SECRET;'
```
#### PreStop
This container hook is called immediately before a container is terminated due to an API request or management event such as a liveness/startup probe failure, preemption, resource contention and others. 
There are two types of hook handlers that can be implemented for Containers:
1. Exec - Executes a specific command, such as pre-stop.sh, inside the cgroups and namespaces of the Container. Resources consumed by the command are counted against the Container.
2. HTTP - Executes an HTTP request against a specific endpoint on the Container.

