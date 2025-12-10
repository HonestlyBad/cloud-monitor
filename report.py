import json
from typing import List, Dict, Any

from colorama import init, Fore, Style

# Initialize colorama (needed especially on Windows to enable ANSI colors)
init(autoreset=True)

def format_status(status: str) -> str:
    """
    Returns a colorized status string with an icon.

    healthy -> green Check
    degraded -> yellow Warning Triangle
    down -> red X
    unkown -> dimmed ?
    """

    status_lower = status.lower() if status else "unkown"

    if status_lower == "healthy":
        color = Fore.GREEN
        icon = "✅"
    elif status_lower == "degraded":
        color = Fore.YELLOW
        icon = "⚠️"
    elif status_lower == "down":
        color = Fore.RED
        icon = "❌"
    else:
        color = Fore.WHITE + Style.DIM
        icon = "❓"
    
    # Pad the raw text to a fixed width for nicer columns
    raw = f"{status_lower:<8}" # e.g "healthy "
    # Wrap with color + icon
    return f"{color}{icon} {raw}{Style.RESET_ALL}"


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

    # Legend for quick reference
    print("Legend:")
    print(f"  {Fore.GREEN}✅ healthy{Style.RESET_ALL}")
    print(f"  {Fore.YELLOW}⚠️ degraded{Style.RESET_ALL}")
    print(f"  {Fore.RED}❌ down{Style.RESET_ALL}")
    print(f"  {Style.DIM}❓ unknown{Style.RESET_ALL}\n")

    for r in results:
        status_display = format_status(r["status"])
        print(f"- {r['name']:15} | status={status_display} | monthly_cost=${r['monthly_cost']:,.2f}")

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
