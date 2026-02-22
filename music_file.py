from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Optional

from decouple import config


INVALID_FILENAME_CHARS = '<>:"/\\|?*'


def sanitize_filename(value: str) -> str:
    """Return a filesystem-safe filename segment for Windows paths."""
    cleaned = value.strip()
    for char in INVALID_FILENAME_CHARS:
        cleaned = cleaned.replace(char, "-")
    return " ".join(cleaned.split())


@dataclass(slots=True)
class AppConfig:
    """Runtime configuration loaded from environment variables.

    The values are optional to support interactive prompts as fallback.
    """

    current_playlist_filepath: Optional[str] = None
    destination_filepath: Optional[str] = None
    compare_library_one_filepath: Optional[str] = None
    compare_library_two_filepath: Optional[str] = None
    merge_destination_filepath: Optional[str] = None
    consolidate_source_filepath: Optional[str] = None
    consolidate_destination_filepath: Optional[str] = None

    @classmethod
    def from_environment(cls) -> "AppConfig":
        """Load known values from environment variables when available."""
        return cls(
            current_playlist_filepath=config("CURRENT_PLAYLIST_FILEPATH", default=None),
            destination_filepath=config("DESTINATION_FILEPATH", default=None),
            compare_library_one_filepath=config("COMPARE_LIBRARY_ONE_FILEPATH", default=None),
            compare_library_two_filepath=config("COMPARE_LIBRARY_TWO_FILEPATH", default=None),
            merge_destination_filepath=config("MERGE_DESTINATION_FILEPATH", default=None),
            consolidate_source_filepath=config("CONSOLIDATE_SOURCE_FILEPATH", default=None),
            consolidate_destination_filepath=config("CONSOLIDATE_DESTINATION_FILEPATH", default=None),
        )


@dataclass(slots=True)
class ParsedDownloadFile:
    """Parsed representation of a downloaded music filename.

    Expected pattern: ``{track_no} - {artist} - {title}``.
    """

    full_name: str
    track_number: Optional[str]
    artist: str
    title: str

    @property
    def stripped_title(self) -> str:
        """Return a cleaned title suitable for destination filenames."""
        return sanitize_filename(self.title.replace("(Explicit)", "").strip())

    @classmethod
    def try_parse(cls, file_name: str) -> Optional["ParsedDownloadFile"]:
        """Parse a downloaded filename or return None when not matching pattern."""
        stem = Path(file_name).stem
        parts = [part.strip() for part in stem.split(" - ")]
        if len(parts) < 3:
            return None

        return cls(
            full_name=file_name,
            track_number=parts[0] or None,
            artist=parts[1] or "Unknown",
            title=" - ".join(parts[2:]) or stem,
        )
        