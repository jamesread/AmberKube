# Butane `config.bu` via nginx

**Step 2.3** — Install **nginx** and the **`butane`** CLI on the **kubemaster**, render **`config.bu`**, run **`butane`** to produce **`config.ign`**, and serve **both** over **HTTP**. This is useful when provisioning **Fedora CoreOS** (or other flows) that fetch Ignition over your LAN. The cluster does **not** need to be initialized yet: you only need the kubemaster VM from [Step 2.1 — Prepare the kubemaster node](kubemaster.md) reachable by Ansible (you can run this step **before or after** [Step 2.2 — Kubeadm init (Flannel)](kubeadm-init-flannel.md)).

## What gets created

- **`/var/www/html/config.bu`** — minimal **FCOS**-style Butane (`variant` / `version`, `passwd.users` for **`core`**). If **`ssh_authorized_key`** is set (from **ansible-vault** via **`group_vars/all/vault.yml`**, see **`iac/ansible/README.md`**; Step 2.1), or you pass **`butane_ssh_authorized_key`**, the key is embedded under **`ssh_authorized_keys`** for **`core`**.
- If **all three** join variables below are non-empty (**`kubeadm_join_server`** in **`hosts.yml`**; token and hash from vault; or passed with **`-e`**), the Butane file also defines a **`kubeadm-join.service`** **systemd oneshot** that runs **`kubeadm join`** after **`network-online.target`**:
  - **`kubeadm_join_server`** — control plane API address as **`host:port`** (for example **`192.168.1.10:6443`**).
  - **`kubeadm_join_token`** — bootstrap token from **`kubeadm token create`** / **`kubeadm init`** output.
  - **`kubeadm_join_discovery_token_ca_cert_hash`** — CA cert hash for **`--discovery-token-ca-cert-hash`** (hex or full **`sha256:`** form; a **`sha256:`** prefix is added automatically if you omit it).

The node image must already include **`kubeadm`**, **`kubelet`**, and a container runtime (for example the same Kubernetes stack as [Step 2.1](kubemaster.md)); FCOS may need those supplied via **rpm-ostree** / extensions before **`kubeadm join`** can succeed.

- An nginx **`server`** on port **80** (default) serving that document root, with **`text/plain`** for **`/config.bu`** and **`application/vnd.coreos.ignition+json`** for **`/config.ign`**.
- The **`butane`** package (override with **`butane_package`** in the role defaults). The role runs **`butane /var/www/html/config.bu -o /var/www/html/config.ign`** on the kubemaster whenever **`config.bu`** changes or **`config.ign`** is missing.

Ansible role: **`iac/ansible/roles/kubemaster_nginx_config_bu`**.

## Run the playbook

From **`iac/ansible`** (same inventory as Step 2.1):

```bash title="Ansible control host"
cd iac/ansible
ansible-playbook playbooks/kubemaster-nginx-config-bu.yml
```

Optional: pass a public key explicitly:

```bash title="Ansible control host"
ansible-playbook playbooks/kubemaster-nginx-config-bu.yml \
  -e 'butane_ssh_authorized_key="ssh-ed25519 AAAA... you@host"'
```

## Verify

Set **`KUBEMASTER_IP`** to your kubemaster’s reachable address, for example:

```bash title="Client"
export KUBEMASTER_IP=192.168.1.10
```

From any host that can reach that address:

```bash title="Client"
curl -fsS "http://$KUBEMASTER_IP/config.bu" | head
```

You can compile **`config.bu`** to Ignition yourself with the [Butane documentation](https://coreos.github.io/butane/getting-started/); the role already writes **`/var/www/html/config.ign`** on the kubemaster for you.

## What happens next

- Continue with [Step 3.1 — Create kubeworker VMs](kubeworkers.md) if you are creating libvirt workers, or [Step 3 — Platform layer (Flux)](platform-layer.md) once **`kubectl`** is available.

## Check `config.ign` was generated (curl)

After the playbook finishes, with **`KUBEMASTER_IP`** set as in [Verify](#verify), fetch the Ignition JSON and print it with **`jq`** (this fails if the body is not valid JSON):

```bash title="Client"
curl -fsS "http://$KUBEMASTER_IP/config.ign" | jq .
```
