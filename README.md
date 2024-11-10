# ITU_project
Tanky

This project uses Docker Compose, which is included with Docker Desktop (download from [docker.com](https://www.docker.com/products/docker-desktop/))

## Project Structure

- backend: Contains the FastAPI backend code.
- frontend: Contains the Vue.js frontend code.
- docker-compose.yml: Docker Compose configuration to manage all services.

## Using Docker Compose
> **Note**: If the command `docker-compose` does not work, try using `docker compose` (without the hyphen) instead.

| Command                                | Description                                           |
|----------------------------------------|-------------------------------------------------------|
| `docker-compose build`                 | Builds all services in the `docker-compose.yml`.      |
| `docker-compose build <service_name>`  | Builds a single service (e.g., `web-app`, `backend`). |
| `docker-compose up --build`            | Rebuilds and restarts containers.                     |
| `docker-compose up`                    | Starts all services in the foreground.                |
| `docker-compose up -d`                 | Starts all services in detached mode (background).    |
| `docker-compose down`                  | Stops and removes all containers.                     |
| `docker-compose down -v`               | Stops containers and removes volumes (data cleanup).  |
| `docker-compose logs <service_name>`   | Shows logs for a specific service.                    |
| `docker-compose exec <service_name> sh`| Opens a shell in a specific running container.        |
| `docker ps`                            | Lists all currently running Docker containers.        |

### Commands inside the docker
Watch for changes in Tailwind CSS:
```bash
docker exec -it frontend npx tailwindcss -i ./src/assets/tailwind.css -o ./src/assets/output.css --watch
```




## Running the Project

Services will be available at:
- [http://localhost:8080](http://localhost:8080) - Web App frontend
- [http://localhost:8000](http://localhost:8000) - FastAPI backend
- [http://localhost:6379](http://localhost:6379) - Redis database

API Documentation:
- [http://localhost:8000/docs](http://localhost:8000/docs) - FastAPI Swagger UI
- [http://localhost:8000/redoc](http://localhost:8000/redoc) - FastAPI Redoc UI

# If problems with permission in node-modules
- Run containers as docker compuse -up
- Navigate to web-app container
```bash
docker exec -it frontend bash
```
- apply permissions
```bash
chmod -R 777 ./node_modules
```
