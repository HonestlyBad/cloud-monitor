import subprocess
import requests
from typing import Literal, Dict, Any

# Allowed health statuses for clarity
HealthStatus = Literal["healthy", "degraded", "down", "unknown"]

def http_health_check(url: str, timeout: float = 3.0) -> HealthStatus:
    """
    Performs a simple HTTP GET request to determine if a service is available.

    Used for checking:
      - API endpoints
      - microservices
      - load balancers
      - health/ready endpoints

    Args:
        url (str): HTTP endpoint to check.
        timeout (float): Max wait time before treating as failed.

    Returns:
        HealthStatus: healthy / degraded / down
    """
    try:
        res = requests.get(url, timeout=timeout)

        # 2xx = healthy
        if 200 <= res.status_code < 300:
            return "healthy"

        # 3xx–4xx = degraded (usually misconfig or client error)
        elif 300 <= res.status_code < 500:
            return "degraded"

        # 5xx = server down / overloaded
        else:
            return "down"

    except requests.RequestException:
        # Network issue / timeout / DNS failure
        return "down"


def ping_health_check(host: str, timeout: int = 2000) -> HealthStatus:
    """
    Pings an IP or hostname once to test basic network availability.

    Used for checking:
      - internal worker nodes
      - servers without HTTP endpoints
      - VPN or internal network reachability

    Args:
        host (str): Hostname or IP to ping.

    Returns:
        HealthStatus: healthy / down
    """

    # Windows uses "ping -n 1", Linux/Mac would use "-c 1"
    cmd = ["ping", "-n", "1", host]

    # Run command silently
    result = subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    # 0 = success
    return "healthy" if result.returncode == 0 else "down"


def evaluate_service(service: Dict[str, Any]) -> Dict[str, Any]:
    """
    Determines which health check method to use based on service type.

    Example:
      type: "http" → check URL
      type: "ping" → check host reachability

    Returns:
        dict: service name, type, and status
    """

    stype = service.get("type")
    status: HealthStatus = "unknown"

    # Call the right health check based on type
    if stype == "http":
        status = http_health_check(service["url"])

    elif stype == "ping":
        status = ping_health_check(service["host"])

    else:
        status = "unknown"

    # Return standardized health response
    return {
        "name": service.get("name", "unknown"),
        "type": stype,
        "status": status
    }
