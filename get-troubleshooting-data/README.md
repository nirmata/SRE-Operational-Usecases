# Kyverno-Policy-Based Troubleshooting and Resource Management for Kubernetes
This repository includes resources for testing a Kyverno policy designed to initiate a job. This job gathers troubleshooting data (including logs, kubectl describe output, and events from the namespace) from pods that have restarted three times and subsequently creates a Jira ticket.

## Prerequisites:
- A Kubernetes cluster with Kyverno 1.10 or above installed. 

## Usage:

### Building the Image
This process involves building a custom image containing a Python script for extracting pod details. For testing purpose, the same image provided in the policy can be used as well. 

```
# Clone this repository
# Build the custom image with Docker
docker build -t [username]/[image-name]:[tag] -f Dockerfile .

# Push the image to your repository
docker push [username]/[image-name]:[tag]

```
### RBAC Configuration
For the Kyverno generate policy to function correctly, it requires permissions to generate jobs, and the associated service accounts require permissions to retrieve describe outputs, events, and logs of pods across all namespaces. Deploy `cr-generate.yaml` and `readpods-cr-crb.yaml` for this purpose.

### Deploying the Kyverno Policy
The policy can be customized to include appropriate details like the image, Jira server, project key, and issue type based on your setup. Prior to deploying this policy, a secret with your Jira API token has to be created in each namespace, which will be mounted inside the pod as a volume for Jira server authentication. The process of secret creation with jira API token across namespaces can be automated using this Kyverno policy. Additionally, for this policy to work, remove `system:nodes` group from the Kyverno configMap. 

```
kubectl -n <namespace> create secret generic api-token-secret --from-literal=apiToken=<jira token>
```

### Testing
Deploy a sample deployment using `depl-readonlyrootfs.yaml` to simulate a crashing pod scenario. After three restarts, the Kyverno policy will trigger a job to collect troubleshooting data from the crashing pod and create a Jira ticket.

```
kubectl get pods -n abc
NAME                                                              READY   STATUS             RESTARTS        AGE
get-debug-data-nginx-deployment-559458cb7b-kvzkb-ehebp7v5-5qtrp   0/1     Completed          0               59m
nginx-deployment-559458cb7b-kvzkb                                 0/1     CrashLoopBackOff   16 (3m3s ago)   60m
```

### Enhancements
- Implement a cleanup policy to remove all jobs created by this Kyverno policy at scheduled intervals.
- Automatically scale down deployments to 0 replicas for deployments that have experienced more than five restarts.
- Implement generate policy to automatically sync a secret consisting of your jira api token across namespaces to avoid the manual step of creating the secret in every namespace.
