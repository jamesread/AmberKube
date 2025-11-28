# AmberKube

<div align="center">
  <img src="assets/amberkube.svg" alt="AmberKube Logo" width="200">
</div>

The first layer of stuff needed to make Kubernetes useable in a self-hosted environment.

---

> **WARNING**: This project was started to understand **just how hard it is to truely maintain** your own Kubernetes-based platform. The answer so far is that __building is easy, maintaining it is hard__. It is an ongoing experiment from [James Read](https://jread.com). It is used for his various kubernetes clusters in a self hosted setup and ongoing learning. [Read more about James' self hosting here](https://blog.jread.com/posts/my-selfhosted-private-enterprise/).


<img src="assets/architecture.png" alt="Architecture Diagram">

## Layers

* **Layer 0**: Infrastructure - Ansible
* **Layer 1:** Platform - Kubernetes
* **Layer 2:** -- workloads --
