# Descheduler

- **Component path:** [`iac/kubernetes/descheduler`](https://github.com/jamesread/AmberKube/tree/main/iac/kubernetes/descheduler)
- **Description:** _Kubernetes Descheduler that periodically evicts pods to rebalance nodes._

- **Homepage:** [https://kubernetes-sigs.github.io/descheduler/](https://kubernetes-sigs.github.io/descheduler/)
- **Repository:** [https://github.com/kubernetes-sigs/descheduler](https://github.com/kubernetes-sigs/descheduler)
## Deployment Type
- HelmRelease (name: `descheduler`, namespace: `default`, chart: `descheduler`, source: `iac/kubernetes/descheduler/app/descheduler.yaml`)
## Files
- `app/descheduler.yaml`
- `app/kustomization.yaml`
- `ks.yaml`
- `metadata.yaml`
