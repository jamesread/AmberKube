# Installation

These pages walk through bringing up AmberKube in order.

## Step 1 — Overview

You need a **Fedora VM** on your network (clean install), reachable over **SSH** from the machine where you will run **Ansible**, and enough resources for a small Kubernetes control-plane node (see the project README for rough sizing). Install Ansible and the collections referenced in [Step 2.1 — Prepare the kubemaster node](kubemaster.md). For **`iac/ansible`**, create an encrypted **`group_vars/all/vault.yml`** from **`group_vars/all/vault.yml.example`** (that vault file is not in the repo); see **`iac/ansible/README.md`**.

## Step 2 — Infra layer

The **infra layer** is the Kubernetes foundation: the control-plane node (**Kubemaster**) and optional worker nodes (**Kubeworkers**).

### Kubemaster

When the host and tooling are ready, continue with [2.1 — Prepare node](kubemaster.md) (Ansible), [2.2 — Kubeadm init (Flannel)](kubeadm-init-flannel.md), and optionally [2.3 — Butane via nginx](butane-nginx.md) to publish a **`config.bu`** for Fedora CoreOS (ordering of 2.2 vs 2.3 is flexible).

### Kubeworkers

- [3.1 — Create kubeworker VMs](kubeworkers.md) — **`playbooks/create-workers-libvirt.yml`** on the **`hypervisor`** host; **`kubeworker_count`** workers (see **`hosts.yml`**). For **`virt-customize`**, the image is only given a per-VM **hostname** before **`virt-install`** (unless you extend **`extraVmCustomise`** in the role).
- [3.2 — Kubeworker Kubernetes bootstrap](kubeworker-k8s-bootstrap.md) — **`playbooks/kubeworker-k8s-bootstrap.yml`**: **`machine_k8s`** and **`kubeadm join`** on each host in inventory group **`kubeworkers`**. Run after workers are up and reachable by SSH from the Ansible control host.

You can do Kubeworkers in parallel with or after preparing the control plane, depending on your workflow; join tokens must match the cluster you **`kubeadm init`**’d in Step 2.2.

## Step 3 — Platform layer (Flux)

To install **platform layer** workloads using **Flux** (GitOps) from the **`iac/kubernetes/`** tree, see [Step 3 — Platform layer (Flux)](platform-layer.md). The bootstrap instructions use **`flux bootstrap github`** with **environment variables** (**`GITHUB_TOKEN`**, **`GITHUB_OWNER`**, **`GITHUB_REPO`**, **`GIT_BRANCH`**, **`FLUX_SYNC_PATH`**) so you can **`export`** values once and paste the command without editing the line; **`GITHUB_TOKEN`** is a GitHub PAT with access to the target repo (often a fork—the examples default **`GITHUB_OWNER`** / **`GITHUB_REPO`** to **`jamesread`** / **`AmberKube`**). Typically after the API server is reachable and **`kubectl`** works (Step 2.2); worker VMs (Step 3.1) and **`kubeadm join`** (Step 3.2) may come before or after, depending on where you schedule infra components.
