# Nfs

- **Component path:** [`iac/kubernetes/nfs`](https://github.com/xconspirisist/kubernetes-homelab/tree/main/iac/kubernetes/nfs)
- **Description:** _NFS server manifests for shared persistent storage._

- **Homepage:** [https://kubernetes-sigs.github.io/nfs-subdir-external-provisioner/](https://kubernetes-sigs.github.io/nfs-subdir-external-provisioner/)
- **Repository:** [https://github.com/kubernetes-sigs/nfs-subdir-external-provisioner](https://github.com/kubernetes-sigs/nfs-subdir-external-provisioner)
## Deployment Type
- HelmRelease (name: `nfs`, namespace: `default`, chart: `nfs-subdir-external-provisioner`, source: `iac/kubernetes/nfs/nfs.yaml`)
## Files
- `kustomization.yaml`
- `metadata.yaml`
- `nfs.yaml`
