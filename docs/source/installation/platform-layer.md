# Platform layer (Flux)

**Step 3** installs **platform layer** workloads using **[Flux](https://fluxcd.io/)** (GitOps). In AmberKube, that means the platform pieces under **`iac/kubernetes/`**—for example **cert-manager**, **MetalLB**, **NGINX Ingress**, **Kyverno**, monitoring hooks, and the **`flux-system`** overlays—expressed as **`HelmRepository`**, **`HelmRelease`**, **`Kustomization`**, and related manifests. Flux’s controllers reconcile those definitions from a **Git** source so the cluster stays aligned with **[github.com/jamesread/AmberKube](https://github.com/jamesread/AmberKube)** (unless you point Flux at another remote).

You need a **working cluster** and **`kubectl`** configured (after [Step 2.2 — Kubeadm init (Flannel)](kubeadm-init-flannel.md)). Workers from [Step 3.1 — Create kubeworker VMs](kubeworkers.md) are optional for this step if your infra components can run on the control plane; many homelab setups still join workers first.

## Install the Flux CLI

On a machine that has **`kubectl`** access to the cluster (often your laptop or the kubemaster), install the **`flux`** command-line tool. Follow the current instructions: [Flux installation](https://fluxcd.io/flux/installation/).

## Bootstrap Flux on the cluster

**Bootstrap** installs the Flux controllers into the **`flux-system`** namespace and creates a **`GitRepository`** that points at the Git repository you configure, plus an initial **`Kustomization`** that syncs a path you choose. Use **`flux bootstrap github`** when the remote is on **GitHub**—it uses the GitHub API, manages deploy keys, and pushes bootstrap commits reliably. (Use **`flux bootstrap git`** only for non-GitHub remotes such as GitLab or self-hosted Git.)

The examples below default to **[github.com/jamesread/AmberKube](https://github.com/jamesread/AmberKube)**. Set **`GITHUB_OWNER`** and **`GITHUB_REPO`** to **your fork** if you are not a maintainer, because bootstrap **writes commits** to that repository.

You need a **[GitHub personal access token](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/managing-your-personal-access-tokens)** (**PAT**) with permission to push and administer the target repo (classic: **`repo`** scope; or fine-grained: repository access with **Contents: Read and write** and **Metadata** read). Export it as **`GITHUB_TOKEN`** (Flux reads this variable). Do not commit the token; use **`export`** for the session or a local env file that stays out of Git.

Set the values once as **environment variables**, then run **`flux bootstrap github`**:

```bash title="Workstation (kubectl + flux)"
export GITHUB_TOKEN="ghp_REPLACE_ME"
export GITHUB_OWNER="jamesread"
export GITHUB_REPO="AmberKube"
export GIT_BRANCH="main"
export FLUX_SYNC_PATH="iac/kubernetes"

flux bootstrap github \
  --owner="${GITHUB_OWNER}" \
  --repository="${GITHUB_REPO}" \
  --branch="${GIT_BRANCH}" \
  --path="${FLUX_SYNC_PATH}" \
  --personal \
  --reconcile
```

- **`GITHUB_TOKEN`** — PAT used by the Flux CLI against the GitHub API (and for git operations during bootstrap).
- **`GITHUB_OWNER`** — GitHub **user** or **organization** that owns the repository (your GitHub username for a fork, or **`jamesread`** for upstream if you have access).
- **`GITHUB_REPO`** — Repository name only (e.g. **`AmberKube`**), not the full URL.
- **`GIT_BRANCH`** — Branch Flux should track (often **`main`**).
- **`FLUX_SYNC_PATH`** — Directory **inside the repo** for the cluster **`Kustomization`** (here **`iac/kubernetes`**).
- **`--personal`** — Owner is a **user** account, not an organization. Omit **`--personal`** when **`GITHUB_OWNER`** is an **org** (see [Flux bootstrap for GitHub](https://fluxcd.io/flux/installation/bootstrap/github/) for org and team options).
- **`--reconcile`** — Reconcile bootstrap state when the repository **already exists** (typical for AmberKube). Omit on a brand-new empty repo if you prefer the default Flux behavior.

For a **public** repository on a **personal** account when Flux **creates** the repo, you may need **`--private=false`** (Flux defaults new repos to private). For **GitHub Enterprise Server**, set **`--hostname`**.

See the official guide: [Flux bootstrap for GitHub](https://fluxcd.io/flux/installation/bootstrap/github/). For GitLab, Gitea, or generic Git servers, see [Flux bootstrap for Git repositories](https://fluxcd.io/flux/installation/bootstrap/).

If you already have Flux installed elsewhere, you can instead apply **`GitRepository`** and **`Kustomization`** resources by hand; bootstrap is the usual first-time path.

## What the platform layer means here

AmberKube keeps each component under **`iac/kubernetes/<component>/`** with:

- **`metadata.yaml`** — human-oriented description (not applied to the cluster).
- **`ks.yaml`** — Flux **`Kustomization`** (`kustomize.toolkit.fluxcd.io/v1`) that points at **`./iac/kubernetes/<component>/app`** and **`GitRepository`** **`flux-system`**.
- **`app/`** — Kubernetes manifests and **`kustomization.yaml`** (kustomize.config.k8s.io) consumed by that Flux **`Kustomization`**.

The root **`iac/kubernetes/kustomization.yaml`** lists only **`*/ks.yaml`** so the bootstrap sync applies the Flux **`Kustomization`** CRs together; each workload reconciles **independently**, so one broken **`app/`** does not block the whole tree.

The **`flux-system`** workload’s Flux **`Kustomization`** is named **`flux-system-apps`** (not **`flux-system`**) to avoid clashing with the bootstrap root **`Kustomization`** also named **`flux-system`**. The component catalog in the docs is under **Kubernetes** in the navigation (for example [Flux System](../kubernetes/flux-system.md)).

## Verify

After bootstrap and any extra **`Kustomization`** resources are applied:

```bash title="Workstation (kubectl)"
flux get kustomizations -A
flux get sources git -n flux-system
kubectl get pods -n flux-system
```

Check that **`HelmRelease`** and **`HelmRepository`** objects in your synced paths reach **Ready** status.

## What happens next

- Tune **`values.yaml`** and overlays per component, or add environment-specific paths (your own **`environments/`** layout) if you use that pattern.
- Application workloads (Layer 2) can be added as additional Flux **`Kustomization`** resources or other GitOps paths.
