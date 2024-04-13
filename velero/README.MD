# Velero  
## Setting up velero backups in kubernetes cluster  

https://velero-backup-anvesh.sfo3.digitaloceanspaces.com



```bash
velero install \
    --provider velero.io/aws \
    --bucket velero-backup-anvesh \
    --plugins velero/velero-plugin-for-aws:v1.3.0,digitalocean/velero-plugin:v1.1.0 \
    --backup-location-config s3Url=https://sfo3.digitaloceanspaces.com,region=sfo3 \
    --use-volume-snapshots=false \
    --secret-file=./cloud-credentials
```

```bash
velero uninstall 
```

https://velero-backup-anvesh.sfo3.digitaloceanspaces.com


```bash
velero install \
    --provider aws \
    --plugins velero/velero-plugin-for-aws:v1.0.0 \
    --bucket velero-backup-anvesh \
    --backup-location-config region=us-east-1 \
    --secret-file ./aws-credentials \
    --pod-annotations iam.amazonaws.com/role=arn:aws:iam::472901755127:user/anvesh \
    --use-volume-snapshots=false 
```



## To check the job logs  

```bash
kubectl logs -l job-name=backup-cronjob-28549554 -n velero
/bin/sh: /scripts/backup_script.sh: Permission denied
```



velero restore create --from-backup testing-backup-do