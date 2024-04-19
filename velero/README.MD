# Velero  
## Setting up velero backups in kubernetes cluster  

### Install Velero with backup location on Digital Ocean  
```bash
velero install \
    --provider velero.io/aws \
    --bucket velero-backup-anvesh \
    --plugins velero/velero-plugin-for-aws:v1.3.0,digitalocean/velero-plugin:v1.1.0 \
    --backup-location-config s3Url=https://sfo3.digitaloceanspaces.com,region=sfo3 \
    --use-volume-snapshots=false \
    --secret-file=./cloud-credentials
```

### Install Velero with backup location on AWS   
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
 
## To Uninstall the Velero  
```bash
velero uninstall 
```  

## To check the job logs  
```bash
kubectl logs -l job-name=backup-cronjob-28549554 -n velero
/bin/sh: /scripts/backup_script.sh: Permission denied
```

## To restore the cluster from backup  
```bash 
velero restore create --from-backup testing-backup-do
```  