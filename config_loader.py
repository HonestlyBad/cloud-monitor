import yaml
import logging
from pathlib import Path

logger = logging.getLogger(__name__)

def load_config(path: str) -> dict:
    """
    Loads and parses a YAML configuration file.

    Cloud engineers frequently work with YAML (Terraform, Kubernetes,
    Docker Compose, CI/CD pipelines, etc.). This function allows your
    tool to read environment definitions, list of services, credentials,
    resource allocations, and more.

    Args:
        path (str): Path to the YAML config file.

    Returns:
        dict: Parsed YAML as a Python dictionary.
    """

    # Convert string path → Path object for safer filesystem operations
    cfg_path = Path(path)
    logger.info("Loading config from %s", cfg_path)

    # Verify config exists
    if not cfg_path.exists():
        logger.error("Config file not found: %s", cfg_path)
        raise FileNotFoundError(f"Config file not found: {path}")

    # Open and parse YAML safely
    with cfg_path.open() as f:
        data = yaml.safe_load(f)

    # Basic validation: ensure required keys exist
    if "services" not in data:
        logger.error("Config missing 'services' key.")
        raise ValueError("Config missing 'services' key.")

    logger.info("Config loaded successfully with %d services", len(data["services"]))
    return data
