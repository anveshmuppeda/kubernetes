#  Kubernetes Horizontal Pod Autoscaler (HPA)  

## Increase the load  
Run this in a separate terminal so that the load generation continues and you can carry on with the rest of the steps  
```bash
kubectl run -i --tty load-generator --rm --image=busybox:1.28 --restart=Never -- /bin/sh -c "while sleep 0.01; do wget -q -O- http://php-apache; done"  
```
kubectl -n autoscaling run -i --tty load-generator --rm --image=busybox:1.28 --restart=Never -- /bin/sh -c "while sleep 0.01; do wget -q -O- http://nginx-svc; done" 


### Now run:  
```bash
# type Ctrl+C to end the watch when you're ready
kubectl get hpa php-apache --watch  
```  
