# Kube Dashboard

- **Component path:** [`iac/kubernetes/kube-dashboard`](https://github.com/xconspirisist/kubernetes-homelab/tree/main/iac/kubernetes/kube-dashboard)
- **Description:** _Kubernetes Dashboard web UI and supporting manifests._

- **Homepage:** [https://kubernetes.io/docs/tasks/access-application-cluster/web-ui-dashboard/](https://kubernetes.io/docs/tasks/access-application-cluster/web-ui-dashboard/)
- **Repository:** [https://github.com/kubernetes/dashboard](https://github.com/kubernetes/dashboard)
## Deployment Type
- HelmRelease (name: `kube-dashboard`, namespace: `default`, chart: `kubernetes-dashboard`, source: `iac/kubernetes/kube-dashboard/kube-dashboard.yaml`)
## Files
- `ks.yaml`
- `kube-dashboard.yaml`
- `kustomization.yaml`
- `metadata.yaml`
- `values.yaml`
