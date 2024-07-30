from kubernetes import client, config
import os
from datetime import datetime

def get_pod_details(api_instance, namespace, pod_name):
    pod = api_instance.read_namespaced_pod(name=pod_name, namespace=namespace)
    describe = f"Name: {pod.metadata.name}\n" \
               f"Namespace: {pod.metadata.namespace}\n" \
               f"Priority: {pod.spec.priority}\n" \
               f"ServiceAccount: {pod.spec.service_account_name}\n" \
               f"Node: {pod.spec.node_name}\n" \
               f"Start Time: {pod.status.start_time}\n" \
               f"Labels: {pod.metadata.labels if pod.metadata.labels else '<none>'}\n" \
               f"Annotations: {pod.metadata.annotations if pod.metadata.annotations else '<none>'}\n" \
               f"Status: {pod.status.phase}\n" \
               f"Node: {pod.spec.node_name}\n" \
               f"Start Time: {pod.status.start_time}\n"    

    for container_status in pod.status.container_statuses:
        describe += f"Container Name: {container_status.name}\n" \
                    f"  Ready: {container_status.ready}\n" \
                    f"  State: {container_status.state}\n" \
                    f"  Last State: {container_status.last_state}\n" \
                    f"  Restart Count: {container_status.restart_count}\n" \
                    f"  Image: {container_status.image}\n" \
                    f"  Image ID: {container_status.image_id}\n" \
                    f"  Container ID: {container_status.container_id}\n"    

    # Volumes
    describe += "\nVolumes:\n"
    if pod.spec.volumes:
        for volume in pod.spec.volumes:
            describe += f"  {volume.name}:\n" \
                        f"    Type: {type(volume).__name__}\n"        
    else:
        describe += "  <none>\n"
        
    # QoS Class
    describe += f"\nQoS Class: {pod.status.qos_class}\n"

    # Tolerations
    describe += "\nTolerations:\n"
    if pod.spec.tolerations:
        for toleration in pod.spec.tolerations:
            describe += f"  Key: {toleration.key if toleration.key else '<none>'}\n" \
                        f"  Operator: {toleration.operator}\n" \
                        f"  Value: {toleration.value if toleration.value else '<none>'}\n" \
                        f"  Effect: {toleration.effect}\n" \
                        f"  Toleration Seconds: {toleration.toleration_seconds if toleration.toleration_seconds else 'Not specified'}\n"
    else:
        describe += "  <none>\n"

    return describe

def get_pod_events(api_instance, namespace, pod_name):
    field_selector = f"involvedObject.name={pod_name},involvedObject.namespace={namespace}"
    events = api_instance.list_namespaced_event(namespace=namespace, field_selector=field_selector)
    events_str = "\n".join([f"{event.last_timestamp}: {event.message}" for event in events.items])
    
    return events_str

def dump_data_to_file(namespace, pod_name, logs, describe, events):
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    temp_dir = f"/tmp/{pod_name}_{timestamp}"
    os.makedirs(temp_dir, exist_ok=True)
    
    with open(f"{temp_dir}/logs.txt", "w") as f:
        f.write(logs)
    with open(f"{temp_dir}/describe.txt", "w") as f:
        f.write(describe)
    with open(f"{temp_dir}/events.txt", "w") as f:
        f.write(events)
    
    print(f"Data dumped to {temp_dir}")

def get_pod_info(namespace, pod_name):
    config.load_incluster_config()
    api_instance = client.CoreV1Api()
    
    logs = api_instance.read_namespaced_pod_log(name=pod_name, namespace=namespace)
    describe = get_pod_details(api_instance, namespace, pod_name)
    events = get_pod_events(api_instance, namespace, pod_name)
    
    return logs, describe, events

def main(namespace, pod_name):
    logs, describe, events = get_pod_info(namespace, pod_name)
    print(f"=== Logs for {pod_name} in {namespace} ===\n{logs}\n")
    print(f"=== Describe output for {pod_name} in {namespace} ===\n{describe}\n")
    print(f"=== Events in {namespace} ===\n{events}\n")
    dump_data_to_file(namespace, pod_name, logs, describe, events)

if __name__ == "__main__":
    import sys
    if len(sys.argv) != 3:
        print("Usage: script.py <namespace> <pod_name>")
        sys.exit(1)
    
    namespace = sys.argv[1]
    pod_name = sys.argv[2]
    main(namespace, pod_name)
