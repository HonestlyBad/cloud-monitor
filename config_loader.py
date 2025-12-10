import yaml
from pathlib import Path

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

    # Verify config exists
    if not cfg_path.exists():
        raise FileNotFoundError(f"Config file not found: {path}")

    # Open and parse YAML safely
    with cfg_path.open() as f:
        data = yaml.safe_load(f)

    # Basic validation: ensure required keys exist
    if "services" not in data:
        raise ValueError("Config missing 'services' key.")

    return data
