---
// filepath: kubernetes/docs/ai/dashboard-setup.md
sidebar_label: "Kubernetes Dashboard"
sidebar_id: "dashboard-setup"
sidebar_position: 1
---

# Kubernetes Dashboard
### Install

To deploy Dashboard, execute following command:

```shell
kubectl apply -f https://raw.githubusercontent.com/kubernetes/dashboard/v2.7.0/aio/deploy/recommended.yaml
```
### Access

To access Dashboard from your local workstation you must create a secure channel to your Kubernetes cluster. Run the following command:

```shell
kubectl proxy
```
Now access Dashboard at:

[`http://localhost:8001/api/v1/namespaces/kubernetes-dashboard/services/https:kubernetes-dashboard:/proxy/`](
http://localhost:8001/api/v1/namespaces/kubernetes-dashboard/services/https:kubernetes-dashboard:/proxy/).

**NOTE:** If the above link doesn't work, refer in github repo https://github.com/kubernetes/dashboard


## Create An Authentication Token (RBAC)
## Creating sample user

Here we are creating a new user using the Service Account mechanism of Kubernetes, grant this user admin permissions and login to Dashboard using a bearer token tied to this user.

## Creating a Service Account

We are creating Service Account with the name `admin-user` in namespace `kubernetes-dashboard` first.

```yaml
apiVersion: v1
kind: ServiceAccount
metadata:
  name: admin-user
  namespace: kubernetes-dashboard
```

## Creating a ClusterRoleBinding

```yaml
apiVersion: rbac.authorization.k8s.io/v1
kind: ClusterRoleBinding
metadata:
  name: admin-user
roleRef:
  apiGroup: rbac.authorization.k8s.io
  kind: ClusterRole
  name: cluster-admin
subjects:
- kind: ServiceAccount
  name: admin-user
  namespace: kubernetes-dashboard
```

## Getting a Bearer Token

Now we need to find the token we can use to log in. Execute the following command:

```shell
kubectl -n kubernetes-dashboard create token admin-user
```

It should print something like:

```
eyJhbGciOiJSUzI1NiIsImtpZCI6IiJ9..........NYQ
```

Now copy the token and paste it into the `Enter token` field on the login screen.
Click the `Sign in` button and that's it. You are now logged in as an admin.

## Clean up and next steps

Remove the admin `ServiceAccount` and `ClusterRoleBinding` which we created above.

```shell
kubectl -n kubernetes-dashboard delete serviceaccount admin-user
kubectl -n kubernetes-dashboard delete clusterrolebinding admin-user
```
