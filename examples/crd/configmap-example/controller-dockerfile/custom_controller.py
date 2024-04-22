from kubernetes import client, config, watch

def create_configmap(namespace, name, data):
    core_v1_api = client.CoreV1Api()

    configmap = client.V1ConfigMap(
        metadata=client.V1ObjectMeta(namespace=namespace, name=name),
        data=data
    )

    core_v1_api.create_namespaced_config_map(namespace=namespace, body=configmap)

def delete_configmap(namespace, name):
    core_v1_api = client.CoreV1Api()
    core_v1_api.delete_namespaced_config_map(name=name, namespace=namespace)

def main():
    config.load_incluster_config()  # Use in-cluster configuration
    api_instance = client.CustomObjectsApi()
    group = "anvesh.com"  # Update to the correct API group
    version = "v1"  # Update to the correct API version
    namespace = "default"  # Assuming custom resource is in default namespace
    plural = "customconfigmaps"  # Update to the correct plural form of your custom resource

    # Watch for events on custom resource
    resource_version = ""
    while True:
        stream = watch.Watch().stream(
            api_instance.list_namespaced_custom_object,
            group, version, namespace, plural,
            resource_version=resource_version
        )
        for event in stream:
            custom_resource = event['object']
            event_type = event['type']

            # Extract custom resource name
            resource_name = custom_resource['metadata']['name']

            # Extract key-value pairs from the custom resource spec
            resource_data = custom_resource.get('spec', {})

            # Handle events of type ADDED (resource created)
            if event_type == "ADDED":
                create_configmap(namespace=namespace, name=resource_name, data=resource_data)
            # Handle events of type DELETED (resource deleted)
            elif event_type == "DELETED":
                delete_configmap(namespace=namespace, name=resource_name)

            # Update resource_version to resume watching from the last event
            resource_version = custom_resource['metadata']['resourceVersion']

if __name__ == "__main__":
    main()
