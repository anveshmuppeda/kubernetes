# How to connect to S3 from EKS using the IAM role for the service account 
TABLE OF CONTENTS
Prerequisites
Create an OIDC provider
Create an IAM policy
Create a service account
Create an IAM Role and attach the policy
Annotate the service account with the IAM role
Testing the connectivity between Pod and S3 Bucket
Conclusion

## Create an OIDC provider
For the EKS cluster created, by default there will be an OIDC issuer URL associated with it. To use the IAM role for the service account, the OIDC provider needs to exist with OIDC issuer URL. To create the OIDC provider, we will use eksctl command line utility.


```
>> eksctl utils associate-iam-oidc-provider --cluster demo-cluster --approve
```
**The demo-cluster is the name of the EKS cluster.**  

To verify if an OIDC provider is created, we need to run the following command.  


```
>> aws iam list-open-id-connect-providers
```  
We will get the below details if the OIDC provider was successfully created.  


```
{
    "OpenIDConnectProviderList": [
        {
            "Arn": "arn:aws:iam::17483678901:oidc-provider/oidc.eks.ap-south-1.amazonaws.com/id/D510BCG4F7E27AM04AZNS95G6914V4A0"
        }
    ]
}
``` 
## Create an IAM policy
Create the file **s3-policy.json** with the below contents.  


```
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Action": "s3:GetObject",
            "Resource": "arn:aws:s3:::demo-bucket"
        }
    ]
}
``` 
We will create an IAM policy to allow access to get the object from the S3 bucket named demo-bucket using the below command.


```
aws iam create-policy --policy-name s3-policy --policy-document file://s3-policy.json
```  
## Create a service account
Create a file demo-service-account.yaml. We have to create a Kubernetes service account with the name demo-sa in the namespace demo-s3 using the below yaml file.

```
apiVersion: v1
kind: ServiceAccount
metadata:
  name: demo-sa
  namespace: demo-s3
```

Now apply the below command to create a service account.
```
kubectl apply -f demo-service-account.yaml
```
## Create an IAM Role and attach the policy
Create a file demo-role-relationship.yaml for the trust policy.


```
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Principal": {
        "Federated": "arn:aws:iam::17483678901:oidc-provider/oidc.eks.ap-south-1.amazonaws.com/id/D510BCG4F7E27AM04AZNS95G6914V4A0"
      },
      "Action": "sts:AssumeRoleWithWebIdentity",
      "Condition": {
        "StringEquals": {
          "oidc.eks.ap-south-1.amazonaws.com/id/D510BCG4F7E27AM04AZNS95G6914V4A0:aud": "sts.amazonaws.com",
          "oidc.eks.ap-south-1.amazonaws.com/id/D510BCG4F7E27AM04AZNS95G6914V4A0:sub": "system:serviceaccount:demo-s3:demo-sa"
        }
      }
    }
  ]
}
```
Once it is done, we need to create the IAM role and attach the trust policy.

```
aws iam create-role --role-name s3-role --assume-role-policy-document file://demo-role-relationship.json"
```
Now, we will attach the IAM policy to the role created above.

```
aws iam attach-role-policy --role-name s3-role --policy-arn=arn:aws:iam::17483678901:policy/s3-policy
```
## Annotate the service account with the IAM role
The service account needs to be annotated to the IAM role using the below command.

```
kubectl annotate serviceaccount -n demo-s3 demo-sa eks.amazonaws.com/role-arn=arn:aws:iam::17483678901:role/s3-role
```
## Testing the connectivity between Pod and S3 Bucket
Create a file s3-demo-deployment.yaml . Notice that, we are using the 'default' service account that does not have access to the S3 bucket as we have only configured access to the 'demo-sa' service account.

```
apiVersion: apps/v1
kind: Deployment
metadata:
  name: nginx
  namespace: demo-s3
spec:
  selector:
    matchLabels:
      app: nginx
  template:
    metadata:
      labels:
        app: nginx
    spec:
      serviceAccountName: default
      initContainers:
      - name: demo-aws-cli
        image: amazon/aws-cli
        command: ['aws', 's3', 'cp', 's3://demo-bucket/test.txt, '-'
      containers:
      - name: my-app
        image: nginx
```
Now, let us run the deployment file using kubectl apply -f s3-demo-deployment.yaml.


```
kubectl get pods -n demo-s3
NAME                                                READY   STATUS    
nginx-8665cf9655-7h5fs                 0/1         Init:CrashLoopBackoff
```
Observe above that, the pod did not come up successfully as the Init container was not able to access the s3 bucker demo-bucket. We can also check this using the below command.

```
kubectl logs -l app=nginx -c demo-aws-cli -n demo-s3

download failed: s3://demo-bucket/test.txt to - An error occurred (403) when calling the HeadObject operation: Forbidden
```
Now, let us change the service account to demo-sa in the init container as shown below.

```
 spec:
      serviceAccountName: demo-sa
      initContainers:
      - name: demo-aws-cli
        image: amazon/aws-cli
        command: ['aws', 's3', 'cp', 's3://demo-bucket/test.txt, '-'
```
Now reapply using the command kubectl apply -f s3-demo-deployment.yaml.

```
NAME                                                READY   STATUS    RESTARTS   AGE
nginx-12455f5f955-9g8gs                    1/1     Running       0               1d
```
Let us verify if it was able to connect to S3 and print the contents in the console.

```
kubectl logs -f nginx-12455f5f955-9g8gs -n demo-s3

Hi!!!! Testing IAM role for a service account.
``` 
As we have used the demo-sa service account, it was able to successfully connect to S3 bucket.

## Conclusion
In this blog, we have seen what is IRSA and how to use it to access the S3 bucket from the EKS pods. We have also seen, how the pod is connected to a particular service account and how it uses IRSA to connect to the S3 bucket.
