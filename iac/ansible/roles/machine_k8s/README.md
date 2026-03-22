# machine_k8s

Install a k8s node (could be a control/worker).
## Variables
This role does not have any variables.


## Example usage

From `iac/ansible` (see `hosts.yml` for `ansible_host`, `ansible_user`, and `ssh_authorized_key`):

```bash
ansible-playbook playbooks/kubemaster.yml
```

Or in your own playbook:

```yaml
- hosts: kubemaster
  become: true
  roles:
    - role: machine_k8s
```
