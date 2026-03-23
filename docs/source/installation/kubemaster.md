# Prepare the kubemaster node (Ansible)

**Step 2.1** — Use the Ansible playbook under `iac/ansible` to turn a **clean Fedora VM** on your network into a node that is ready for **`kubeadm init`** (packages, CRI-O, kubelet, and pulling kubeadm images). This is **Layer 0** in AmberKube: it does not create the cluster by itself. Continue with **[Step 2.2 — Kubeadm init (Flannel)](kubeadm-init-flannel.md)** when this playbook has finished. Optionally use **[Step 2.3 — Butane (nginx)](butane-nginx.md)** to serve a generated **`config.bu`** from the kubemaster (before or after Step 2.2).

## Prerequisites

- A Fedora VM reachable by SSH (typically as `root` or another user with `sudo`).
- [Ansible](https://docs.ansible.com/ansible/latest/installation_guide/intro_installation.html) installed on the machine where you run the playbook.
- Collections used by the [`machine_k8s`](../ansible/machine_k8s.md) role:

  ```bash
  ansible-galaxy collection install ansible.posix community.general
  ```

## Configure inventory

Edit **`iac/ansible/hosts.yml`** (next to **`ansible.cfg`**) so Ansible can reach your VM:

- Set **`ansible_host`** to the VM’s IP or DNS name if the inventory hostname does not already resolve from your control machine.
- Set **`ansible_user`** (and SSH keys or `ansible_ssh_private_key_file`) if you do not log in as `root`.
- Set **`vault_ssh_authorized_key`** in **`group_vars/all/vault.yml`** (ansible-vault encrypted; see **`iac/ansible/README.md`**) to your public key line (for example the contents of `~/.ssh/id_ed25519.pub`) if you want the **`machine_k8s`** role to install it for **`authorized_keys`**. The playbook uses **`ssh_authorized_key`**, which is mapped from the vault variable in **`group_vars/all/main.yml`**.

The play targets the **`kubemaster`** group; hosts listed under that group get the role.

## Run the playbook

From the **`iac/ansible`** directory (so **`ansible.cfg`** picks up **`roles/`** and **`hosts.yml`**). The repo’s **`ansible.cfg`** sets **`become_ask_pass`**, so Ansible may prompt for your **sudo** password on the target when **`become`** is required (unless you use passwordless sudo).

```bash
cd iac/ansible
ansible-playbook playbooks/kubemaster.yml
```

If you run Ansible from another working directory, pass **`-i`** and **`--roles-path`** explicitly, or set `ANSIBLE_ROLES_PATH` to include `iac/ansible/roles`.

## What happens next

The playbook applies the **`machine_k8s`** role only. After it completes successfully (reboots may occur depending on SELinux and resolver changes), continue on the VM with **[Step 2.2 — Kubeadm init (Flannel)](kubeadm-init-flannel.md)** to run **`kubeadm init`** and install Flannel. Optionally run **[Step 2.3 — Butane (nginx)](butane-nginx.md)** from your Ansible host to install nginx and serve **`config.bu`** (any time after SSH to the kubemaster works).

For a detailed task list of the role, see [Machine K8s](../ansible/machine_k8s.md).

To provision **libvirt kubeworker** VMs (count from **`kubeworker_count`** in **`hosts.yml`**), see [Step 3.1 — Create kubeworker VMs](kubeworkers.md).

## Ansible version warning

You may see a warning that **`ansible.posix` does not support** your installed Ansible version. That comes from the collection’s declared compatibility range; it is often safe to ignore if the play succeeds. Updating the collection (`ansible-galaxy collection install ansible.posix --upgrade`) may clear the warning.
