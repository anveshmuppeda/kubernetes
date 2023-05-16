#!/bin/bash
echo "
1. Creating AWS EKS cluster using eksctl.
2. Deploying the Selenium Grid on EKS cluster.
3. Clearing Evicted Pods from specific Namespace.

Please Choose an appropriate option from above."
read operation

akscluster()
{
    read -p "Enter the cluster name: " ekscluster
    read -p "Enter the cluster region: " eksclusterregion
    eksctl create cluster --name={$ekscluster} \
                        --region={$eksclusterregion} \
                        --without-nodegroup
    # Get List of clusters
    eksctl get cluster
    #Create & Associate IAM OIDC Provider for our EKS Cluster
    eksctl utils associate-iam-oidc-provider \
            --region  {$eksclusterregion} \
            --cluster {$ekscluster} \
            --approve
}

seleniumgrid()
{
    helm install --dry-run selenium selenium-grid
    helm install selenium selenium-grid
    sleep 30
    url=$(kubectl get svc -n selenium | grep selenium-hub-svc | awk '{print $4}')
    url+=":4444/graphql"
    url="http://"$url
    #echo "$url"
    helm upgrade selenium selenium-grid --set triggers.metdata.url={$url}
}

deleteevict()
{
    echo "Clearing the Evicted Pods from cluster in specific namespaces"
    read -p "Enter the namespace to delete the evicted pods: " namespace
    cat <<EOF | kubectl get pod -n $namespace | grep Evicted | awk '{print $1}' | xargs kubectl delete pod -n {$namespace}
EOF
    echo "All the evicted pods are cleared in $namespace namespace"
}

#main function call definitions
if [ "$operation" == "1" ]; then
    echo -e "\nInstalling the AWS EKS Clsuter\n"
    #calling askcluster creation functions
    akscluster

elif [ "$operation" == "2" ]; then
    echo -e "\nDeploying the Selenium Grid"
    #calling selenium grid deployment function
    seleniumgrid
elif [ "$operation" == "3" ]; then
    echo -e "\Deleting the Evicted pods from the specific Namespace"
    #calling delete evicted pod function
    deleteevict
else
    echo "Invalid Option"
fi