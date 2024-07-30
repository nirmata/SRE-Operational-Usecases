# Kyverno-Policy-Based Troubleshooting and Resource Management for Kubernetes
This repository includes resources for testing a Kyverno policy designed to initiate a job. This job gathers troubleshooting data (including logs, kubectl describe output, and events from the namespace) from pods that have restarted three times.

## Prerequisites:
- A Kubernetes cluster with Kyverno 1.10 or above installed. 

## Usage:

### Building the Image
This process involves building a custom image containing a Python script for extracting pod details. 

```
# Clone this repository
# Build the custom image with Docker
cd SRE-Operational-Usecases/get-troubleshooting-data/get-debug-data/build
docker build -t [username]/[image-name]:[tag] -f Dockerfile .

# Push the image to your repository
docker push [username]/[image-name]:[tag]

```
### RBAC Configuration
For the Kyverno generate policy to function correctly, it requires permissions to generate jobs, and the associated service accounts require permissions to retrieve describe outputs, events, and logs of pods across all namespaces. Deploy `cr-generate.yaml` and `readpods-cr-crb.yaml` for this purpose.

### Deploying the Kyverno Policy
For this policy to work, remove `system:nodes` group from the Kyverno configMap. 

```
kubectl patch configmap kyverno -n kyverno --type=json -p='[{"op": "remove", "path": "/data/excludeGroups"}]'
```

### Testing
Deploy a sample deployment using `depl-readonlyrootfs.yaml` to simulate a crashing pod scenario. After three restarts, the Kyverno policy will trigger a job to collect troubleshooting data from the crashing pod.

```
kubectl get pods -n abc
NAME                                                              READY   STATUS             RESTARTS        AGE
get-debug-data-nginx-deployment-559458cb7b-kvzkb-ehebp7v5-5qtrp   0/1     Completed          0               59m
nginx-deployment-559458cb7b-kvzkb                                 0/1     CrashLoopBackOff   16 (3m3s ago)   60m
```

### Enhancements
- Implement a cleanup policy to remove all jobs created by this Kyverno policy at scheduled intervals.
- Automatically scale down deployments to 0 replicas for deployments that have experienced more than five restarts.
- Implement generate policy to automatically create a jira issue based on the debug information gathered by the job. For more information, see https://github.com/nirmata/SRE-Operational-Usecases/tree/main/get-troubleshooting-data. 
