# RPI-Logger

A logger that retrieves information about the kubernetes cluster and store them in a csv.

It makes use of the official [kubernetes python client](https://github.com/kubernetes-client/python) to communicate with the Kubernetes cluster.  

It retrieves data about the cluster configuration such as pods, nodes from the Core API and retrieves data about the CPU and memory utilization by utilizing the API of the Kubernetes metrics server.

Note: Authentication into Kuberntes is done via the .kube configuration file stored locally. This can be changed with slight modifications to the code.
