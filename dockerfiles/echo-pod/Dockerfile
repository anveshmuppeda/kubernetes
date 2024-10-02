# Use a lightweight Nginx base image
FROM nginx:alpine

# # Install bash for dynamic script execution
# RUN apt-get update && apt-get install -y bash

# Copy the HTML, CSS, and image files to the nginx html directory
COPY ./html /usr/share/nginx/html

# Copy the script to inject the pod name
COPY pod_name.sh /usr/local/bin/pod_name.sh

# Make the script executable
RUN chmod +x /usr/local/bin/pod_name.sh

# Add an entrypoint script to dynamically inject pod name
ENTRYPOINT ["/usr/local/bin/pod_name.sh"]

# Expose port 80
EXPOSE 80

# Use nginx default command
CMD ["nginx", "-g", "daemon off;"]