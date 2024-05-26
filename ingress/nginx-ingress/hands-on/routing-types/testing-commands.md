# Commands to test the ingress routings   

## Basic Routing  
#### Syntax  
```bash
curl http://<basic-routing-ingress-url>
```  
#### Example  
```bash
$ curl http://161.35.240.187
$ Welcome to Blogging Application

```  

## Host Based Routing  
#### Syntax  
```bash
curl http://<basic-routing-ingress-url> -H "host: blog.example.com"
curl http://<basic-routing-ingress-url> -H "host: stream.example.com"
```  
#### Example  
```bash
$ curl http://161.35.240.187/ -H "host: blog.example.com"
$ Welcome to Blogging Application  
$ curl http://161.35.240.187/ -H "host: stream.example.com"  
$ Welcome to Streaming Application  
```  

## Path Based Routing  
#### Syntax  
```bash
curl http://<basic-routing-ingress-url>/blog -H "host: my.domain.dom"
curl http://<basic-routing-ingress-url>/stream -H "host: my.domain.dom"
```  
#### Example  
```bash
$ curl http://161.35.240.187/blog -H "host: my.domain.dom"
$ Welcome to Blogging Application  
$ curl http://161.35.240.187/stream -H "host: my.domain.dom"  
$ Welcome to Streaming Application  
```  


curl http://161.35.240.187/ -H "host: anything.anvesh.domain.com"