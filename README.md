# Kafucka Distributed Cluster

A distributed Python backend featuring an Auth API and an Ingestion API that acts as a high-throughput **Kafka producer**. This project uses a Master/Worker architecture over a **Tailscale** VPN, allowing multiple developers to run API nodes locally that all share a central PostgreSQL database and Kafka broker.

## Architecture

- **Master Node (Host):** Runs the PostgreSQL database, the Kafka broker, and local instances of the APIs.
- **Worker Nodes (sharing server workload):** Run _only_ the APIs. They connect to the Master node's database and Kafka broker securely over Tailscale.

## Prerequisites (Everyone)

1. **Docker** and the **Docker Compose** plugin installed.
2. **Tailscale** installed and logged in.

---

## Master Node Setup (For the Host)

As the host, your machine runs the core infrastructure.

### 1. Configure Environment

Create a `.env` file at the root of the project. **Do not commit this file.**

```env
# Your machine's Tailscale IPv4 address (100.x.x.x)
TAILSCALE_IP=100.x.x.x

# Database Credentials
DATABASE_URL=postgresql+asyncpg://<POSTGRES_USER>:<POSTGRES_PWD>@localhost:5432/<POSTGRES_DBNAME>

# Security
SECRET=your_super_secret_key
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

### 2. Start the Cluster

Boot the database, Kafka broker, and your local API nodes using the default compose file:

```bash
docker compose up -d --build
```

- Auth API is available at: `http://localhost:8000`
- Ingestion API is available at: `http://localhost:8001`

---

## Worker Node Setup (For sharing server workload)

As a worker, your machine only runs the lightweight API containers and routes data to the Master node.

### 1. Join the VPN

Ensure Tailscale is running and you have joined the Host's Tailscale network. You should be able to ping the Host's `100.x.x.x` IP address. Ask the Host for this IP.

### 2. Configure Environment

Create a `.env` file at the root of the project. **Do not commit this file.** You will need the same database credentials and secrets as the Master, but your URLs must point to the Master's Tailscale IP.

```env
# The HOST machine's Tailscale IPv4 address
MASTER_TAILSCALE_IP=100.x.x.x

# Database Credentials (pointing to the Master's IP)
DATABASE_URL=postgresql+asyncpg://<POSTGRES_USER>:<POSTGRES_PWD>@100.x.x.x:5432/<POSTGRES_DBNAME>

# Kafka Configuration (pointing to the Master's IP)
KAFKA_SERVER_URL=100.x.x.x:9092

# Security (Must exactly match the Master's keys)
SECRET=your_super_secret_key
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

> **Note:** If your `docker-compose.worker.yml` uses hardcoded placeholders like `<MY_TAILSCALE_IP>` instead of `.env` variables, simply replace those placeholders directly in the `.yml` file before running the next step.

### 3. Start the APIs

Boot up the worker containers using the dedicated worker compose file:

```bash
docker compose -f docker-compose.worker.yml up -d
```

Your local APIs are now running and will instantly start communicating securely with the Master's database and message broker!
