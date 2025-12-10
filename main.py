import argparse
import logging
import os

from config_loader import load_config
from health_checks import evaluate_service
from cost_model import estimate_monthly_cost
from report import print_summary, write_json


def setup_logging() -> None:
    """
    Configure application-wide logging.

    - Logs to console (via StreamHandler)
    - Logs to logs/monitor.log (via FileHandler)
    """
    os.makedirs("logs", exist_ok=True)

    logging.basicConfig(
        level = logging.INFO,
        format="%(asctime)s [%(levelname)s] %(name)s - %(message)s",
        handlers=[
            logging.FileHandler("logs/monitor.log", encoding="utf-8"),
            logging.StreamHandler()
        ]
    )

def main():
    """
    Entry point for the Cloud Environment Health & Cost Monitor.

    This script:
      - Loads a YAML config describing cloud services
      - Performs health checks (HTTP/Ping)
      - Calculates estimated cloud costs
      - Prints a formatted report
      - Saves results to a JSON file

    It simulates what DevOps/cloud engineers build internally for:
      - Monitoring scripts
      - Status dashboards
      - Cost reporting automation
      - CI/CD checks
    """

    setup_logging()
    logger = logging.getLogger(__name__)

    logger.info("Starting Cloud Environment Health & Cost Monitor")

    # Command-line interface
    parser = argparse.ArgumentParser(description="Cloud Environment Health & Cost Monitor")
    parser.add_argument("--config", required=True, help="Path to YAML config file")
    parser.add_argument("--out", default="report.json", help="Path to JSON report output")
    args = parser.parse_args()

    logger.info("Using config file: %s", args.config)
    logger.info("Output JSON will be written to: %s", args.out)

    # Load YAML config
    cfg = load_config(args.config)

    # Load YAML config
    cfg = load_config(args.config)

    # Environment label (prod/staging/etc.)
    env_name = cfg.get("environment", "unknown")
    logger.info("Environment: %s", env_name)

    results = []

    # Process each service in the config
    for svc in cfg["services"]:
        svc_name = svc.get("name", "unkown")
        logger.info("Evaluating service: %s", svc_name)

        # Perform HTTP/Ping health check
        health = evaluate_service(svc)

        # Calculate cloud cost
        monthly_cost = estimate_monthly_cost(svc)

        # Merge results into a single dict
        results.append({
            **health,
            "monthly_cost": monthly_cost
        })
    
    # Print human-readable report
    print_summary(env_name, results)

    # Save to JSON file for pipelines or dashboards
    write_json(args.out, results)
    logger.info("Wrote JSON report to %s", args.out)
    logger.info("Monitoring run complete")

# Run only if script is launched (not imported)
if __name__ == "__main__":
    main()
