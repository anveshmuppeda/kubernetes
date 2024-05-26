# Self Signed Certs in Ingress  

## These are the steps for self signed certificates.
### Generate the tls.key and tls.crt for our domain using the below command

Here I am using my-self-signed-domain.com as domain.  

```bash
openssl req -x509 -nodes -days 365 -newkey rsa:2048 \
    -out self-signed-tls.crt -keyout self-signed-tls.key \
    -subj "/CN=my-self-signed-domain.com" \
    -reqexts SAN \
    -extensions SAN \
    -config <(cat /etc/ssl/openssl.cnf \
        <(printf "[SAN]\nsubjectAltName=DNS:my-self-signed-domain.com,DNS:*.my-self-signed-domain.com"))
```

### Create Kubernetes secret

```bash
kubectl create secret tls self-signed-tls --key self-signed-tls.key --cert self-signed-tls.crt
```

###  Create Ingress  
Create ingress, make sure you have ingress controller already installed.  

### Check by hitting the URL  
```bash 
curl -v https://178.128.128.44 -H 'Host: my-self-signed-domain.com' -k

```