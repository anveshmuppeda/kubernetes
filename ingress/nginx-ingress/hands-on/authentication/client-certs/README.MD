# Authentication in Ingress  

## Generate the CA Key and Certificate  
```bash
$ openssl req -x509 -sha256 -newkey rsa:4096 -keyout ca.key -out ca.crt -days 356 -nodes -subj '/CN=Anvesh' 

openssl req -x509 -sha256 -newkey rsa:4096 -keyout ca.key -out ca.crt -days 365 -nodes -subj '/CN=Anvesh' -extensions v3_ca

```  

# Generate the Server Key, and Certificate and Sign with the CA Certificate  
```bash
$ openssl req -new -newkey rsa:4096 -keyout server.key -out server.csr -nodes -subj '/CN=ingress-domain.com'
$ openssl x509 -req -sha256 -days 365 -in server.csr -CA ca.crt -CAkey ca.key -set_serial 01 -out server.crt
```  

```bash
openssl req -new -newkey rsa:4096 -keyout server.key -out server.csr -nodes -subj '/CN=ingress-domain.com' -reqexts SAN -config <(cat /etc/ssl/openssl.cnf <(printf "[SAN]\nsubjectAltName=DNS:ingress-domain.com,DNS:*.ingress-domain.com"))
openssl x509 -req -sha256 -days 365 -in server.csr -CA ca.crt -CAkey ca.key -set_serial 01 -out server.crt -extensions SAN -extfile <(cat /etc/ssl/openssl.cnf <(printf "[SAN]\nsubjectAltName=DNS:ingress-domain.com,DNS:*.ingress-domain.com"))
```

# Generate the Client Key, and Certificate and Sign with the CA Certificate
```bash
$ openssl req -new -newkey rsa:4096 -keyout client.key -out client.csr -nodes -subj '/CN=Anvesh'
$ openssl x509 -req -sha256 -days 365 -in client.csr -CA ca.crt -CAkey ca.key -set_serial 02 -out client.crt
```  
```bash
openssl req -new -newkey rsa:4096 -keyout client.key -out client.csr -nodes -subj '/CN=Anvesh' -reqexts SAN -config <(cat /etc/ssl/openssl.cnf <(printf "[SAN]\nsubjectAltName=DNS:Anvesh"))
openssl x509 -req -sha256 -days 365 -in client.csr -CA ca.crt -CAkey ca.key -set_serial 02 -out client.crt -extensions SAN -extfile <(cat /etc/ssl/openssl.cnf <(printf "[SAN]\nsubjectAltName=DNS:Anvesh"))

```

## Generate the CA Key and Certificate 
```bash
openssl req -x509 -nodes -days 365 -newkey rsa:2048 \
    -out self-signed-tls.crt -keyout self-signed-tls.key \
    -subj "/CN=anvesh.com" \
    -reqexts SAN \
    -extensions SAN \
    -config <(cat /etc/ssl/openssl.cnf \
        <(printf "[SAN]\nsubjectAltName=DNS:anvesh.com,DNS:*.anvesh.com"))
```



```bash
$ kubectl create secret generic tls-secret --from-file=tls.crt=server.crt --from-file=tls.key=server.key --from-file=ca.crt=ca.crt
```

### Testing  
```bash
curl -v http://161.35.240.187/ -H 'Host: ingress-domain.com'
```  

















```bash

kubectl get pods -n kube-system | grep nginx-ingress-controller
nginx-ingress-controller-5984b97644-qbwtv   1/1       Running
$ kubectl exec -it -n kube-system nginx-ingress-controller-5984b97644-qbwtv cat /etc/nginx/nginx.conf | grep ssl_client_certificate -A 1
ssl_client_certificate                  /etc/ingress-controller/ssl/default-my-certs.pem;
ssl_verify_client                       on;

```



curl -v https://161.35.240.187/ -H 'Host: ingress-domain.com' --cert client.crt --key client.key -k



curl -k https://161.35.240.187/ -v -H 'Host: meow.com' --cert client.crt --key client.key 



curl -k http://172.17.4.99 -v -H 'Host: external-auth-01.sample.com'


curl https://ingress-domain.com/ --cert client.crt --key client.key -k