DOCKER_IMAGE = local/NAME

all: fmt

.PHONY: fmt
fmt:
	uv run ruff format
	uv run ruff check --fix

.PHONY: check
check: test mypy


.PHONY: test
test:
	uv run pytest

.PHONY: mypy
mypy:
	uv run mypy

.PHONY: docker
docker:
	docker build -t $(DOCKER_IMAGE) .
