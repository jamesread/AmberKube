# Kubeworker Kubernetes bootstrap (Step 3.2)

**Step 3.2** — After [Step 3.1 — Create kubeworker VMs](kubeworkers.md), run **`iac/ansible/playbooks/kubeworker-k8s-bootstrap.yml`** to install the **`machine_k8s`** stack (CRI-O, kubelet, **`kubeadm config images pull`**, etc.) on each worker and run **`kubeadm join`** using **`kubeadm_join_*`** from the **ansible-vault** file **`group_vars/all/vault.yml`** (see **`iac/ansible/README.md`**).

The play targets inventory group **`kubeworkers`** (one host per worker). **SSH** must work from the Ansible control host to each host (set **`ansible_host`** if the inventory name does not resolve on your network).

This step is **separate** from VM creation (Step 3.1 only sets **hostname** on the disk when using **`virt-customize`**, unless you extend **`extraVmCustomise`** in the **`create-libvirt-vm`** role).

## Inventory (`hosts.yml` + vault)

Under **`children`**, define **`kubeworkers`** with **one inventory host per worker**. The number of hosts in **`kubeworkers`** must equal **`kubeworker_count`**. Use names that match the libvirt VM names from Step 3.1 (for example **`kubeworker-01`**, **`kubeworker-02`**, …) and set **`ansible_host`** to each guest’s IP when DNS does not resolve the name.

Set **`kubeadm_join_server`** in **`hosts.yml`** **`all.vars`** (non-secret). **`kubeadm_join_token`** and **`kubeadm_join_discovery_token_ca_cert_hash`** are supplied via **`vault_kubeadm_join_token`** and **`vault_kubeadm_join_discovery_token_ca_cert_hash`** in **`group_vars/all/vault.yml`** — same semantics as for [Butane / Ignition](butane-nginx.md) if you use those on FCOS workers.
- **`ansible_user`** per host (often **`root`**) if you do not connect as root by default.

## Run

From **`iac/ansible`**:

```bash title="Ansible control host"
cd iac/ansible
ansible-playbook playbooks/kubeworker-k8s-bootstrap.yml
```

Workers are processed **one at a time** (**`serial: 1`**) because **`machine_k8s`** may reboot the guest.

## What happens next

Verify nodes with **`kubectl get nodes`** on the control plane. Continue with [Step 3 — Platform layer (Flux)](platform-layer.md) when ready.
