# Cert Manager

- **Component path:** [`iac/kubernetes/cert-manager`](https://github.com/jamesread/AmberKube/tree/main/iac/kubernetes/cert-manager)
- **Description:** _Manages ACME/PKI certificates via cert-manager controllers._

- **Homepage:** [https://cert-manager.io/](https://cert-manager.io/)
- **Repository:** [https://github.com/cert-manager/cert-manager](https://github.com/cert-manager/cert-manager)
## Deployment Type
- HelmRelease (name: `cert-manager`, namespace: `default`, chart: `cert-manager`, source: `iac/kubernetes/cert-manager/app/cert-manager.yaml`)
## Files
- `app/cert-manager.yaml`
- `app/issuer.yaml`
- `app/kustomization.yaml`
- `app/policy.yaml`
- `app/values.yaml`
- `ks.yaml`
- `metadata.yaml`
