.PHONY: help build run stop clean test push

help:
	@echo "BCP-CyberSuite Docker Commands:"
	@echo "  make build    - Build Docker image"
	@echo "  make run      - Run container interactively"
	@echo "  make daemon   - Run as daemon"
	@echo "  make stop     - Stop container"
	@echo "  make clean    - Remove containers and images"
	@echo "  make test     - Run tests in container"
	@echo "  make push     - Push to Docker Hub"
	@echo "  make shell    - Access container shell"

build:
	docker build -t bcp-cybersuite:latest .

run:
	docker run -it --rm \
		--name bcp-cybersuite \
		-v "$(PWD)/reports:/app/reports" \
		-v "$(PWD)/databases:/app/databases" \
		bcp-cybersuite:latest

daemon:
	docker run -d --restart unless-stopped \
		--name bcp-cybersuite \
		-v "$(PWD)/reports:/app/reports" \
		-v "$(PWD)/databases:/app/databases" \
		bcp-cybersuite:latest

stop:
	docker stop bcp-cybersuite || true
	docker rm bcp-cybersuite || true

clean:
	docker system prune -f
	docker images prune -f

test:
	docker run --rm bcp-cybersuite:latest \
		python -m pytest tests/ -v

shell:
	docker exec -it bcp-cybersuite /bin/bash

push:
	docker tag bcp-cybersuite:latest cybernahid/bcp-cybersuite:latest
	docker push cybernahid/bcp-cybersuite:latest
