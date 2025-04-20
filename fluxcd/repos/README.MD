## Folder Structure  

```bash
./repos
├── app1
│   ├── README.MD
│   ├── deploy
│   │   ├── app1-deployment.yaml
│   │   └── app1-service.yaml
│   └── src
│       ├── Dockerfile
│       └── html
│           ├── index.html
│           ├── k8s-logo.png
│           └── styles.css
├── app2
│   ├── README.MD
│   └── src
│       ├── Dockerfile
│       └── html
│           ├── index.html
│           ├── k8s-logo.png
│           └── styles.css
├── app3
│   ├── README.MD
│   └── charts
│       ├── README.MD
│       └── simple-chart
│           ├── Chart.yaml
│           ├── charts
│           ├── templates
│           │   ├── NOTES.txt
│           │   ├── _helpers.tpl
│           │   ├── deployment.yaml
│           │   ├── hpa.yaml
│           │   ├── ingress.yaml
│           │   ├── service.yaml
│           │   ├── serviceaccount.yaml
│           │   └── tests
│           │       └── test-connection.yaml
│           └── values.yaml
└── infra-repo
    ├── apps
    │   ├── app1
    │   │   ├── README.md
    │   │   ├── gitrepository.yaml
    │   │   └── kustomization.yaml
    │   ├── app2
    │   │   ├── README.md
    │   │   ├── deploy
    │   │   │   ├── app2-deployment.yaml
    │   │   │   └── app2-service.yaml
    │   │   ├── gitrepository.yaml
    │   │   ├── imagepolicy.yaml
    │   │   ├── imagerepository.yaml
    │   │   ├── imageupdateautomation.yaml
    │   │   └── kustomization.yaml
    │   └── app3
    │       ├── README.MD
    │       ├── gitrepository.yaml
    │       ├── helmchart.yaml
    │       └── helmrelease.yaml
    ├── clusters
    │   ├── dev
    │   │   └── flux-system
    │   │       ├── gotk-components.yaml
    │   │       ├── gotk-sync.yaml
    │   │       └── kustomization.yaml
    │   ├── staging
    │   │   └── flux-system
    │   │       └── gotk-components.yaml
    │   └── test
    │       └── flux-system
    │           ├── gotk-components.yaml
    │           ├── gotk-sync.yaml
    │           └── kustomization.yaml
    └── infrastructure

28 directories, 46 files
```