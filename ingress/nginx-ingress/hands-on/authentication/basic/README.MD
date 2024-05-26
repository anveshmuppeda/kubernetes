# Authentication in Ingress  

## Basic Auth   
### Create htpasswd file  
```bash
$ htpasswd -c auth foo
New password: <bar>
New password:
Re-type new password:
Adding password for user foo
```  

### Convert htpasswd into a secret  
```bash
$ kubectl create secret generic basic-auth --from-file=auth
secret "basic-auth" created
```  

### Testing  
```bash
curl -v http://161.35.240.187/ -H 'Host: foo.bar.com'
```  
