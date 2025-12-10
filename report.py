import json
from typing import List, Dict, Any

def print_summary(env_name: str, results: List[Dict[str, Any]]) -> None:
    """
    Prints a human-readable summary of all service statuses and costs.

    This simulates what cloud dashboards like AWS Cost Explorer /
    GCP Cloud Monitoring / IBM Cloud Monitoring show.

    Args:
        env_name (str): Environment label (staging, prod, etc.)
        results (list): List of service health + cost dictionaries.
    """

    print(f"\n=== Cloud Environment Health Report: {env_name} ===\n")

    for r in results:
        print(f"- {r['name']:15} | status={r['status']:8} | monthly_cost=${r['monthly_cost']:,.2f}")

    print()

    # Total monthly cost of all services
    total = sum(r["monthly_cost"] for r in results)
    print(f"Total estimated monthly cost: ${total:,.2f}\n")


def write_json(path: str, results: List[Dict[str, Any]]) -> None:
    """
    Outputs the service results to a JSON file.

    Useful for:
      - CI pipelines
      - dashboards
      - other tools to consume
      - saving historical records

    Args:
        path (str): Output file path.
        results (list): Result data.
    """

    with open(path, "w") as f:
        json.dump(results, f, indent=2)
