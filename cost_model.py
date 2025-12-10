from typing import Dict, Any

def estimate_monthly_cost(service: Dict[str, Any], hours_per_month: int = 24 * 30) -> float:
    """
    Computes a simple estimated monthly cloud cost for a service.

    Cloud pricing is typically:
      - Per hour (EC2, VMs, containers)
      - Based on CPU cores & RAM size

    This simplified model:
      - Uses hourly_rate if provided in the config
      - Otherwise derives an estimated cost using cpu_cores + ram_gb

    Args:
        service (dict): The service configuration.
        hours_per_month (int): Typically 720 hours/month.

    Returns:
        float: Monetary cost estimate.
    """

    rate = service.get("hourly_rate")

    # If no explicit hourly rate, compute a simple cost formula
    if rate is None:
        cpu = service.get("cpu_cores", 1)
        ram = service.get("ram_gb", 1)

        # Simple cloud-like pricing model ($ per hour)
        rate = cpu * 0.02 + ram * 0.005

    # Multiply by hours per month to get estimated monthly price
    return round(rate * hours_per_month, 2)
