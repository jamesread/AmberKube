# Haproxy

- **Component path:** [`iac/kubernetes/haproxy`](https://github.com/jamesread/AmberKube/tree/main/iac/kubernetes/haproxy)
- **Description:** _HAProxy ingress layer plus metrics/stats endpoints._

- **Homepage:** [https://www.haproxy.org/](https://www.haproxy.org/)
- **Repository:** [https://github.com/haproxy/haproxy](https://github.com/haproxy/haproxy)
## Deployment Type
- HelmRelease (name: `haproxy`, namespace: `default`, chart: `haproxy-ingress`, source: `iac/kubernetes/haproxy/app/haproxy.yaml`)
## Files
- `app/haproxy.yaml`
- `app/ingress-metrics.yaml`
- `app/ingress-stats.yaml`
- `app/kustomization.yaml`
- `app/values.yaml`
- `ks.yaml`
- `metadata.yaml`
