# Unable to debug my Kubernetes pod using "kubectl debug"  

I have a Kubernetes pod with two containers, and the extra container is encountering problems, leading to a crash loop backoff. In an attempt to debug, I'm using the kubectl debug command. However, I'm facing challenges in identifying and accessing the specific sidecar-container within the debug pod for debugging purposes.

Here's a snippet of my pod manifest:
`apiVersion: v1
kind: Pod
metadata:
  name: nginx-pod
  labels:
    app: nginx
spec:
  containers:
  #Main application container
  - name: nginx-container
    image: nginx:latest
    ports:
      - containerPort: 80
    volumeMounts:
      - name: logs
        mountPath: /var/log/nginx
  #This is sidecar container
  - name: sidecar-container
    image: busybox
    command: ["/bin/sh"]
    args: ["-c", "tail -f /var/log/access.log"]
    volumeMounts:
      - name: logs
        mountPath: /var/log/nginx
  volumes:
    - name: logs
      emptyDir: {}
`

I can get the sidecar-container logs related to above issue but I want to debug it through the debug pod.
`
kubectl logs nginx-pod  -c sidecar-container
tail: can't open '/var/log/access.log': No such file or directory
tail: no files
`
> I intentionally provided an incorrect path for my sidecar container in the manifest file to simulate a failure. This is done for debugging purposes using **kubectl debug**.


And here's the kubectl debug command I'm using, which will create an extra pod to debug:
`
kubectl debug nginx-pod -it --image=busybox:1.28 --share-processes --copy-to=debug-pod
`

Output of the **kubectl debug** command:
`
kubectl debug nginx-pod -it --image=busybox:1.28 --share-processes --copy-to=debug-pod
Defaulting debug container name to debugger-qnnf7.
If you don't see a command prompt, try pressing enter.
/ #
`

Pods status:

```
k get po               
NAME        READY   STATUS             RESTARTS      AGE
debug-pod   2/3     CrashLoopBackOff   1 (12s ago)   15s
nginx-pod   1/2     CrashLoopBackOff   3 (27s ago)   80s
```

[![enter image description here](https://i.stack.imgur.com/CFujq.jpg)](https://i.stack.imgur.com/CFujq.jpg)

[![enter image description here](https://i.stack.imgur.com/vwKs0.png)](https://i.stack.imgur.com/vwKs0.png)


I am able to find the location of the main container within the debug and able to access all the files related main application container.

```
/ # 
/ # ps
PID   USER     TIME  COMMAND
    1 65535     0:00 /pause
    7 root      0:00 nginx: master process nginx -g daemon off;
   35 101       0:00 nginx: worker process
   36 101       0:00 nginx: worker process
   37 101       0:00 nginx: worker process
   38 101       0:00 nginx: worker process
   39 101       0:00 nginx: worker process
   40 101       0:00 nginx: worker process
   41 101       0:00 nginx: worker process
   42 101       0:00 nginx: worker process
   49 root      0:00 sh
   61 root      0:00 ps
/ # 
/ # cd proc/7/root/
(unreachable)/ # ls
bin                   docker-entrypoint.d   home                  mnt                   root                  srv                   usr
boot                  docker-entrypoint.sh  lib                   opt                   run                   sys                   var
dev                   etc                   media                 proc                  sbin                  tmp
(unreachable)/ # cat etc/hostname 
debug-pod
(unreachable)/ # cd var/log/nginx/
(unreachable)/var/log/nginx # ls
access.log  error.log
(unreachable)/var/log/nginx # 
(unreachable)/var/log/nginx #
```

Despite this, I can't seem to locate the sidecar-container within the debug pod. Any insights or guidance on how to effectively debug the additional container in this scenario would be greatly appreciated. **Is it possible** to access the sidecar-container files here to debug?

