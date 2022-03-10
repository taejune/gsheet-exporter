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
		-e GOOGLE_APPLICATION_CREDENTIALS=/secret/credential.json \
		-e SHEET_ID= \
		-e RANGE= \
		-e REGISTRY_URL= \
		-e DOCKER_CRED= \
		-e QUAY_CRED= \
		-e ARCHIVE_PATH=/data \
		-e SCP_DEST= \
		-e SCP_PASS \
		-v /tmp/data:/data \
		$(REPO)/$(IMAGE):$(TAG)