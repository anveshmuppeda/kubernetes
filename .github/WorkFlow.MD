# GitHub Actions "Update README with Kubernetes Blogs" Overview  

## 🚀 Script Overview

This project includes a Python script (`update_readme.py`) that automates updating your `README.md` with **only your Kubernetes‑related Medium posts** in a Markdown table.  

- **Fetch & Filter**: It uses the [feedparser](https://feedparser.readthedocs.io/en/latest/) library to read your Medium RSS feed, then filters entries whose tags include any of your specified categories (e.g. “kubernetes”, “k8s”). 
- **Locate Table Block**: It scans your README for the markers  
  ```md
  <!-- BLOG-POST-LIST:START -->
     …table rows…
  <!-- BLOG-POST-LIST:END -->
  ```  
  and extracts the existing table rows between them. 
- **Preserve & Append**: It keeps all existing rows, then appends only _new_ posts (by comparing URLs) at the end—renumbering each row sequentially.  
- **Rewrite README**: Finally, it stitches the updated table (header + all rows) back into the README between your markers.

**Directory structure** (example):

```
.github/
  scripts/
    update_readme.py
README.md         ← contains your markers & table
```

---

## 🔐 Permissions & Setup

To let GitHub Actions run this script daily and push changes, you need:

1. **Personal Access Token**  
   - Classic PAT with the **`repo`** scope (“Full control of private repositories”) so it can read/write your code and open PRs. 
   - If you also update workflow files, add the **`workflow`** scope.  

2. **Repository‑level Actions Permissions**  
   In **Settings → Actions → General**:  
   - Under **Workflow permissions**, select **Read and write permissions**.  
   - Enable **“Allow GitHub Actions to create and approve pull requests”** if you want the script to open PRs automatically.  

3. **Store Your Token**  
   - Go to **Settings → Secrets and variables → Actions** and click **New repository secret**.  
   - Name it `PAT_TOKEN` and paste your PAT.

4. **Workflow Checklist**  
   Your `.github/workflows/update-readme.yml` should:  
   - **Use your PAT** when checking out/pushing:
     ```yaml
     - uses: actions/checkout@v4
       with:
         token: ${{ secrets.PAT_TOKEN }}
         persist-credentials: false
     ```  
   - **Set up Python** and run your script:
     ```yaml
     - uses: actions/setup-python@v4
       with: { python-version: "3.x" }
     - run: |
         pip install feedparser
         python ./.github/scripts/update_readme.py
     ```  
   - **Commit & Push** changes to your `dev` branch:
     ```yaml
     - run: |
         git config user.name  "Kubernetes Bot"
         git config user.email "kubernetes-bot@yourdomain.com"
         git add README.md
         git commit -m "Update README with latest Kubernetes blogs"
         git push origin dev
     ```

---

With this in place, every day at 4 AM UTC your workflow will fetch new Kubernetes posts, update the table in your README, and push the changes—keeping your blog list always up‑to‑date!


---

# Docker Build, Push, and Update  

## CI/CD Workflow Steps

1. **Trigger Conditions**:
   - Runs when code is pushed to `main` or `fluxcd` branches
   - Also runs when new version tags (`v*`) are created

2. **Build Process**:
   - Checks out the repository code
   - Determines version:
     - Uses tag name for version tags (e.g., `v1.0.0`)
     - Uses first 8 characters of commit SHA for branch pushes
   - Builds Docker image from:
     ```
     fluxcd/repos/app1/src/Dockerfile
     ```
   - Tags image with format: `anvesh35/fluxcd-demo-app1:<version>`
   - Pushes image to Docker Hub

3. **Manifest Update**:
   - Updates deployment YAML with new image tag:
     ```
     fluxcd/repos/app1/deploy/app1-deployment.yaml
     ```
   - Commits the change to `fluxcd` branch with message:
     ```
     "Update image to <version>"
     ```

4. **Required Setup**:
   - Repository secrets needed:
     - `DOCKERHUB_USERNAME` - Your Docker Hub username
     - `DOCKERHUB_TOKEN` - Docker Hub access token
   - Repository permissions:
     - GitHub Actions must have write permissions
     - Branch protection rules must allow Actions to push to `fluxcd` branch

5. **Directory Structure**:
   ```
   /fluxcd/repos/app1/
     ├── src/
     │   └── Dockerfile      # Source Dockerfile
     └── deploy/
         └── app1-deployment.yaml  # Deployment manifest
   ```

This workflow automatically keeps your deployment manifests synchronized with your built images, pushing all changes to the `fluxcd` branch where Flux can detect and apply them.