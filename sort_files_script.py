from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Iterable

from music_file import ParsedDownloadFile, sanitize_filename


SUPPORTED_SORT_INPUT_EXTENSIONS = {".mp3", ".mp4", ".flac", ".m4a", ".wav", ".ogg"}


@dataclass(slots=True)
class SortResult:
    """Summary of one sorting operation."""

    moved: int = 0
    skipped_invalid_name: int = 0
    skipped_unsupported_type: int = 0


def check_for_artist_folder(name: str, destination_root: str) -> Path:
    """Ensure artist directory exists and return its path.

    The first artist in multi-artist names is used for primary grouping.
    """
    artist_name = sanitize_filename(name.split(",")[0].strip() or "Unknown")
    artist_path = Path(destination_root) / artist_name
    artist_path.mkdir(parents=True, exist_ok=True)
    return artist_path


def iter_source_files(source_dir: Path, allowed_extensions: Iterable[str]) -> Iterable[Path]:
    """Yield files in source directory matching allowed extensions."""
    normalized_extensions = {
        ext if ext.startswith(".") else f".{ext}" for ext in allowed_extensions
    }
    for path in source_dir.iterdir():
        if path.is_file() and path.suffix.lower() in normalized_extensions:
            yield path


def sort_files_script(sort_file_path: str, new_repository_path: str) -> SortResult:
    """Sort downloaded files into artist folders using filename structure.

    Expects source files in pattern: ``{track_no} - {artist} - {title}.{ext}``.
    """
    source_dir = Path(sort_file_path)
    destination_dir = Path(new_repository_path)
    destination_dir.mkdir(parents=True, exist_ok=True)

    result = SortResult()
    for source_path in source_dir.iterdir():
        if not source_path.is_file():
            continue

        if source_path.suffix.lower() not in SUPPORTED_SORT_INPUT_EXTENSIONS:
            result.skipped_unsupported_type += 1
            continue

        parsed = ParsedDownloadFile.try_parse(source_path.name)
        if parsed is None:
            result.skipped_invalid_name += 1
            continue

        artist_dir = check_for_artist_folder(parsed.artist, str(destination_dir))
        destination_file = artist_dir / f"{parsed.stripped_title}{source_path.suffix.lower()}"

        # os.replace moves the file atomically on the same drive and overwrites target.
        source_path.replace(destination_file)
        result.moved += 1

    return result