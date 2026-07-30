pre-commit:
	echo "Running pre-commit hooks"
	pre-commit run --all-files

actionlint:
	echo "Running actionlint against .github/workflows"
	actionlint -color

kustomize-build:
	echo "Building all Kubernetes app kustomizations"
	@set -e; for d in iac/kubernetes/*/app; do \
		echo "  kustomize build $$d"; \
		kustomize build "$$d" >/dev/null; \
	done

ansible-lint:
	echo "Running ansible-lint against iac/ansible"
	@if [ ! -f iac/ansible/.vault_pass ]; then \
		printf 'ci-dummy-not-for-decryption\n' > iac/ansible/.vault_pass; \
		echo "Created temporary iac/ansible/.vault_pass for syntax-check"; \
	fi
	cd iac/ansible && ansible-lint

kube-lint:
	echo "Running kube-linter against iac/kubernetes/"
	kube-linter lint iac/kubernetes

ci: actionlint pre-commit kustomize-build ansible-lint

docs:
	make -C docs

docgen:
	./scripts/generate_kubernetes_docs.py
	./scripts/generate_ansible_docs.py

.PHONY: pre-commit actionlint kustomize-build ansible-lint kube-lint ci docs docgen
