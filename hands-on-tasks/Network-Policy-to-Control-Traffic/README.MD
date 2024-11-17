### **Complete Steps for Task 3: Implement a Network Policy to Restrict Traffic Between Pods**

#### **Step 1: Create the Namespaces**

1. Create the `frontend` and `backend` namespaces:
   ```bash
   kubectl create namespace frontend
   kubectl create namespace backend
   ```

2. Verify the namespaces:
   ```bash
   kubectl get namespaces
   ```

---

#### **Step 2: Deploy the NGINX Pod in the `backend` Namespace**

1. Create a YAML file for the NGINX pod, `nginx-backend.yaml`:
   ```yaml
   apiVersion: v1
   kind: Pod
   metadata:
     name: nginx-backend
     namespace: backend
     labels:
       app: nginx
   spec:
     containers:
     - name: nginx
       image: nginx
       ports:
       - containerPort: 80
   ```

2. Apply the configuration:
   ```bash
   kubectl apply -f nginx-backend.yaml
   ```

3. Verify that the pod is running:
   ```bash
   kubectl get pods -n backend
   ```

---

#### **Step 3: Create a Service for the Backend Pod**

1. Create a YAML file for the service, `nginx-backend-service.yaml`:
   ```yaml
   apiVersion: v1
   kind: Service
   metadata:
     name: nginx-backend
     namespace: backend
   spec:
     selector:
       app: nginx
     ports:
     - protocol: TCP
       port: 80
       targetPort: 80
   ```

2. Apply the service configuration:
   ```bash
   kubectl apply -f nginx-backend-service.yaml
   ```

3. Verify the service is created and has endpoints:
   ```bash
   kubectl get svc -n backend
   kubectl get endpoints -n backend
   ```

   The endpoints should include the IP of the `nginx-backend` pod.

---

#### **Step 4: Deploy a Busybox Pod in the `frontend` Namespace**

1. Create a YAML file for the Busybox pod, `busybox-frontend.yaml`:
   ```yaml
   apiVersion: v1
   kind: Pod
   metadata:
     name: busybox-frontend
     namespace: frontend
     labels:
       app: busybox
   spec:
     containers:
     - name: busybox
       image: busybox
       command: ["sleep", "3600"]
   ```

2. Apply the configuration:
   ```bash
   kubectl apply -f busybox-frontend.yaml
   ```

3. Verify the pod is running:
   ```bash
   kubectl get pods -n frontend
   ```

---

#### **Step 5: Label the `frontend` Namespace**

The NetworkPolicy requires the `frontend` namespace to have a label `name=frontend`.

1. Add the label to the namespace:
   ```bash
   kubectl label namespace frontend name=frontend
   ```

2. Verify the label is applied:
   ```bash
   kubectl get namespaces --show-labels
   ```

---

#### **Step 6: Create the NetworkPolicy**

1. Create a YAML file for the NetworkPolicy, `network-policy.yaml`:
   ```yaml
   apiVersion: networking.k8s.io/v1
   kind: NetworkPolicy
   metadata:
     name: allow-frontend-to-backend
     namespace: backend
   spec:
     podSelector:
       matchLabels:
         app: nginx
     ingress:
     - from:
       - namespaceSelector:
           matchLabels:
             name: frontend
       ports:
       - protocol: TCP
         port: 80
   ```

2. Apply the NetworkPolicy:
   ```bash
   kubectl apply -f network-policy.yaml
   ```

3. Verify the NetworkPolicy is applied:
   ```bash
   kubectl get networkpolicy -n backend
   ```

---

#### **Step 7: Test Connectivity**

1. **Test from the Allowed Namespace (`frontend`)**:
   Run this command from the `busybox-frontend` pod:
   ```bash
   kubectl exec -n frontend busybox-frontend -- wget -qO- http://nginx-backend.backend.svc.cluster.local
   ```
   - Expected Output: The NGINX default welcome page (HTML content).

2. **Test from a Disallowed Namespace**:
   Create a temporary pod in a different namespace (e.g., `default`) and try accessing the backend:
   ```bash
   kubectl run temp-busybox --image=busybox --restart=Never -- sleep 3600
   kubectl exec temp-busybox -- wget -qO- http://nginx-backend.backend.svc.cluster.local
   ```
   - Expected Output: Connection should fail (timeout).

3. Clean up the temporary pod:
   ```bash
   kubectl delete pod temp-busybox
   ```

---

#### **Step 8: Debugging (If Needed)**

1. If `wget` hangs or fails:
   - Ensure the `frontend` namespace has the correct label:
     ```bash
     kubectl get namespaces --show-labels
     ```
   - Verify the `nginx-backend` service and endpoints:
     ```bash
     kubectl describe svc nginx-backend -n backend
     kubectl get endpoints -n backend
     ```
   - Check the logs of the `nginx-backend` pod:
     ```bash
     kubectl logs -n backend nginx-backend
     ```

2. If DNS doesn’t resolve:
   - Test DNS resolution from the `busybox-frontend` pod:
     ```bash
     kubectl exec -n frontend busybox-frontend -- nslookup nginx-backend.backend.svc.cluster.local
     ```

---

### **Clean Up**

Once done, you can delete all resources:
```bash
kubectl delete namespace frontend backend
```