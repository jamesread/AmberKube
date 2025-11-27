# Descheduler

- **Component path:** [`iac/kubernetes/descheduler`](https://github.com/xconspirisist/kubernetes-homelab/tree/main/iac/kubernetes/descheduler)
- **Description:** _Kubernetes Descheduler that periodically evicts pods to rebalance nodes._

- **Homepage:** [https://kubernetes-sigs.github.io/descheduler/](https://kubernetes-sigs.github.io/descheduler/)
- **Repository:** [https://github.com/kubernetes-sigs/descheduler](https://github.com/kubernetes-sigs/descheduler)
## Deployment Type
- HelmRelease (name: `descheduler`, namespace: `default`, chart: `descheduler`, source: `iac/kubernetes/descheduler/descheduler.yaml`)
## Files
- `descheduler.yaml`
- `kustomization.yaml`
- `metadata.yaml`
