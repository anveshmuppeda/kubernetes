# Use a lightweight Nginx base image
FROM nginx:alpine

# # Install bash for dynamic script execution
# RUN apt-get update && apt-get install -y bash

# Copy the HTML, CSS, and image files to the nginx html directory
COPY ./html /usr/share/nginx/html

# Expose port 80
EXPOSE 80

# Use nginx default command
CMD ["nginx", "-g", "daemon off;"]