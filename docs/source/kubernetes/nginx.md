# Nginx

- **Component path:** [`iac/kubernetes/nginx`](https://github.com/jamesread/AmberKube/tree/main/iac/kubernetes/nginx)
- **Description:** _NGINX ingress controller configuration and values._

- **Homepage:** [https://kubernetes.github.io/ingress-nginx/](https://kubernetes.github.io/ingress-nginx/)
- **Repository:** [https://github.com/kubernetes/ingress-nginx](https://github.com/kubernetes/ingress-nginx)
## Deployment Type
- HelmRelease (name: `ingress-nginx`, namespace: `default`, chart: `ingress-nginx@4.13.2`, source: `iac/kubernetes/nginx/app/nginx.yaml`)
## Files
- `app/kustomization.yaml`
- `app/nginx.yaml`
- `app/values.yaml`
- `ks.yaml`
- `metadata.yaml`
