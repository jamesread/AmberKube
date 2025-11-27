# Cert Manager

- **Component path:** [`iac/kubernetes/cert-manager`](https://github.com/xconspirisist/kubernetes-homelab/tree/main/iac/kubernetes/cert-manager)
- **Description:** _Manages ACME/PKI certificates via cert-manager controllers._

- **Homepage:** [https://cert-manager.io/](https://cert-manager.io/)
- **Repository:** [https://github.com/cert-manager/cert-manager](https://github.com/cert-manager/cert-manager)
## Deployment Type
- HelmRelease (name: `cert-manager`, namespace: `default`, chart: `cert-manager`, source: `iac/kubernetes/cert-manager/cert-manager.yaml`)
## Files
- `cert-manager.yaml`
- `issuer.yaml`
- `kustomization.yaml`
- `metadata.yaml`
- `policy.yaml`
- `values.yaml`
