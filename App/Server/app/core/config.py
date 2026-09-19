"""Settings come from config.env (next to setup.ps1). Real environment variables win over the file.
Set APP_CONFIG to point at a different file."""
import os
from pathlib import Path

_DEFAULT_FILE = Path(__file__).resolve().parents[2] / "config.env"


def _load_file() -> dict[str, str]:
    path = Path(os.environ.get("APP_CONFIG", _DEFAULT_FILE))
    values: dict[str, str] = {}
    if path.is_file():
        for line in path.read_text(encoding="utf-8").splitlines():
            line = line.strip()
            if not line or line.startswith("#") or "=" not in line:
                continue
            key, _, value = line.partition("=")
            values[key.strip()] = value.strip().strip("\"'")
    return values


_file_values = _load_file()


def get(key: str, default: str = "") -> str:
    return os.environ.get(key) or _file_values.get(key) or default


HOST = get("APP_HOST", "127.0.0.1")
PORT = int(get("APP_PORT", "8000"))
