---
sidebar_position: 2
title: Getting Started with Terraform
---

# Terraform Getting Started

This repository demonstrates a step-by-step approach to learning Terraform, from basic concepts to advanced features like modules, remote execution, workspaces, and AWS Secrets Manager integration.

---

## Getting Started

1. **Clone this repository:**
   ```sh
   git clone https://github.com/anveshmuppeda/terraform-getting-started.git
   cd terraform-getting-started
   ```

2. **Follow the section guides below for each example.**

---

## Structure

```
.
├── 001-simple-example
├── 002-var-example
├── 003-aws-provider
├── 004-ec2-app
├── 005-simple-module
├── 006-s3-backend
├── 007-remote-exec
├── 008-workspaces
├── 009-awssm-secret
├── 010-rds-awssm
├── 011-rds-awssm-advanced
├── 012-import-example
├── 013-refresh-example
└── README.md
```

---

## Guide

### 001-simple-example

- **Goal:** Introduce the basic Terraform syntax and workflow.
- **Files:** `main.tf`
- **How to use:**
  1. `cd 001-simple-example`
  2. `terraform init`
  3. `terraform apply`

---

### 002-var-example

- **Goal:** Demonstrate input variables.
- **Files:** `main.tf`, `variables.tf`
- **How to use:**
  1. `cd 002-var-example`
  2. Edit `variables.tf` to set variable defaults or use `-var` on the CLI.
  3. `terraform init`
  4. `terraform apply`

---

### 003-aws-provider

- **Goal:** Configure the AWS provider and use variables.
- **Files:** `main.tf`, `provider.tf`, `variables.tf`, `var.tfvars`
- **How to use:**
  1. `cd 003-aws-provider`
  2. Set your AWS credentials (via env vars or AWS CLI).
  3. `terraform init`
  4. `terraform apply -var-file=var.tfvars`

---

### 004-ec2-app

- **Goal:** Deploy a simple EC2 instance with user data.
- **Files:** `main.tf`, `provider.tf`, `variables.tf`, `terraform.tfvars`
- **How to use:**
  1. `cd 004-ec2-app`
  2. Update `terraform.tfvars` with your AMI ID and key pair.
  3. `terraform init`
  4. `terraform apply`

---

### 005-simple-module

- **Goal:** Introduce modules for reusable infrastructure.
- **Files:** `main.tf`, `modules/ec2-app/main.tf`, `modules/ec2-app/variables.tf`
- **How to use:**
  1. `cd 005-simple-module`
  2. `terraform init`
  3. `terraform apply`

---

### 006-s3-backend

- **Goal:** Use an S3 backend for remote state storage.
- **Files:** `backend.tf`, `main.tf`, `provider.tf`, `variables.tf`, `terraform.tfvars`
- **How to use:**
  1. `cd 006-s3-backend`
  2. Edit `backend.tf` with your S3 bucket details.
  3. `terraform init`
  4. `terraform apply`

---

### 007-remote-exec

- **Goal:** Use `remote-exec` and `file` provisioners to configure EC2 after launch.
- **Files:** `main.tf`, `index.html`, `modules/ec2-app/main.tf`, `modules/ec2-app/variables.tf`
- **How to use:**
  1. `cd 007-remote-exec`
  2. Update variables and `index.html` as needed.
  3. `terraform init`
  4. `terraform apply`

---

### 008-workspaces

- **Goal:** Manage multiple environments using workspaces and variable files.
- **Files:** `main.tf`, `variables.tf`, `dev.tfvars`, `staging.tfvars`, `prod.tfvars`, `modules/ec2-app/main.tf`, `modules/ec2-app/variables.tf`
- **How to use:**
  1. `cd 008-workspaces`
  2. Create/select a workspace:  
     `terraform workspace new dev`  
     `terraform workspace select dev`
  3. Apply with environment-specific variables:  
     `terraform apply -var-file=dev.tfvars`
  4. Repeat for `staging` and `prod` as needed.

---

### 009-awssm-secret

- **Goal:** Use AWS Secrets Manager to inject secrets into your Terraform-managed infrastructure.
- **Files:** `main.tf`, `variables.tf`, `terraform.tfvars`, `modules/ec2-app/main.tf`, `modules/ec2-app/variables.tf`
- **How to use:**
  1. `cd 009-awssm-secret`
  2. Ensure you have a secret named `terraform-demo-secret` in AWS Secrets Manager with a JSON structure (e.g., `{"username": "myappuser"}`).
  3. Update `terraform.tfvars` with your AMI ID, instance type, and other variables as needed.
  4. `terraform init`
  5. `terraform apply`
  6. The EC2 instance will use the secret value (e.g., `username`) as the instance name.

---

### 010-rds-awssm

- **Goal:** Provision an AWS RDS MySQL instance with credentials managed in AWS Secrets Manager using Terraform modules.
- **Files:** 
  - `main.tf`
  - `provider.tf`
  - `modules/secretmanager/main.tf`, `modules/secretmanager/variables.tf`
  - `modules/rds/main.tf`, `modules/rds/variables.tf`
- **How to use:**
  1. `cd 010-rds-awssm`
  2. Edit `main.tf` to set your desired username and password for the secret (or use variables).
  3. `terraform init`
  4. `terraform apply`
  5. After creation, connect to your RDS instance using the endpoint, username, and password stored in Secrets Manager.
  6. Example MySQL connection:
     ```sh
     mysql -h <rds-endpoint> -P 3306 -u <username> -p
     ```
     (You can find `<rds-endpoint>` in the AWS RDS console or Terraform outputs.)

- **Notes:**
  - Make sure your local MySQL client is compatible (MySQL 8.x recommended).
  - The RDS instance will use the credentials stored in AWS Secrets Manager, managed by the `secretmanager` module.
  - Security group and networking setup may be required to allow inbound connections from your IP.

---

### 011-rds-awssm-adv

- **Goal:** Provision an AWS RDS MySQL instance with credentials securely generated and stored in AWS Secrets Manager, and store all DB connection details (host, port, db name, username, password) in a separate secret for application use.
- **Files:** 
  - `main.tf`
  - `modules/secretmanager/main.tf`, `modules/secretmanager/variables.tf`
  - `modules/rds/main.tf`, `modules/rds/variables.tf`
- **How to use:**
  1. `cd 011-rds-awssm-adv`
  2. Edit `main.tf` to set your desired username for the secret (password will be randomly generated).
  3. `terraform init`
  4. `terraform apply`
  5. After creation, you will have:
     - A secret in AWS Secrets Manager with the DB credentials (username & random password).
     - A separate secret in AWS Secrets Manager containing all connection info (endpoint, port, db name, username, password).
     - An RDS instance using these credentials.
  6. Example MySQL connection:
     ```sh
     mysql -h <rds-endpoint> -P 3306 -u <username> -p
     ```
     (You can find `<rds-endpoint>`, username, and password in the connection info secret.)

- **Notes:**
  - The password is generated only once and remains stable unless you taint or change the random password resource.
  - Do **not** overwrite the credentials secret with connection info; always use a separate secret for connection details.
  - Security group and networking setup may be required to allow inbound connections from your IP.

---

### 012-import-example

- **Goal:** Import an existing AWS EC2 instance (created manually) into Terraform management.
- **Files:** 
  - `main.tf`
  - `imported-resources.tf` (generated during import, then merged into `main.tf`)
- **How to use:**
  1. **Create the EC2 instance manually** in the AWS Console.
  2. **Create a `main.tf`** with an import block:
     ```hcl
     import {
       id = "i-0e924e12540ecfa2f"
       to = aws_instance.imported_ec2_example
     }
     ```
  3. Initialize Terraform:
     ```sh
     terraform init
     ```
  4. Generate the resource configuration from the existing instance:
     ```sh
     terraform plan -generate-config-out=imported-resources.tf
     ```
  5. **Move the generated resource configuration** from `imported-resources.tf` into your `main.tf`.
  6. Import the resource into Terraform state:
     ```sh
     terraform import aws_instance.imported_ec2_example i-0e924e12540ecfa2f
     ```
  7. Now, your manually created EC2 instance is managed by Terraform!

- **Notes:**
  - After import, you can manage, update, or destroy the instance using Terraform as you would with any other resource.
  - Always review the generated configuration and adjust tags or settings as needed to match your infrastructure standards.

---

### 013-refresh-example

- **Goal:** Demonstrate how to use `terraform apply -refresh-only` to sync Terraform state with real infrastructure changes made outside of Terraform.
- **Files:** 
  - `main.tf`
- **How to use:**
  1. `cd 013-refresh-example`
  2. Deploy an EC2 instance using `terraform apply`.
  3. Make a manual change to the EC2 instance in the AWS Console (e.g., add or modify a tag).
  4. Run:
     ```sh
     terraform apply -refresh-only
     ```
     This updates the Terraform state file to reflect the real infrastructure.
  5. Run:
     ```sh
     terraform plan
     ```
     Terraform will show any differences between your configuration and the actual state (e.g., tags present in state but not in `main.tf`).
  6. To bring your configuration in sync, manually update your `main.tf` file as needed and run `terraform apply` again.

- **Notes:**
  - `terraform apply -refresh-only` only updates the state file; it does not change your infrastructure or configuration files.
  - Always review and manually update your configuration files to match desired state after using refresh-only.

---

## Prerequisites

- [Terraform](https://www.terraform.io/downloads.html) installed
- AWS account and credentials configured (`aws configure` or environment variables)
- An existing AWS key pair for EC2 instances

---

**Happy Terraforming!**