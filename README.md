# Cloud Monitor – Python Cloud Environment Health & Cost Tool

Cloud Monitor is a lightweight Python CLI tool that evaluates the **health**, **availability**, and **estimated monthly cost** of cloud services based on a YAML configuration file.

It simulates real-world cloud engineering workflows by performing:

- HTTP health checks  
- Ping connectivity checks  
- Cost estimation  
- YAML-driven environment definitions  
- Logging to both console & file  
- Colorized CLI reporting  
- JSON output for downstream pipelines  

This project is ideal for DevOps, Cloud Engineering, and SRE learning paths.

---

## 🔥 Features

- HTTP health checks for APIs and microservices  
- Ping checks for internal hosts / worker nodes  
- Colorized status output (healthy, degraded, down, unknown)  
- Estimated monthly cost calculation  
- YAML configuration support  
- JSON output for pipelines  
- Structured logging (`logs/monitor.log`)  
- Extensible modular architecture  

---

## 📂 Project Structure

```text
cloud-monitor/
│
├── main.py
├── config_loader.py
├── health_checks.py
├── cost_model.py
├── report.py
├── config.example.yaml
├── requirements.txt
└── README.md
```

---

## ⚙️ Installation

### 1. Clone the repository

```bash
git clone https://github.com/HonestlyBad/cloud-monitor.git
cd cloud-monitor
```

### 2. Create & activate a virtual environment

```bash
python -m venv venv
```

**Windows:**

```bash
venv\Scripts\activate
```

**Mac/Linux:**

```bash
source venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

---

## 🚀 Running the Tool

Use the included example config:

```bash
python main.py --config config.example.yaml
```

You will get:

- A colorized health report in the terminal  
- A JSON file (`report.json`)  
- A detailed log file (`logs/monitor.log`)  

---

## 📝 Example Output

```text
=== Cloud Environment Health Report: staging ===

Legend:
  ✅ healthy
  ⚠️ degraded
  ❌ down
  ❓ unknown

- auth-api        | status=✅ healthy   | monthly_cost=$72.00
- user-service    | status=❌ down      | monthly_cost=$43.20
- internal-worker | status=✅ healthy   | monthly_cost=$28.80

Total estimated monthly cost: $144.00
```

---

## 🧾 YAML Configuration Format

Here is the example configuration file:

```yaml
environment: "staging"
owner: "Albert"
currency: "USD"

services:
  - name: "auth-api"
    type: "http"
    url: "https://httpbin.org/status/200"
    cpu_cores: 2
    ram_gb: 4
    hourly_rate: 0.05

  - name: "user-service"
    type: "http"
    url: "https://httpbin.org/status/503"
    cpu_cores: 1
    ram_gb: 2
    hourly_rate: 0.03

  - name: "internal-worker"
    type: "ping"
    host: "8.8.8.8"
    cpu_cores: 1
    ram_gb: 1
    hourly_rate: 0.02
```

### Required keys

| Key | Description |
|-----|-------------|
| `environment` | Label for the environment (staging, prod, etc.) |
| `services` | List of service definitions |
| `name` | Name of the service |
| `type` | `http` or `ping` |
| `url` or `host` | Health check endpoint |
| `cpu_cores`, `ram_gb` | Used for cost estimation |
| `hourly_rate` | Optional explicit cost override |

---

## 📊 JSON Output Example

```json
[
  {
    "name": "auth-api",
    "type": "http",
    "status": "healthy",
    "monthly_cost": 72.0
  },
  {
    "name": "user-service",
    "type": "http",
    "status": "down",
    "monthly_cost": 43.2
  }
]
```

---

## 📒 Logging

Execution logs are saved to:

```text
logs/monitor.log
```

Example log entries:

```text
2025-01-01 12:00:00,123 [INFO] main - Evaluating service: auth-api
2025-01-01 12:00:00,456 [INFO] cost_model - Estimated monthly cost for service 'auth-api' is 72.00
2025-01-01 12:00:00,789 [WARNING] health_checks - Ping to 10.0.0.5 failed
```

---

## 🧱 Architecture Overview

### main.py
- Orchestrates the entire workflow  
- Loads config, runs checks, prints summary, writes JSON  

### config_loader.py
- Loads YAML  
- Validates structure  

### health_checks.py
- HTTP health checks  
- Ping health checks  

### cost_model.py
- Simple cost computation  
- Supports explicit or derived cost  

### report.py
- Colorized console output  
- Summary report  
- JSON output writer  

---

## 🛠 Extending the Project

### Add support for real cloud providers

- AWS (`boto3`)  
- IBM Cloud (`ibm-cloud-sdk-core`)  
- Azure (`azure-mgmt-*`)  
- GCP (`google-cloud-*`)  

### Add async health checks with asyncio

Speed up health checks when monitoring many services by running them concurrently.

### Convert into a pip-installable CLI

Allow users to run:

```bash
cloudmon --config prod.yaml
```

### Dockerize

Run this tool inside CI/CD jobs or as a cron-based monitoring container.

---

## 📄 License

MIT License 

---

## 👤 Author

**Albert Tulo IV**  
Software Developer / Cloud Engineer 
GitHub: (https://github.com/HonestlyBad)
