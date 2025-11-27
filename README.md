<div align = "center">
  <img src="docs/source/assets/amberkube.svg" alt="AmberKube Logo" width="128">
  <h1>AmberKube</h1>
</div>

A robust little Kubernetes distribution, designed for zero upstream changes, low hardware requirements, and maintained with AI.

> **WARNING**: This project was started to understand **just how hard it is to truely maintain** your own Kubernetes-based platform. It is an ongoing experiment from [James Read](https://jread.com), where he uses it for his various kubernetes clusters in a self hosted setup. [Read more about James' self hosting here](https://blog.jread.com/posts/my-selfhosted-private-enterprise/).

You should probably not really use this, and use OpenShift instead :-)

* **Documentation**: https://jamesread.github.io/AmberKube

## High level main technical components

* Fedora
* Ansible
* Flux
* metallb
* nfs-externaldir
* kyverno
* kubemetrics
* kube-state-metrics

All components are documented in the **docs**: https://jamesread.github.io/AmberKube

## Design goal: zero upstream changes

* Relies on upstream projects, direct from upstream source.

## Design goal: low hardware requirementsd

* Target is a single x86 VM, 4Gb/RAM, but can be scaled.
* Emphasis on using as few projects as is practical, with low resource usage.
* Targets full Fedora (not container distros like CoreOS or Talos), because it's easy to setup, manage snd debug. It's also readily available on many cloud providers.
* Helm, because of zero overhead post-install, even though it sucks for Day2.

## Anti design goals

* Designed for homelabs, not cloud providers, so won't use any specialist CSI or CNI drivers.
* Prioritize low overhead and simplicity over scale (eg, Flannel over Calico, eg Flux over Argo).
* Won't support variations - eg not Ubuntu, or Talos, or CoreOS.

## This is a No-Nonsense Open Source project

- All code in this project is Open Source (AGPL), and dependencies must use OSI approved Open Source licenses.
- No company is paying for development, there is no paid-for support from the developers.
- No separate core and premium version, no plus/pro version or paid-for extra features.
- No SaaS service or "special cloud version".
- No "anonymous data collection", usage tracking, user tracking, telemetry or email address collection.
- No requests for reviews in any "app store" or feedback surveys.
- No prompts to "upgrade to the latest version".
- No internet-connection required for any functionality.
