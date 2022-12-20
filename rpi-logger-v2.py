from kubernetes import client, config

# Configs can be set in Configuration class directly or using helper utility
config.load_kube_config()

api = client.CustomObjectsApi()
resource = api.list_namespaced_custom_object(group="metrics.k8s.io",version="v1beta1", namespace="default", plural="pods")
# print(resource)
for pod in resource["items"]:
    # print(pod)
    print(pod['containers'], "\n")