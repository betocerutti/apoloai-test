.PHONY: orders_shell products_shell test_products test_orders

# Check if -v flag is passed to make run
ifeq ($(findstring -v,$(MAKEFLAGS)),-v)
    DOCKER_COMPOSE_ARGS :=
else
    DOCKER_COMPOSE_ARGS := -d
endif

run:
	@echo "Starting services"
	docker-compose up $(DOCKER_COMPOSE_ARGS)

stop:
	@echo "Stopping services"
	docker-compose down


orders_shell:
	@echo "Starting shell in orders container"
	docker exec -it orders_service_container /bin/sh

test_orders:
	@echo "Running tests in orders container"
	docker exec -it orders_service_container bash -c "pytest -v"

products_shell:
	@echo "Starting shell in products container"
	docker exec -it products_service_container /bin/sh

test_products:
	@echo "Running tests in products container"
	docker exec -it product_service_container bash -c "./manage.py test"

# Help target
.PHONY: help
help:
	@echo "Usage:"
	@echo "  make run [-v]"
	@echo "  make <target>"
	@echo ""
	@echo "Targets:"
	@echo "  run            - Start all services (use -v to run in attached mode)"
	@echo "  orders_shell   - Open shell in orders container"
	@echo "  products_shell - Open shell in products container"
	@echo "  test_orders    - Run tests in orders container"
	@echo "  test_products  - Run tests in products container"

