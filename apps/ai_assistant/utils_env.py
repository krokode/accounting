"""
Safe .env file manipulation utilities.
"""
import os
from pathlib import Path
from django.conf import settings


def get_env_path() -> Path:
    return Path(settings.BASE_DIR) / '.env'


def update_env_variables(updates: dict):
    """
    Safely updates or appends key-value pairs in the .env file,
    preserving existing comments and other environment variables.
    """
    env_path = get_env_path()
    lines = []
    if env_path.exists():
        with open(env_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()

    updated_keys = set()
    new_lines = []

    for line in lines:
        stripped = line.strip()
        if stripped and not stripped.startswith('#') and '=' in stripped:
            key, _ = stripped.split('=', 1)
            key = key.strip()
            if key in updates:
                new_val = str(updates[key]).strip()
                new_lines.append(f"{key}={new_val}\n")
                updated_keys.add(key)
                continue
        new_lines.append(line)

    # Append any keys that weren't already present in .env
    for key, val in updates.items():
        if key not in updated_keys and val is not None:
            new_lines.append(f"{key}={str(val).strip()}\n")

    with open(env_path, 'w', encoding='utf-8') as f:
        f.writelines(new_lines)
