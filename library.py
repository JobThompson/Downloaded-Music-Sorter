from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Iterable


DEFAULT_AUDIO_EXTENSIONS = {".mp3", ".mp4", ".flac", ".m4a", ".wav", ".ogg"}


def normalize_track_name(file_name: str) -> str:
    """Normalize track names for duplicate detection across naming schemes."""
    stem = Path(file_name).stem
    parts = [part.strip() for part in stem.split(" - ")]
    if len(parts) >= 3:
        stem = " - ".join(parts[2:])
    return stem.replace("(Explicit)", "").strip().casefold()


@dataclass(frozen=True, slots=True)
class LibraryTrack:
    """Represents one audio file discovered while scanning a library."""

    path: Path

    @property
    def file_name(self) -> str:
        return self.path.name

    @property
    def normalized_name(self) -> str:
        return normalize_track_name(self.file_name)


class Library:
    """Scans a root directory recursively and exposes discovered tracks."""

    def __init__(self, root_path: str, allowed_extensions: Iterable[str] | None = None):
        self.root = Path(root_path)
        self.allowed_extensions = {
            ext if ext.startswith(".") else f".{ext}"
            for ext in (allowed_extensions or DEFAULT_AUDIO_EXTENSIONS)
        }
        self.tracks = self._scan_tracks()
        self.songs = [track.normalized_name for track in self.tracks]

    def _scan_tracks(self) -> list[LibraryTrack]:
        """Collect all files matching supported extensions from the root."""
        discovered: list[LibraryTrack] = []
        if not self.root.exists() or not self.root.is_dir():
            return discovered

        for path in self.root.rglob("*"):
            if path.is_file() and path.suffix.lower() in self.allowed_extensions:
                discovered.append(LibraryTrack(path=path))
        return discovered

    def get_song_paths(self) -> list[str]:
        """Return all discovered track paths as strings."""
        return [str(track.path) for track in self.tracks]

    def get_song_paths_unstripped(self) -> list[str]:
        """Compatibility wrapper for previous API naming."""
        return self.get_song_paths()


