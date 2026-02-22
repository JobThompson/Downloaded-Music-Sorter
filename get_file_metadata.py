from __future__ import annotations

from pathlib import Path

from win32com.client import Dispatch


shell = Dispatch("Shell.Application")


def get_file_metadata(file_path: str) -> dict[str, str]:
    """Return Windows Shell metadata key/value pairs for a file.

    Raises:
        ValueError: If the path is invalid.
        RuntimeError: If metadata cannot be retrieved.
    """
    path = Path(file_path)
    if not path.exists() or not path.is_file():
        raise ValueError(f"Invalid file path: {file_path}")

    metadata: dict[str, str] = {}
    namespace = shell.NameSpace(str(path.parent))
    if namespace is None:
        raise RuntimeError(f"Could not open namespace for: {path.parent}")

    item_name = path.stem
    for item in namespace.Items():
        if str(item) == item_name:
            for index in range(0, 500):
                key = namespace.GetDetailsOf(index, index)
                value = namespace.GetDetailsOf(item, index)
                if key:
                    metadata[key] = value
            break

    if not metadata:
        raise RuntimeError(f"No metadata found for file: {file_path}")

    return metadata
