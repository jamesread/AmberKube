# Machine K8s

- **Role path:** [`iac/ansible/roles/machine_k8s`](https://github.com/xconspirisist/kubernetes-homelab/tree/main/iac/ansible/roles/machine_k8s)
- **Description:** Install a k8s node (could be a control/worker).

## Tasks
- Disable SELinux _(ansible.posix.selinux)_
- Flush Handlers _(ansible.builtin.meta)_
- Check if crio is installed _(ansible.builtin.stat)_
- Install Kubernetes if it isn't already
- Install Kubernetes packages _(ansible.builtin.package)_
- Remove unwanted packages _(ansible.builtin.package)_
- Copy k8s modprobe _(ansible.builtin.copy)_
- Modprobe netfilter _(community.general.modprobe)_
- Service - enable and start CRIO _(ansible.builtin.service)_
- Enable IPv4 forwarding via syscyl _(ansible.posix.sysctl)_
- Do something with sysctl (ipv4) _(ansible.posix.sysctl)_
- Do something with sysctl (ipv6) _(ansible.posix.sysctl)_
- Reload, start and enable kubelet _(ansible.builtin.service)_
- Stop and disable resolved _(ansible.builtin.service)_
- Flush Handlers _(ansible.builtin.meta)_
- Remove old systemd-resolved resolv.conf stub _(ansible.builtin.file)_
- Restart network manager to regenerate resolv.conf _(ansible.builtin.service)_
- Flush handlers _(ansible.builtin.meta)_
- Kubeadm pull _(ansible.builtin.command)_
## Files
- `README.md`
- `files/k8s-modprobe.conf`
- `handlers/main.yml`
- `meta/main.yml`
- `tasks/main.yml`
