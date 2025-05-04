---
// filepath: /Users/anveshmuppeda/Desktop/anvesh/tech/git/kubernetes/docs/security/vault.md
sidebar_label: "HashiCorp Vault"
sidebar_id: "vault"
sidebar_position: 1
---

# HashiCorp Vault: Secrets Management for Kubernetes

HashiCorp Vault is a tool for securely managing secrets, such as API keys, passwords, and certificates. It provides a centralized solution for storing, accessing, and controlling sensitive data in Kubernetes clusters. This guide provides an overview of Vault, its benefits, and how to integrate it with Kubernetes.

---

<div style={{ backgroundColor: '#f9f9f9', borderLeft: '4px solid #0078d4', padding: '1rem', margin: '1rem 0', borderRadius: '5px' }}>
    <h2 style={{ marginTop: 0 }}>🚧 Work in Progress</h2>
    <p>This page is currently under construction. Please check back later for detailed information about HashiCorp Vault setup and usage in Kubernetes.</p>
</div>

---

## Table of Contents
- [Introduction](#introduction)
- [Why Use HashiCorp Vault?](#why-use-hashicorp-vault)
- [Architecture](#architecture)
- [Installation](#installation)
- [Configuration](#configuration)
- [Best Practices](#best-practices)

---

## Introduction
HashiCorp Vault is a powerful tool for managing secrets in Kubernetes. It provides fine-grained access control, encryption, and auditing capabilities, ensuring that sensitive data is securely stored and accessed.

---

## Why Use HashiCorp Vault?
- **Centralized Secrets Management**: Store and manage secrets in a single, secure location.
- **Dynamic Secrets**: Generate secrets on demand, such as database credentials.
- **Access Control**: Use policies to control who can access specific secrets.
- **Audit Logging**: Track access to secrets for compliance and security purposes.

---

## Architecture
HashiCorp Vault integrates with Kubernetes as follows:
1. **Vault Server**: The central component that stores and manages secrets.
2. **Kubernetes Auth Method**: Allows Kubernetes workloads to authenticate with Vault using service accounts.
3. **Secrets Injection**: Secrets can be injected into pods as environment variables or files.

---

## Installation
> **Note:** Detailed installation steps will be added soon.

---

## Configuration
To configure Vault with Kubernetes, you need to enable the Kubernetes authentication method and define policies. Example configuration:

### Enable Kubernetes Auth Method
```bash
vault auth enable kubernetes
vault write auth/kubernetes/config \
    token_reviewer_jwt="$(cat /var/run/secrets/kubernetes.io/serviceaccount/token)" \
    kubernetes_host="https://$KUBERNETES_PORT_443_TCP_ADDR:443" \
    kubernetes_ca_cert=@/var/run/secrets/kubernetes.io/serviceaccount/ca.crt
``` 
### Define Policy  
```bash
path "secret/data/my-app/*" {
  capabilities = ["read"]
}
```
### Create Role
```bash
vault write auth/kubernetes/role/my-app \
    bound_service_account_names=my-app-sa \
    bound_service_account_namespaces=my-app-namespace \
    policies=my-app-policy \
    ttl=1h
```

--- 
## Best Practices
- Use namespaces to isolate secrets for different applications.
- Regularly rotate secrets to minimize exposure.
- Implement access control policies to restrict access to sensitive data.
- Monitor Vault logs for unauthorized access attempts.
- Use encryption for data at rest and in transit.
- Regularly back up Vault data to prevent data loss.
- Test disaster recovery procedures to ensure quick recovery in case of failure.
- Use dynamic secrets for databases and other services to minimize the risk of credential exposure.

---  
Stay tuned for more detailed information on setting up and using HashiCorp Vault in Kubernetes!