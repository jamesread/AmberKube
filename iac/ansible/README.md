# Ansible layout

- **`ansible.cfg`** — inventory `hosts.yml`, `roles_path`, and **`vault_password_file = .vault_pass`**.
- **`hosts.yml`** — hosts and non-secret **`all.vars`** (no join tokens or SSH keys).
- **`group_vars/all/main.yml`** — maps **`vault_*`** variables to the names playbooks expect.
- **`group_vars/all/vault.yml`** — **your** ansible-vault encrypted file (not in git). Create it from **`group_vars/all/vault.yml.example`**.

## Ansible Vault (required)

Secrets (**`vault_ssh_authorized_key`**, **`vault_kubeadm_join_token`**, **`vault_kubeadm_join_discovery_token_ca_cert_hash`**) must live in an encrypted **`group_vars/all/vault.yml`**. That file is **gitignored** so it is never committed.

### Initialize from the template

```bash
cd iac/ansible

# Option A — edit plaintext, then encrypt
cp group_vars/all/vault.yml.example group_vars/all/vault.yml
${EDITOR:-vi} group_vars/all/vault.yml   # set real key + kubeadm values
ansible-vault encrypt group_vars/all/vault.yml

# Option B — encrypt the example first, then edit inside the vault
ansible-vault encrypt group_vars/all/vault.yml.example --output group_vars/all/vault.yml
ansible-vault edit group_vars/all/vault.yml
```

### Vault password

Create **`iac/ansible/.vault_pass`** with **one line** (your passphrase) and **`chmod 600 .vault_pass`**. That path is **gitignored**.

If you prefer not to use a password file, remove or override **`vault_password_file`** in **`ansible.cfg`** and use **`--ask-vault-pass`**, or set **`ANSIBLE_VAULT_PASSWORD_FILE`** when running playbooks.

### After cloning

Every clone needs its own **`vault.yml`** and **`.vault_pass`**. The committed **`vault.yml.example`** holds **demo-shaped** values only — replace them with real data before relying on playbooks.

## Check

```bash
cd iac/ansible
ansible-inventory --list
ansible all -m debug -a "var=ssh_authorized_key" --limit localhost
```

If **`vault.yml`** is missing, Ansible will report undefined **`vault_*`** variables or vault decrypt errors until you create and encrypt the file as above.
