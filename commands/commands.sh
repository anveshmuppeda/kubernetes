#!/bin/bash

# Function to check if kubectl is installed
check_kubectl() {
    command -v kubectl >/dev/null 2>&1 || { echo >&2 "kubectl is required but not installed. Aborting."; exit 1; }
}

get_namespace(){
    kubectl get namespace | awk '{print $1}'
    read -p "Enter the namespace name from the above list: " namespace
}
# Function to display the menu
display_mian_menu() {
   echo "===== kubectl Pod Commands ====="
   echo "1. Get pods"
   echo "2. Describe resources"
   echo "3. Get logs for a pod"
   echo "4. Delete a pod"
   echo "5. Delete other resources"
   echo "6. Nodes"
   echo "7. Exit"
   echo "==============================="
}
# Function to get pods
get_pods() {
    echo "1. Get pods from all namespaces"
    echo "2. Get pods from specific namespace"
    read -p "Enter your choice (1-2): " podchoice
    case $podchoice in
           1)   echo "Getting pods in all namespaces:"
                kubectl get pods --all-namespaces ;;
           2)   echo "Getting pods from specific namespace:"
                get_namespace
                kubectl get pods -n $namespace ;;
           *) echo "Invalid choice. Please enter a number between 1 and 2." ;;
    esac    
}

# Function to get logs for a pod
get_pod_logs() {

    get_namespace
    kubectl get pod -n $namespace | awk '{print $1}'
    read -p "Enter the name of the pod from the above list: " pod_name
    #calculate the containers count
    container_count=$(kubectl get pod "$pod_name" -o=jsonpath='{.spec.containers[*].name}' | tr -cd ' ' | wc -c)
    # Add 1 to account for the fact that container names are space-separated
    ((container_count++))

    if [ $container_count -eq 1 ]; then
        echo "Fetching logs for pod $pod_name in namespace $namespace:"
        kubectl logs -n $namespace $pod_name
    else
        kubectl get pod "$pod_name" -o=jsonpath='{.spec.containers[*].name}'
        echo -e "\nPod $pod_name has morethan two containers, please select the one of the container from above to view the logs:"
        read container_name
        echo "Fetching logs for pod $pod_name container $container_name in namespace $namespace:"
        kubectl logs -n $namespace $pod_name -c $container_name
    fi
}

# Function to describe a Resource
describe_resource() {
   
    echo "===== Select the resource to be described ====="
    echo "1. Pod"
    echo "2. Deployment"
    echo "3. Satefulset"
    echo "4. Daemonset"
    echo "5. Configmap"
    echo "6. Secret"
    echo "7. Other"
    echo "==============================="
    read -p "Enter your choice (1-5): " choice
       case $choice in
           1)   get_namespace
                kubectl get po -n $namespace  | awk '{print $1}'
                read -p "Enter the name of the pod from above list to describe: " pod_name
                echo "Describing pod $pod_name in namespace $namespace:"
                kubectl describe pod -n $namespace $pod_name ;;
           2)   get_namespace
                kubectl get deploy -n $namespace  | awk '{print $1}'
                read -p "Enter the name of the Deployment from above list to describe:" deploy_name
                echo "Describing Deployment $deploy_name in namespace $namespace:"
                kubectl describe deploy -n $namespace $deploy_name ;;
           3)   get_namespace
                kubectl get sts -n $namespace  | awk '{print $1}'
                read -p "Enter the name of the Satefulset from above list to describe:" sts_name
                echo "Describing Satefulset $sts_name in namespace $namespace:"
                kubectl describe sts -n $namespace $sts_name ;;
           4)   get_namespace
                kubectl get ds -n $namespace  | awk '{print $1}'
                read -p "Enter the name of the Daemonset from above list to describe:" ds_name
                echo "Describing Daemonset $ds_name in namespace $namespace:"
                kubectl describe ds -n $namespace $ds_name ;;
           5)   get_namespace
                kubectl get cm -n $namespace  | awk '{print $1}'
                read -p "Enter the name of the Configmap from above list to describe:" cm_name
                echo "Describing Configmap $cm_name in namespace $namespace:"
                kubectl describe cm -n $namespace $cm_name ;;
           6)   get_namespace
                kubectl get secret -n $namespace  | awk '{print $1}'
                read -p "Enter the name of the Secret from above list to describe:" secret_name
                echo "Describing Secret $secret_name in namespace $namespace:"
                kubectl describe secret -n $namespace $secret_name ;;
           7)   echo "To describe any resources in kubernetes use the below command::" 
                echo "kubectl describe <resource_name> -n <namespace_name>";;
           *) echo "Invalid choice. Please enter a number between 1 and 6." ;;
       esac 
}

# Function to delete a pod
delete_pod() {
    get_namespace
    kubectl get pod -n $namespace | awk '{print $1}'
    read -p "Enter the name of the pod from above list: " pod_name

    read -p "Do you want to proceed with Deleting pod $pod_name in namespace $namespace...? (yes/no): " response
    # Convert the response to lowercase for case-insensitive comparison
    response_lower=$(echo "$response" | tr '[:upper:]' '[:lower:]')

    if [[ "$response_lower" == "yes" || "$response_lower" == "y" ]]; then
        echo "Deleting pod $pod_name in namespace $namespace..."
        kubectl delete pod -n $namespace $pod_name
    elif [[ "$response_lower" == "no" || "$response_lower" == "n" ]]; then
        echo "Deleting pod $pod_name in namespace $namespace is cancelled"
    else
        echo "Invalid response. Please enter 'yes', 'no', 'y', or 'n'."
    fi   
}

# Function to delete a pod
delete_resources() {
    echo "===== Select the resource to be deleted ====="
    echo "1. Deployment"
    echo "2. Satefulset"
    echo "3. Daemonset"
    echo "4. Configmap"
    echo "5. Secret"
    echo "6. Other"
    echo "==============================="
    read -p "Enter your choice (1-5): " choice
       case $choice in
           1)   get_namespace
                kubectl get deploy -n $namespace | awk '{print $1}'
                read -p "Enter the name of the deployment from above list: " deploy_name

                read -p "Do you want to proceed with Deleting Deployment $deploy_name in namespace $namespace...? (yes/no): " response
                # Convert the response to lowercase for case-insensitive comparison
                response_lower=$(echo "$response" | tr '[:upper:]' '[:lower:]')

                if [[ "$response_lower" == "yes" || "$response_lower" == "y" ]]; then
                    echo "Deleting Deployment $deploy_name in namespace $namespace..."
                    kubectl delete deploy -n $namespace $deploy_name
                elif [[ "$response_lower" == "no" || "$response_lower" == "n" ]]; then
                    echo "Deleting Deployment $deploy_name in namespace $namespace is cancelled"
                else
                    echo "Invalid response. Please enter 'yes', 'no', 'y', or 'n'."
                fi ;;
           2)   get_namespace
                kubectl get sts -n $namespace | awk '{print $1}'
                read -p "Enter the name of the Statefulset from above list: " sts_name

                read -p "Do you want to proceed with Deleting Statefulset $sts_name in namespace $namespace...? (yes/no): " response
                # Convert the response to lowercase for case-insensitive comparison
                response_lower=$(echo "$response" | tr '[:upper:]' '[:lower:]')

                if [[ "$response_lower" == "yes" || "$response_lower" == "y" ]]; then
                    echo "Deleting Statefulset $sts_name in namespace $namespace..."
                    kubectl delete sts -n $namespace $sts_name
                elif [[ "$response_lower" == "no" || "$response_lower" == "n" ]]; then
                    echo "Deleting Statefulset $sts_name in namespace $namespace is cancelled"
                else
                    echo "Invalid response. Please enter 'yes', 'no', 'y', or 'n'."
                fi ;;
           3)   get_namespace
                kubectl get ds -n $namespace | awk '{print $1}'
                read -p "Enter the name of the Daemonset from above list: " ds_name

                read -p "Do you want to proceed with Deleting Daemonset $ds_name in namespace $namespace...? (yes/no): " response
                # Convert the response to lowercase for case-insensitive comparison
                response_lower=$(echo "$response" | tr '[:upper:]' '[:lower:]')

                if [[ "$response_lower" == "yes" || "$response_lower" == "y" ]]; then
                    echo "Deleting Daemonset $ds_name in namespace $namespace..."
                    kubectl delete ds -n $namespace $ds_name
                elif [[ "$response_lower" == "no" || "$response_lower" == "n" ]]; then
                    echo "Deleting Daemonset $ds_name in namespace $namespace is cancelled"
                else
                    echo "Invalid response. Please enter 'yes', 'no', 'y', or 'n'."
                fi ;;
           4)   get_namespace
                kubectl get cm -n $namespace | awk '{print $1}'
                read -p "Enter the name of the Configmap from above list: " cm_name

                read -p "Do you want to proceed with Deleting Configmap $cm_name in namespace $namespace...? (yes/no): " response
                # Convert the response to lowercase for case-insensitive comparison
                response_lower=$(echo "$response" | tr '[:upper:]' '[:lower:]')

                if [[ "$response_lower" == "yes" || "$response_lower" == "y" ]]; then
                    echo "Deleting Configmap $cm_name in namespace $namespace..."
                    kubectl delete cm -n $namespace $cm_name
                elif [[ "$response_lower" == "no" || "$response_lower" == "n" ]]; then
                    echo "Deleting Configmap $cm_name in namespace $namespace is cancelled"
                else
                    echo "Invalid response. Please enter 'yes', 'no', 'y', or 'n'."
                fi ;;
           5)   get_namespace
                kubectl get secret -n $namespace | awk '{print $1}'
                read -p "Enter the name of the Secret from above list: " secret_name

                read -p "Do you want to proceed with Deleting Secret $secret_name in namespace $namespace...? (yes/no): " response
                # Convert the response to lowercase for case-insensitive comparison
                response_lower=$(echo "$response" | tr '[:upper:]' '[:lower:]')

                if [[ "$response_lower" == "yes" || "$response_lower" == "y" ]]; then
                    echo "Deleting Secret $secret_name in namespace $namespace..."
                    kubectl delete secret -n $namespace $secret_name
                elif [[ "$response_lower" == "no" || "$response_lower" == "n" ]]; then
                    echo "Deleting Secret $secret_name in namespace $namespace is cancelled"
                else
                    echo "Invalid response. Please enter 'yes', 'no', 'y', or 'n'."
                fi ;;
           6)   echo "To delete any resources in kubernetes use the below command::" 
                echo "kubectl delete <resource_name> -n <namespace_name>";;
           *) echo "Invalid choice. Please enter a number between 1 and 6." ;;
       esac 
}

# Function to get nodes
get_nodes() {
    echo "Getting nodes:"
    kubectl get nodes
}

#getting node names
get_node_name()
{
    kubectl get nodes | awk '{print $1}'
    read -p "Enter the name of the node from above list: " node_name
}

# Function to describe a node
describe_node() {
    get_node_name
    echo "Describing node $node_name:"
    kubectl describe node $node_name
}

# Function to get node status
get_node_status() {
    get_node_name
    command -v jq >/dev/null 2>&1 || { echo >&2 "JQ is required but not installed. Aborting."; }
    echo "Getting status for node $node_name:"
    kubectl get node $node_name -o json | jq '.status.conditions'
}

# Function to get node configuration
get_node_config() {
    get_node_name
    command -v jq >/dev/null 2>&1 || { echo >&2 "JQ is required but not installed. Aborting."; }
    echo "Getting configuration for node $node_name:"
    kubectl get node $node_name -o json | jq '.metadata'
}

# Function to get node events
get_node_events() {
    get_node_name
    echo "Getting events for node $node_name:"
    kubectl get events --field-selector involvedObject.name=$node_name --sort-by=.metadata.creationTimestamp
}

# Function to drain a node (evicting pods)
drain_node() {
    get_node_name
    echo "Draining node $node_name (evicting pods):"
    kubectl drain $node_name --ignore-daemonsets
}

# Function to uncordon (make schedulable) a node
uncordon_node() {
    get_node_name
    echo "Uncordoning (making schedulable) node $node_name:"
    kubectl uncordon $node_name
}

# Function to cordon (make unschedulable) a node
cordon_node() {
    get_node_name
    echo "Cordoning (making unschedulable) node $node_name:"
    kubectl cordon $node_name
}

# Function to view system logs for a node
view_node_logs() {
    get_node_name
    echo "Viewing system logs for node $node_name:"
    kubectl logs -n kube-system $(kubectl get pods -n kube-system --field-selector spec.nodeName=$node_name -o jsonpath='{.items[0].metadata.name}')
}

# Function to view kubelet logs for a node
view_kubelet_logs() {
    get_node_name
    echo "Viewing kubelet logs for node $node_name:"
    kubectl logs -n kube-system $(kubectl get pods -n kube-system --field-selector spec.nodeName=$node_name -o jsonpath='{.items[0].metadata.name}')
}

# Function to get node metrics
get_node_metrics() {
    echo "Node metrics:"
    kubectl top node
}

# Function to get node components (kubelet, proxy, etc.)
get_node_components() {
    get_node_name
    echo "Getting components for node $node_name:"
    kubectl get pods --all-namespaces --field-selector spec.nodeName=$node_name
}

# Function to get node resource usage
get_node_resource_usage() {
    get_node_name
    echo "Getting resource usage for node $node_name:"
    kubectl describe node $node_name | grep -E '(Allocatable|Capacity|Conditions|Addresses|System Info|Non-terminated Pods|Container Runtime Version)'
}

nodes_commands() {
    echo "===== kubectl Worker Node Commands ====="
    echo "1. Get nodes"
    echo "2. Describe a node"
    echo "3. Get node status"
    echo "4. Get node configuration"
    echo "5. Get node events"
    echo "6. Drain a node (evicting pods)"
    echo "7. Cordon(make unschedulable) a node"
    echo "8. Uncordon (make schedulable) a node"
    echo "9. View system logs for a node"
    echo "10. View kubelet logs for a node"
    echo "11. Get node metrics"
    echo "12. Get node components (kubelet, proxy, etc.)"
    echo "13. Get node resource usage"
    echo "========================================"
    read -p "Enter your choice (1-13): " choice

    case $choice in
        1) get_nodes ;;
        2) describe_node ;;
        3) get_node_status ;;
        4) get_node_config ;;
        5) get_node_events ;;
        6) drain_node ;;
        7) cordon_node ;;
        8) uncordon_node ;;
        9) view_node_logs ;;
        10) view_kubelet_logs ;;
        11) get_node_metrics ;;
        12) get_node_components ;;
        13) get_node_resource_usage ;;
        *) echo "Invalid choice. Please enter a number between 1 and 13." ;;
    esac
}

# Main function
main() {
   while true; do
       display_mian_menu
       check_kubectl
       read -p "Enter your choice (1-7): " choice
       
       case $choice in
           1) get_pods ;;
           2) describe_resource ;;
           3) get_pod_logs ;;
           4) delete_pod ;;
           5) delete_resources ;;
           6) nodes_commands ;;
           7) echo "Exiting the script. Goodbye!"; exit 0 ;;
           *) echo "Invalid choice. Please enter a number between 1 and 7." ;;
       esac
   done
}

# Execute the main function
main