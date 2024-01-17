# Ephemeral Container  

```
kubectl debug nginx-pod -it --image=busybox:1.28 --share-processes --copy-to=extra-container
```