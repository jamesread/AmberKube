# Kube Dashboard

- **Component path:** [`iac/kubernetes/kube-dashboard`](https://github.com/jamesread/AmberKube/tree/main/iac/kubernetes/kube-dashboard)
- **Description:** _Kubernetes Dashboard web UI and supporting manifests._

- **Homepage:** [https://kubernetes.io/docs/tasks/access-application-cluster/web-ui-dashboard/](https://kubernetes.io/docs/tasks/access-application-cluster/web-ui-dashboard/)
- **Repository:** [https://github.com/kubernetes/dashboard](https://github.com/kubernetes/dashboard)
## Deployment Type
- HelmRelease (name: `kube-dashboard`, namespace: `default`, chart: `kubernetes-dashboard`, source: `iac/kubernetes/kube-dashboard/app/kube-dashboard.yaml`)
## Files
- `app/kube-dashboard.yaml`
- `app/kustomization.yaml`
- `app/values.yaml`
- `ks.yaml`
- `metadata.yaml`
