from kubernetes import client, config

# Configs can be set in Configuration class directly or using helper utility
config.load_kube_config()

api = client.CustomObjectsApi()

# Get resource utilization of pods namespaced
def get_res_util_pods_namespaced(namespace):
    resource = api.list_namespaced_custom_object(group="metrics.k8s.io",version="v1beta1", namespace=namespace, plural="pods")

    for pod in resource["items"]:
        # print(pod)
        print(pod['containers'], "\n")


# Get resource utilization of all pods (including kubernetes internal containers)
def get_res_util_pods_all():
    resource = api.list_cluster_custom_object(group="metrics.k8s.io",version="v1beta1", plural="pods")

    for pod in resource["items"]:
        # print(pod)
        print(pod['containers'], "\n")

# Get resource utilization of all nodes
def get_res_util_nodes_all():
    resource = api.list_cluster_custom_object(group="metrics.k8s.io",version="v1beta1", plural="nodes")

    for node in resource["items"]:
        print(node)

# get_res_util_nodes_all()
#
# get_res_util_pods_all()

get_res_util_pods_namespaced("default")