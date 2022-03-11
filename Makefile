DOCKERCMD=$(shell which docker)
DOCKERBUILD=$(DOCKERCMD) build
DOCKERPUSH=$(DOCKERCMD) push

REPO=tmaxcloudck
IMAGE=gsheet-exporter
TAG=dev

build:
	@echo "building..."
	@$(DOCKERBUILD) . -t $(REPO)/$(IMAGE):$(TAG)

push:
	@echo "push $(REPO)/$(IMAGE):$(TAG)..."
	@$(DOCKERPUSH) $(REPO)/$(IMAGE):$(TAG)

run:
	@docker run --name gsheet -it --rm -p 8080:8080 \
		-e GOOGLE_APPLICATION_CREDENTIALS=/secret/playground-321801-3f90d7a582f0.json \
		-e TARGET_SHEETS='1zBHhKvdz5sv2HZFWGcbsvAVFspQAvm_yEYtY9ZffSZc;CK1!C2:D,1zBHhKvdz5sv2HZFWGcbsvAVFspQAvm_yEYtY9ZffSZc;CK2!C2:D' \
		-e REGISTRY_URL= \
		-e DOCKER_CRED= \
		-e QUAY_CRED= \
		-e ARCHIVE_PATH=/data \
		-e SCP_DEST= \
		-e SCP_PASS \
		-v /tmp/data:/data \
		$(REPO)/$(IMAGE):$(TAG)