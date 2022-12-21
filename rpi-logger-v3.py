import time
import datetime
from kubernetes import client, config

# Configs can be set in Configuration class directly or using helper utility
config.load_kube_config()

custom_obj_api = client.CustomObjectsApi()
core_api = client.CoreV1Api()


def get_data_from_api(namespace):
    timestamp = str(datetime.datetime.now())
    pod_metrics_result = custom_obj_api.list_namespaced_custom_object(group="metrics.k8s.io", version="v1beta1",
                                                                      namespace=namespace, plural="pods")
    node_metrics_result = custom_obj_api.list_cluster_custom_object(group="metrics.k8s.io", version="v1beta1",
                                                                    plural="nodes")
    pods_data = core_api.list_namespaced_pod(namespace)
    nodes_data = core_api.list_node()

    return {"timestamp": timestamp, "pods_data": pods_data, "nodes_data": nodes_data,
            "metrics_data": {"pod_metrics_result": pod_metrics_result, "node_metrics_result": node_metrics_result}}


def get_container_util_sum(pod_data):
    cpu_sum = 0  # cpu_sum will be in nano cores
    mem_sum = 0  # mem_sum will be in Ki
    count_container = 0
    for pod in pod_data:
        for container in pod['containers']:
            cpu_usage = container['usage']['cpu']
            mem_usage = container['usage']['memory']
            if cpu_usage != '0':
                cpu_sum += int(cpu_usage[:-1])
            if mem_usage != 0:
                mem_sum += int(mem_usage[:-2])
            count_container += 1
    return [count_container, cpu_sum, mem_sum]


def get_node_util(master_node_name, nodes_idle, node_metrics):
    master_node_cpu = 0
    master_node_mem = 0
    cpu_idle_sum = 0
    mem_idle_sum = 0

    for node_metric in node_metrics:
        print(node_metric['metadata']['name'])

        if node_metric['metadata']['name'] == master_node_name:
            master_node_cpu = int(node_metric['usage']['cpu'][:-1])
            master_node_mem = int(node_metric['usage']['memory'][:-2])
        elif node_metric['metadata']['name'] in nodes_idle:
            cpu_usage = node_metric['usage']['cpu']
            mem_usage = node_metric['usage']['memory']
            if cpu_usage != '0':
                cpu_idle_sum += int(cpu_usage[:-1])
            if mem_usage != 0:
                mem_idle_sum += int(mem_usage[:-2])

    return [master_node_cpu, master_node_mem], [cpu_idle_sum, mem_idle_sum]


def parse_node_data(nodes_data, pods_data):
    master_node_name = ''
    nodes_all = []
    nodes_active = set()

    for node in nodes_data.items:
        if 'node-role.kubernetes.io/master' in node.metadata.labels.keys():
            master_node_name = node.metadata.labels['kubernetes.io/hostname']
        nodes_all.append(node.metadata.labels['kubernetes.io/hostname'])

    for pod in pods_data.items:
        nodes_active.add(pod.spec.node_name)

    nodes_idle = list(set(nodes_all) ^ nodes_active)

    return master_node_name, nodes_idle


def get_values():
    api_data = get_data_from_api("default")

    timestamp = api_data['timestamp']

    metrics_data = api_data["metrics_data"]
    pod_metrics = metrics_data['pod_metrics_result']['items']
    node_metrics = metrics_data['node_metrics_result']['items']

    master_node_name, nodes_idle = parse_node_data(api_data['nodes_data'], api_data['pods_data'])

    count_nodes_idle = len(nodes_idle)

    master_node_util, node_idle_util = get_node_util(master_node_name, nodes_idle, node_metrics)  # [master_node_cpu, master_node_mem], [cpu_idle_sum, mem_idle_sum]

    container_util_sum = get_container_util_sum(pod_metrics)  # [count_container, cpu_usage, mem_usage]

    output_ls = [timestamp] + container_util_sum + master_node_util + [count_nodes_idle] + node_idle_util
    print(output_ls)


get_values()
