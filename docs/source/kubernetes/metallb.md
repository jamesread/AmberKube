# Metallb

- **Component path:** [`iac/kubernetes/metallb`](https://github.com/jamesread/AmberKube/tree/main/iac/kubernetes/metallb)
- **Description:** _MetalLB load balancer configuration for bare-metal services._

- **Homepage:** [https://metallb.universe.tf/](https://metallb.universe.tf/)
- **Repository:** [https://github.com/metallb/metallb](https://github.com/metallb/metallb)
## Deployment Type
- HelmRelease (name: `metallb`, namespace: `default`, chart: `metallb@0.15.2`, source: `iac/kubernetes/metallb/app/metallb.yaml`)
## Files
- `app/ipaddresses.yaml`
- `app/kustomization.yaml`
- `app/l2advertisments.yaml`
- `app/metallb.yaml`
- `app/values.yaml`
- `ks.yaml`
- `metadata.yaml`
