all: echo # to not run any script unintentionally

# Test (to not run any script unintentionally)

echo:
	@echo "Makefile"

# make container

container:
	./docker_trivy.sh