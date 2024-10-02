FROM ubuntu:18.04  

#maintainer
LABEL maintainer="Anvesh Muppeda" 

#install nginx
RUN  apt-get -y update && apt-get -y install nginx

#copying files
COPY default /etc/nginx/sites-available/default
COPY . /usr/share/nginx/html/

#exposing the port
EXPOSE 80
CMD ["/usr/sbin/nginx", "-g", "daemon off;"]