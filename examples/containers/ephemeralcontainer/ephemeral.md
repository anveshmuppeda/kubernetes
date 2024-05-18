# Ephemeral Container  

## Debugging the exited containers  
```
kubectl debug EXISTINGPODNAME -it --image=DEBUGGERIMAGENAME:TAG --share-process --copy-to=COPIED_PODNAME
```
e.g.:  
```
kubectl debug ephemeral-demo-2 -it --image=busybox:1.28 --share-processes --copy-to=debug-ephemeral-demo-2
```

## Debugging the running containers  
```
kubectl debug -it EXISTINGPODNAME --image=DEBUGGERIMAGENAME:TAG --target=EXISTINGCONTAINERNAME
```  
e.g.  

```
kubectl debug -it ephemeral-demo --image=busybox:1.28 --target=ephemeral-demo
```  