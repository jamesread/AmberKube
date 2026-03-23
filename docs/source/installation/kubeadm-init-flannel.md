# Kubeadm init with Flannel

**Step 2.2** — After [Step 2.1 — Prepare the kubemaster node](kubemaster.md) (Ansible has installed CRI-O, kubelet, and kubeadm packages), run **`kubeadm init`** on the **control-plane VM** and install **[Flannel](https://github.com/flannel-io/flannel)** as the pod network (CNI). Flannel’s default configuration expects the cluster pod CIDR **`10.244.0.0/16`**, which you must pass to **`kubeadm init`** so the two match.

Run these commands **on the kubemaster host** (typically as **`root`** unless you have passwordless `sudo` for all steps).

## Initialize the control plane

Use a **`--pod-network-cidr`** that matches Flannel ( **`10.244.0.0/16`** is the usual choice):

```bash title="kubemaster"
kubeadm init --pod-network-cidr=10.244.0.0/16
```

If the node has several network interfaces and the API server should listen on a specific address, set **`CONTROL_PLANE_IP`** and pass it in, for example:

```bash title="kubemaster"
export CONTROL_PLANE_IP=192.168.1.10
kubeadm init --pod-network-cidr=10.244.0.0/16 --apiserver-advertise-address=$CONTROL_PLANE_IP
```

Keep the **`kubeadm join ...`** line from the command output; you will need it for worker nodes (after [Step 3.1 — Create kubeworker VMs](kubeworkers.md) and installing Kubernetes on those hosts).

## Configure `kubectl` on the control plane

For **`root`**:

```bash title="kubemaster"
export KUBECONFIG=/etc/kubernetes/admin.conf
```

To use **`kubectl`** as a non-root user, copy the admin kubeconfig into your home directory:

```bash title="kubemaster"
mkdir -p "$HOME/.kube"
sudo cp -i /etc/kubernetes/admin.conf "$HOME/.kube/config"
sudo chown "$(id -u):$(id -g)" "$HOME/.kube/config"
```

## Install Flannel

Apply the upstream Flannel manifest (check the [Flannel documentation](https://github.com/flannel-io/flannel/blob/master/Documentation/kubernetes.md) for the current URL if this fails):

```bash title="kubemaster"
kubectl apply -f https://raw.githubusercontent.com/flannel-io/flannel/master/Documentation/kube-flannel.yml
```

Wait until the control plane reports **Ready** and Flannel pods are running:

```bash title="kubemaster"
kubectl get nodes
kubectl get pods -n kube-flannel
```

## What happens next

- Publish a **Butane** file over HTTP on the kubemaster (optional): [Step 2.3 — Butane (nginx)](butane-nginx.md).
- Join **worker** nodes with **`kubeadm join`** (and the same Kubernetes/CRI setup as the control plane). See [Step 3.1 — Create kubeworker VMs](kubeworkers.md) for creating worker VMs, then follow the upstream [joining workers](https://kubernetes.io/docs/setup/production-environment/tools/kubeadm/create-cluster-kubeadm/#join-nodes) flow.
- Install the **platform layer** with **Flux**: [Step 3 — Platform layer (Flux)](platform-layer.md).
- For more detail on **`kubeadm init`** options, see the Kubernetes documentation for [creating a cluster with kubeadm](https://kubernetes.io/docs/setup/production-environment/tools/kubeadm/create-cluster-kubeadm/).

If you change the pod CIDR from **`10.244.0.0/16`**, you must use a Flannel manifest (or configuration) that uses the same range; do not only change the **`kubeadm init`** flag.
