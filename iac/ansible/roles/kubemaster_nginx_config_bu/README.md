# kubemaster_nginx_config_bu

Installs **nginx** and the **butane** CLI on the target host, writes **`{{ nginx_docroot }}/{{ config_bu_filename }}`** from a **Butane** template, runs **`butane … -o {{ nginx_docroot }}/{{ config_ign_filename }}`** to produce Ignition, and configures nginx to serve both on port **80**.

Set **`butane_ssh_authorized_key`** or inventory **`ssh_authorized_key`** to embed a public key for the `core` user in the Butane file.

When **`kubeadm_join_server`**, **`kubeadm_join_token`**, and **`kubeadm_join_discovery_token_ca_cert_hash`** are all set (see **`hosts.yml`** **`all.vars`**), the template adds **`systemd.units`** with **`kubeadm-join.service`** (**`Type=oneshot`**) running **`kubeadm join`**.
