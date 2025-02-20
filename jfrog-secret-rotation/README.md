# Background Controller Setup

This repository provides the necessary configurations to deploy a background controller that periodically scans and synchronizes secrets across namespaces using Kyverno policies.

## Steps to Deploy

### 1. Build and Push the Docker Image
Ensure you have a Dockerfile in the repository and build the image using the following command:
```sh
# Build the Docker image
docker build -t <your-image-name>:<tag> .

# Push the image to your registry (Docker Hub, ECR, etc.)
docker push <your-image-name>:<tag>
```

### 2. Apply Role and RoleBinding for Background Controller
Deploy the necessary RBAC permissions for the background controller:
```sh
kubectl apply -f background-controller-role-rolebinding.yaml
```

### 3. Apply the Kyverno CronJob Policy
This policy will create a cronjob, service account, and necessary permissions to manage secrets.
```sh
kubectl apply -f kyverno-cronjob-policy.yaml
```

### 4. Apply the Sync-Secrets Policy
This policy synchronizes the `jfrog-token` secret across namespaces:
```sh
kubectl apply -f sync-secrets.yaml
```

### 5. Update Background Controller Deployment
Edit the background controller deployment and add the following environment variable to set the scan interval:
```yaml
- name: BACKGROUND_SCAN_INTERVAL
  value: "1m"
```
To edit the deployment, run:
```sh
kubectl edit deployment <background-controller-deployment-name>
```
Replace `<background-controller-deployment-name>` with the actual deployment name in your cluster.

## Verification
Once all resources are applied, verify the setup using:
```sh
kubectl get pods
kubectl get cronjobs
kubectl get secrets -A  # To check if secrets are synced
```

## Cleanup
To remove all deployed resources, use:
```sh
kubectl delete -f background-controller-role-rolebinding.yaml
kubectl delete -f kyverno-cronjob-policy.yaml
kubectl delete -f sync-secrets.yaml
```

## Troubleshooting
- Check logs for any errors:
```sh
kubectl logs -l app=<background-controller-label>
```
- Verify Kyverno policies are applied correctly:
```sh
kubectl get clusterpolicy
```
- Ensure the service account has necessary permissions:
```sh
kubectl get sa
kubectl describe sa <service-account-name>
```

---
This repository is maintained to facilitate the automated synchronization of secrets using Kubernetes and Kyverno policies.


