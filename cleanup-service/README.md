# Kyverno-Policy-Based Cleanup for Orphaned Kubernetes Services
This repository includes resources for implementing automated detection and cleanup of orphaned services in Kubernetes using Kyverno policies.

## Prerequisites:
- A Kubernetes cluster with Kyverno 1.10 or above installed with the Cleanup Controller enabled.

## Usage:

### RBAC Configuration
For the Kyverno policies to function correctly, they require appropriate permissions to detect, mark, and clean up services across namespaces. Deploy the RBAC configuration:

```bash
kubectl apply -f kyverno-orphaned-service-rbac.yaml
```

### Deploying the Kyverno Policies

1. Deploy the mutation policy that detects and marks orphaned services:
```bash
kubectl apply -f mutate-orphaned-service-policy.yaml
```

2. Deploy the cleanup policy that will delete marked services after a specified duration:
```bash
kubectl apply -f orphaned-service-cleanup-policy.yaml
```

## Detailed Policy Information

### Mutation Policy (`mutate-orphaned-service-policy.yaml`)

This policy contains four key rules that work together to manage orphaned services:

1. **mark-orphaned-services**: 
   - Detects services that have no endpoints
   - Excludes system namespaces (kube-system, kube-public, kyverno) and the kubernetes default service
   - Adds labels and annotations to mark services as orphaned
   - Labels added: `cleanup.resource: marked-for-deletion` and `cleanup.resource/reason: no-endpoints`
   - Includes timestamp and debug information in annotations

2. **generate-event-for-orphaned-service**:
   - Watches for services with the orphaned labels
   - Generates a Kubernetes warning event when a service is marked as orphaned
   - Makes the orphaned services visible in Kubernetes events, making them easier to track

3. **unmark-services-with-endpoints**:
   - Watches for services previously marked as orphaned
   - When endpoints appear, removes the deletion labels and adds recovery annotations
   - Ensures services are no longer targeted for cleanup once they become active again

4. **generate-event-for-recovered-service**:
   - Watches for services with recovery annotations
   - Generates a Kubernetes normal event when a service recovers
   - Provides visibility into service recovery

The policy uses background scanning to continuously monitor services and their endpoints state, applying the rules automatically as conditions change.

### Cleanup Policy (`orphaned-service-cleanup-policy.yaml`)

This policy:
- Targets services marked with the `cleanup.resource: marked-for-deletion` label
- Verifies they've been marked for the specified duration
- Deletes them according to the configured schedule
- Generates reports on each cleanup action for audit purposes

### Configuring Cleanup Timing

You can adjust how long services must be marked as orphaned before deletion and how frequently the cleanup runs by modifying these values in `orphaned-service-cleanup-policy.yaml`:

```yaml
conditions:
  all:
  - key: "{{ time_diff('{{target.metadata.annotations.\"cleanup.resource/marked-time\"}}','{{ time_now_utc() }}') }}"
    operator: GreaterThan
    value: "0h2m0s"  # For testing use 2 minutes. Change to days in production: value: "168h0m0s" (7 days)
schedule: "*/1 * * * *"  # Run every minute
```

* For production environments, consider changing the waiting period to a longer duration (e.g., "168h0m0s" for 7 days)
* Adjust the schedule to run less frequently (e.g., "0 3 * * *" to run daily at 3 AM)

### Configuring Background Scan Interval

For more responsive detection of orphaned services, you can configure the background scan interval. Edit the Kyverno background controller deployment:

```bash
kubectl edit deployment -n kyverno kyverno-background-controller
```

Add the following environment variable to the container spec:

```yaml
- name: BACKGROUND_SCAN_INTERVAL
  value: "1m"  # Set to 1 minute for faster detection
```

This setting controls how frequently Kyverno scans existing resources and applies the policies.

## What the Policies Do

1. **Mutation Policy**: Detects services with no endpoints, marks them with labels and annotations, and generates events.
2. **Cleanup Policy**: Deletes services that have been marked as orphaned for at least the configured duration.

The cleanup policy runs on a schedule and generates cleanup reports for auditing.
