# Nginx

- **Component path:** [`iac/kubernetes/nginx`](https://github.com/jamesread/AmberKube/tree/main/iac/kubernetes/nginx)
- **Description:** _NGINX ingress controller configuration and values._

- **Homepage:** [https://kubernetes.github.io/ingress-nginx/](https://kubernetes.github.io/ingress-nginx/)
- **Repository:** [https://github.com/kubernetes/ingress-nginx](https://github.com/kubernetes/ingress-nginx)
## Deployment Type
- HelmRelease (name: `ingress-nginx`, namespace: `default`, chart: `ingress-nginx@4.13.2`, source: `iac/kubernetes/nginx/nginx.yaml`)
## Files
- `kustomization.yaml`
- `metadata.yaml`
- `nginx.yaml`
- `values.yaml`
