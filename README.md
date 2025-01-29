# How to Run Virtual Microservices Store

## Requirements

You will need Docker installed on your computer.

1. Clone the project from [https://github.com/betocerutti/apoloai-test.git](link to github).
2. Change the directory to `apoloai-test`.

## Available Make Commands

You can always run `make help` to inspect the available commands.

Here is an example output:

```
Usage:
  make run [-v]
  make <target>

Targets:
  run            - Start all services (use -v to run in attached mode)
  orders_shell   - Open shell in orders container
  products_shell - Open shell in products container
  test_orders    - Run tests in orders container
  test_products  - Run tests in products container
```

## Running the Services

After running `make run`, the services will be available at the following endpoints:

### Product Service

The Product service is a DjangoRestFramework application backed by a SQLite database.

- **Swagger UI**: [http://localhost:8000/swagger](http://localhost:8000/swagger)

Notes: There are initial scripts that load sample data into the product service using Django fixtures. You do not need to worry about this, it is included in the initial command when the containers are created.

### Orders Service

The orders service is a FastAPI application backed by a SQLLite database. 

- **Swagger UI**: [http://localhost:8001/docs](http://localhost:8001/docs)

You can create orders interactively through the Swagger documentation.

## Notes

The entire lifecycle can be tested interactively through the Swagger documentation for each service.



