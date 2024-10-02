#!/bin/sh
## Change to bash if your using nginx image, since alpine uses sh I am using /bin/sh

# Get the hostname (which is the pod name in Kubernetes)
POD_NAME=$(hostname)
POD_NAME=${POD_NAME:-"Unknown Pod Name"}  # Set default to "Unknown Pod" if hostname fails

# Get the node name from env variables
NODE_NAME=${NODE_NAME:-"Unknown Node Name"}  # Set default to "Unknown Node" if not provided

# Replace the placeholders in the HTML with the actual pod name and node name
sed -i "s/{{POD_NAME}}/${POD_NAME}/g" /usr/share/nginx/html/index.html
sed -i "s/{{NODE_NAME}}/${NODE_NAME}/g" /usr/share/nginx/html/index.html

# Start Nginx
nginx -g 'daemon off;'
