---
// filepath: kubernetes/commands/helm/helm.md
sidebar_label: "Helm Commands"
sidebar_id: "helm"
sidebar_position: 2
---

# Welcome to the Helm Commands Cheatsheet

Helm is a powerful package manager for Kubernetes, allowing you to define, install, and manage Kubernetes applications. This cheatsheet provides a quick reference to common Helm commands and their usage.

## Table of Contents
- [Installing Helm](#installing-helm)
- [Basic Commands](#basic-commands)
- [Working with Charts](#working-with-charts)
- [Helm Repositories](#helm-repositories)
- [Advanced Commands](#advanced-commands)
- [Troubleshooting](#troubleshooting)

---

## Installing Helm
To install Helm, follow the official installation guide:  
```bash
curl https://raw.githubusercontent.com/helm/helm/main/scripts/get-helm-3 | bash  
```
### Verify the installation:  
```bash
helm version
```
This should display the version of Helm installed on your system.  

## Basic Commands
### Initialize Helm (v2 only):  
```bash
helm init
```
### Check Helm version:  
```bash
helm version
```
### List all installed releases:  
```bash
helm list
```
### Install a chart:  
```bash
helm install <release-name> <chart-name>
```
### Uninstall a release:  
```bash
helm uninstall <release-name>
```

## Working with Charts
### Search for charts:  
```bash
helm search repo <chart-name>
```
### Install a chart with custom values:  
```bash
helm install <release-name> <chart-name> -f <values-file.yaml>
```
### Upgrade a release:  
```bash
helm upgrade <release-name> <chart-name>
```
### Rollback a release:  
```bash
helm rollback <release-name> <revision>
```
### Get release information:  
```bash
helm get all <release-name>
```
### Template a chart:  
```bash
helm template <chart-name> -f <values-file.yaml>
```
### Lint a chart:  
```bash
helm lint <chart-name>
```
### Package a chart:  
```bash
helm package <chart-name>
```
### Push a chart to a repository:  
```bash
helm push <chart-name> <repository>
```
### Pull a chart from a repository:  
```bash
helm pull <repository>/<chart-name>
```
### Delete a chart:  
```bash
helm delete <chart-name>
```
### Show chart information:  
```bash
helm show <chart-name>
```

## Helm Repositories  
### Add a repository:  
```bash
helm repo add <repo-name> <repo-url>
```
### Update repositories:  
```bash
helm repo update
```
### List all repositories:  
```bash
helm repo list
```
### Remove a repository:  
```bash
helm repo remove <repo-name>
```