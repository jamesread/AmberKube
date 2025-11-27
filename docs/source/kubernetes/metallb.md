# Metallb

- **Component path:** [`iac/kubernetes/metallb`](https://github.com/jamesread/AmberKube/tree/main/iac/kubernetes/metallb)
- **Description:** _MetalLB load balancer configuration for bare-metal services._

- **Homepage:** [https://metallb.universe.tf/](https://metallb.universe.tf/)
- **Repository:** [https://github.com/metallb/metallb](https://github.com/metallb/metallb)
## Deployment Type
- HelmRelease (name: `metallb`, namespace: `default`, chart: `metallb@0.15.2`, source: `iac/kubernetes/metallb/metallb.yaml`)
## Files
- `ipaddresses.yaml`
- `kustomization.yaml`
- `l2advertisments.yaml`
- `metadata.yaml`
- `metallb.yaml`
- `values.yaml`
