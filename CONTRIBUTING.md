# Contributing to Kubernetes Hands-On Guides

🎉 First off, thank you for considering contributing! 🎉

We welcome all forms of contributions:
- 📝 New guide proposals
- ✏️ Tutorial improvements
- 🐛 Issue reporting
- 🔍 Technical reviews
- 📚 Documentation updates
- 💡 Feature suggestions

## Table of Contents
1. [Ways to Contribute](#ways-to-contribute)
2. [Development Setup](#development-setup)
3. [Blog Contribution Guide](#blog-contribution-guide)
4. [Code Contribution Guide](#code-contribution-guide)
5. [Commit Message Guidelines](#commit-message-guidelines)
6. [Pull Request Process](#pull-request-process)
7. [Review Process](#review-process)
8. [Recognition](#recognition)
9. [Code of Conduct](#code-of-conduct)

## Ways to Contribute

### 1. Reporting Issues
- Use our [issue template](https://github.com/anveshmuppeda/kubernetes/issues/new/choose)
- Clearly describe:
  - Environment (K8s version, cloud provider)
  - Steps to reproduce
  - Expected vs actual behavior
  - Screenshots/logs (if applicable)

### 2. Suggesting New Guides
- Start a [discussion](https://github.com/anveshmuppeda/kubernetes/discussions/new?category=ideas)
- Follow format:
  ```markdown
  ## Proposed Topic
  ### Why Important?
  ### Suggested Approach
  ### Related Concepts
  ```

### 3. Writing Blog-Style Guides
- See detailed [blog guidelines](#blog-contribution-guide)

### 4. Improving Documentation
- Fix typos in existing guides
- Update outdated commands
- Add missing diagrams/visuals
- Improve code examples

## Development Setup

1. **Fork & Clone**
   ```bash
   git clone https://github.com/anveshmuppeda/kubernetes.git
   cd kubernetes
   ```

2. **Create Branch**
   ```bash
   git checkout -b feat/add-<guide-name>
   # or
   git checkout -b fix/update-<guide-name>
   ```

3. **Install Tools**
   - [Hugo](https://gohugo.io/) (for local preview)
   - [Markdown Linter](https://github.com/DavidAnson/markdownlint)
   - [Pre-commit Hooks](https://pre-commit.com/)
   ```bash
   brew install hugo markdownlint-cli pre-commit
   pre-commit install
   ```

4. **Local Preview**
   ```bash
   hugo server -D
   ```

## Blog Contribution Guide

### File Structure
```
topicname/
└── README.md
```

### Front Matter Template
```markdown
---
title: "A Hands-On Guide to Kubernetes [TOPIC]"
date: YYYY-MM-DD
author: "Your Name"
categories: ["Kubernetes", "DevOps"]
tags: ["k8s", "containers", "cloud-native"]
cover:
  image: "/images/covers/kubernetes-pods.png"
  caption: "Kubernetes Pod Architecture"
---
```

### Content Guidelines
1. Use H2/H3 headings for sections
2. Include real-world examples:
   ```bash
   kubectl apply -f deployment.yaml
   ```
3. Add diagrams using [Mermaid](https://mermaid.js.org/) syntax:
   ```mermaid
   graph TD
     A[Client] --> B(Service)
     B --> C[Pod 1]
     B --> D[Pod 2]
   ```
4. Reference official docs:
   ```markdown
   [Kubernetes Documentation](https://kubernetes.io/docs/concepts/)
   ```

## Code Contribution Guide

### Style Requirements
- Kubernetes manifests:
  ```yaml
  apiVersion: apps/v1
  kind: Deployment
  metadata:
    name: nginx-deployment
    labels:
      app: nginx
  ```
- Shell commands:
  ```bash
  kubectl get pods -n monitoring
  ```

### Testing
1. Validate manifests:
   ```bash
   kubectl apply --dry-run=client -f manifest.yaml
   ```
2. Use [Kubeval](https://www.kubeval.com/):
   ```bash
   kubeval manifest.yaml
   ```

### Docker Best Practices
- Always use specific tags:
  ```dockerfile
  FROM nginx:1.25.3-alpine
  ```
- Include health checks:
  ```dockerfile
  HEALTHCHECK --interval=30s --timeout=3s \
    CMD curl -f http://localhost/ || exit 1
  ```

## Commit Message Guidelines
Follow [Conventional Commits](https://www.conventionalcommits.org/):
```
feat: add Horizontal Pod Autoscaler guide
fix: correct kubelet commands in node-components.md
docs: update service-mesh comparison table
chore: update markdown linter rules
```

## Pull Request Process
1. Reference related issue (#123)
2. Include before/after screenshots
3. Update README's blog table:
   ```markdown
   | 44 | YYYY-MM-DD | [Your Guide Title](link) |
   ```
4. Ensure passes:
   ```bash
   markdownlint '**/*.md' -c .markdownlint.json
   ```

## Review Process
- Maintainers will respond within 48 hours
- PRs need 2 approvals before merging
- May request:
  - Technical accuracy review
  - Screenshot updates
  - Additional test cases

## Recognition
Accepted contributions will:
- Be featured in release notes
- Get added to [Project Maintainers](#project-maintainers--contributors)
- Receive social media shoutouts (@AnveshMuppeda)
- Earn special contributor role in discussions

## Code of Conduct
All participants must adhere to our [Code of Conduct](CODE_OF_CONDUCT.md). Please report unacceptable behavior to muppedaanvesh@gmail.com.

---

🙌 Ready to contribute? [Find Good First Issues](https://github.com/anveshmuppeda/kubernetes/issues?q=is%3Aopen+is%3Aissue+label%3A%22good+first+issue%22)

