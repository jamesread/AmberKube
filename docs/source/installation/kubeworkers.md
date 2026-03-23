# Create kubeworker VMs (libvirt)

**Step 3.1** — Provision Kubernetes **worker** VMs (count from **`kubeworker_count`** in **`hosts.yml`**, default **three**) on a **libvirt hypervisor** using **`iac/ansible/playbooks/create-workers-libvirt.yml`** and the **`create-libvirt-vm`** role. The default disk image is **`Fedora-Server-Guest-Generic-43-1.6.x86_64.qcow2`** (see `iac/ansible/roles/create-libvirt-vm/defaults/main.yml`); override the directory or filename if your image lives elsewhere.

Set **`customize_type`** in **`all.vars`** to **`virt-customize`** (default when unset), **`cloud-init`**, or **`ignition`**. **`virt-customize`** runs **`virt-customize`** only to set **hostname** on each disk image (plus optional **`extraVmCustomise`** / RHEL **`sm register`** in the role), then **`virt-install`**. **`ignition`** is intended for **Fedora CoreOS** with **`kubeworker_ignition_url`** (for example **`http://$KUBEMASTER_IP/config.ign`** after [Step 2.3 — Butane (nginx)](butane-nginx.md)). The role **`get_url`** downloads **`config.ign`** onto the hypervisor and **`virt-install`** passes it with QEMU **`fw_cfg`**. Optional **`kubeworker_ignition_method: smbios`** is experimental. **`cloud-init`** uses a nocloud ISO (typical for Fedora cloud images). **Kubernetes on workers** is **[Step 3.2 — Kubeworker K8s bootstrap](kubeworker-k8s-bootstrap.md)** (inventory group **`kubeworkers`**, **`machine_k8s`**, **`kubeadm join`**), not this playbook.

## Hypervisor (`hosts.yml`)

Under **`children`**, define a group named **`hypervisor`** whose hosts are the machine(s) where **libvirt** runs (and where the base **qcow2** lives). The playbook **`hosts:`** that group. Use **`ansible_host`** / **`ansible_user`** for SSH to a remote box, or put **`localhost`** in **`hypervisor`** with **`ansible_connection: local`** if libvirt runs on the same host you run Ansible from.

Set **`kubeworker_count`** in **`all.vars`** to the number of worker VMs to create (default **3**). The play maps this to the **`create-libvirt-vm`** role’s **`count`**.

Set **`kubeworker_ram_mb`** in **`all.vars`** to RAM per worker in **MiB** (default **4192**). The play passes this as **`ramMb`** to **`virt-install`** (**`--memory`**).

Set **`kubeworker_storage_domain`** in **`all.vars`** to the **directory** where per-VM **`.qcow2`** disks (and cloud-init **`.iso`** files, if used) are stored (your libvirt storage pool path, default **`/var/lib/libvirt/images`**). The playbook passes this as **`libvirt_storage_domain`** to the **`create-libvirt-vm`** role.

Set **`kubeworker_ignition_url`** when **`customize_type`** is **`ignition`**. With **`fw_cfg`** (default), the **hypervisor** must reach this URL when Ansible runs **`get_url`**. Optional **`kubeworker_ignition_validate_certs`** (default **true**) applies to that download when using **https://**.

Define inventory group **`kubeworkers`** under **`children`** when you plan **[Step 3.2](kubeworker-k8s-bootstrap.md)** — **one host per worker** (count must match **`kubeworker_count`**), with **`ansible_host`** as needed. Step 3.1 does **not** use **`kubeworkers`**; only **`kubeworker-k8s-bootstrap.yml`** does.

The playbook **`hosts:`** the **`hypervisor`** inventory group so **`stat`**, **`cp`**, **`qemu-img`**, and **`virt-install`** run on the libvirt machine.

## Prerequisites

- **libvirt** / **KVM** available and usable on the hypervisor (e.g. membership in **`libvirt`** where applicable).
- Packages the role can install or that you already have: **`virt-install`**, **`qemu-img`**, **`genisoimage`**, **`libguestfs-tools`** (see the role tasks under `iac/ansible/roles/create-libvirt-vm/`).
- The **qcow2** image file present under **`baseImageDirectory`** (default in the role: `/jwrFs/Software/PC/OS/`) with the expected **`baseImageFilename`**, or pass a different path when you run the playbook (see below).
- **[Ansible](https://docs.ansible.com/ansible/latest/installation_guide/intro_installation.html)** on the control host, with SSH or local access to the **`hypervisor`** group.
- With **`kubeworker_ignition_method: fw_cfg`** (default), the hypervisor downloads **`config.ign`** for **`virt-install`**; TLS for that download is controlled by **`kubeworker_ignition_validate_certs`**. With **`smbios`**, the guest is expected to fetch via **`ignition.config.url`** (less reliable here).

## Run the playbook

The play uses **`become: true`** (root) so **`dnf`**, **`virt-install`**, and paths under the libvirt image directory can be managed. **`iac/ansible/ansible.cfg`** sets **`become_ask_pass = True`**, so Ansible **prompts for your sudo password** when needed (you can still pass **`--ask-become-pass`** / **`-K`** explicitly, or configure **passwordless sudo** for your user on the hypervisor). For non-interactive runs, set **`ANSIBLE_BECOME_ASK_PASS=false`** and supply credentials another way (for example **`ansible_become_password`** in the vault).

From **`iac/ansible`**, the default **`hosts.yml`** is loaded (including **`all.vars`** such as **`customize_type`**, **`kubeworker_count`**, **`kubeworker_ram_mb`**, **`kubeworker_storage_domain`**, **`kubeworker_ignition_url`**, the **`hypervisor`** group, and the **`kubeworkers`** group for Step 3.2). **Secrets** (**`ssh_authorized_key`**, **`kubeadm_join_token`**, **`kubeadm_join_discovery_token_ca_cert_hash`**) live in **`group_vars/all/vault.yml`** (ansible-vault); see **`iac/ansible/README.md`**. **`kubeadm_join_*`** are used by **`kubeworker-k8s-bootstrap.yml`**, not Step 3.1.

```bash title="Ansible control host"
cd iac/ansible
ansible-playbook playbooks/create-workers-libvirt.yml
```

The playbook sets **`vmCustomize`** from **`customize_type`** (default **`virt-customize`**). It sets **`count`** from **`kubeworker_count`** (default **3** in **`hosts.yml`**), **`ramMb`** from **`kubeworker_ram_mb`** (default **4192**), **`libvirt_storage_domain`** from **`kubeworker_storage_domain`**, **`vmTitle: kubeworker`**, **`diskSize: 8`**, and attaches VMs to the bridge **`br-teratan`** (via **`extraVirtInstall`**). VM names follow the role’s naming pattern (e.g. `kubeworker-01`, …).

## Overrides

Examples (from **`iac/ansible`**):

```bash title="Ansible control host"
# Different folder for the qcow2 image
ansible-playbook playbooks/create-workers-libvirt.yml \
  -e baseImageDirectory=/var/lib/libvirt/images

# Fewer or more workers (overrides hosts.yml kubeworker_count)
ansible-playbook playbooks/create-workers-libvirt.yml -e kubeworker_count=2

# RAM per worker in MiB (overrides hosts.yml kubeworker_ram_mb)
ansible-playbook playbooks/create-workers-libvirt.yml -e kubeworker_ram_mb=8192

# Different libvirt disk directory (overrides hosts.yml kubeworker_storage_domain)
ansible-playbook playbooks/create-workers-libvirt.yml -e kubeworker_storage_domain=/data/libvirt/images

# Ignition URL (use with customize_type=ignition)
ansible-playbook playbooks/create-workers-libvirt.yml -e customize_type=ignition -e kubeworker_ignition_url=http://192.168.1.10/config.ign

# Step 3.2 — machine_k8s + kubeadm join (after VMs exist; define `kubeworkers` in hosts.yml)
ansible-playbook playbooks/kubeworker-k8s-bootstrap.yml
```

To change the **bridge**, **RAM**, or other fixed values, edit **`playbooks/create-workers-libvirt.yml`** or pass variables that the role reads (see **`create-libvirt-vm`** defaults and tasks).

## What happens next

Run **[Step 3.2 — Kubeworker Kubernetes bootstrap](kubeworker-k8s-bootstrap.md)** when you want **`machine_k8s`** and **`kubeadm join`** on Fedora Server / cloud-init workers. With **`customize_type: ignition`**, workers typically get **`kubeadm join`** (or other config) from Ignition served by the kubemaster ([Step 2.3 — Butane (nginx)](butane-nginx.md)); you may still use Step 3.2 if you prefer Ansible-driven join instead.

**Note:** If you change **`config.ign`** on the kubemaster, delete the cached **`kubeworker-ignition.ign`** on the hypervisor or set **`kubeworker_ignition_force_fetch: true`** in **`hosts.yml`** so **`get_url`** downloads again before **`virt-install`**.

After workers join the cluster, continue with [Step 3 — Platform layer (Flux)](platform-layer.md) to deploy platform workloads from **`iac/kubernetes/`** with GitOps.
