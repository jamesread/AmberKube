pre-commit:
	echo "Running pre-commit hooks"
	pre-commit run --all-files

kube-lint:
	echo "Running kube-linter against iac/kubernetes/"
	kube-linter lint iac/kubernetes

docs:
	make -C docs

docgen:
	./scripts/generate_kubernetes_docs.py
	./scripts/generate_ansible_docs.py

.PHONY: docs docgen
