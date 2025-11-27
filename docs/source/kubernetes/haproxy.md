# Haproxy

- **Component path:** [`iac/kubernetes/haproxy`](https://github.com/xconspirisist/kubernetes-homelab/tree/main/iac/kubernetes/haproxy)
- **Description:** _HAProxy ingress layer plus metrics/stats endpoints._

- **Homepage:** [https://www.haproxy.org/](https://www.haproxy.org/)
- **Repository:** [https://github.com/haproxy/haproxy](https://github.com/haproxy/haproxy)
## Deployment Type
- HelmRelease (name: `haproxy`, namespace: `default`, chart: `haproxy-ingress`, source: `iac/kubernetes/haproxy/haproxy.yaml`)
## Files
- `haproxy.yaml`
- `ingress-metrics.yaml`
- `ingress-stats.yaml`
- `kustomization.yaml`
- `metadata.yaml`
- `values.yaml`
