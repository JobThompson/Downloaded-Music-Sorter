from __future__ import annotations

from pathlib import Path
import shutil

from get_file_metadata import get_file_metadata
from library import Library
from music_file import AppConfig, sanitize_filename
from sort_files_script import check_for_artist_folder, sort_files_script


FUNCTIONS = {
    1: "Sort downloaded files into artist folders.",
    2: "Compare two libraries and optionally merge unique tracks.",
    3: "Consolidate a library by copying unique tracks into one folder.",
}

ALLOWED_FILETYPES = {".mp3", ".mp4", ".flac", ".m4a", ".wav", ".ogg"}


def get_function() -> int:
    """Prompt for a menu option and validate user input."""
    while True:
        print("Select the function you would like to perform:")
        for option, description in FUNCTIONS.items():
            print(f"{option}. {description}")

        selection = input("Selection (or 'exit'): ").strip().lower()
        if selection in {"exit", "quit"}:
            raise SystemExit
        if selection.isdigit() and int(selection) in FUNCTIONS:
            return int(selection)
        print("That is not a valid selection, please choose one of the listed options.\n")


def metadata_identity(file_path: str) -> tuple[str, str]:
    """Build a duplicate-detection identity from tags, with safe fallbacks."""
    metadata = get_file_metadata(file_path)
    title = (
        metadata.get("Title")
        or metadata.get("Filename")
        or Path(file_path).stem
    ).strip()
    artist = (
        metadata.get("Album artist")
        or metadata.get("Authors")
        or metadata.get("Contributing artists")
        or "Unknown"
    ).strip()
    return title.casefold(), artist.casefold()


def compare_libraries(config: AppConfig) -> None:
    """Compare two libraries and optionally merge unique tracks to destination."""
    library1_path = config.compare_library_one_filepath or input("Enter filepath for the first library: ").strip()
    library2_path = config.compare_library_two_filepath or input("Enter filepath for the second library: ").strip()

    library_one = Library(library1_path)
    library_two = Library(library2_path)

    songs_one = set(library_one.songs)
    songs_two = set(library_two.songs)

    missing_from_two = sorted(songs_one - songs_two)
    missing_from_one = sorted(songs_two - songs_one)

    print("\nTracks in library 1 but not library 2:")
    for name in missing_from_two:
        print(f"- {name}")

    print("\nTracks in library 2 but not library 1:")
    for name in missing_from_one:
        print(f"- {name}")

    response = input("\nDo you want to merge unique tracks from both libraries? (Y/N): ").strip().lower()
    if response != "y":
        return

    destination_filepath = config.merge_destination_filepath or input("Enter destination filepath for the merged library: ").strip()
    destination_root = Path(destination_filepath)
    destination_root.mkdir(parents=True, exist_ok=True)

    seen: set[tuple[str, str]] = set()
    copied = 0
    for track_path in library_one.get_song_paths() + library_two.get_song_paths():
        try:
            identity = metadata_identity(track_path)
            if identity in seen:
                continue

            metadata = get_file_metadata(track_path)
            artist = (
                metadata.get("Album artist")
                or metadata.get("Authors")
                or metadata.get("Contributing artists")
                or "Unknown"
            ).strip()
            title = (
                metadata.get("Title")
                or metadata.get("Filename")
                or Path(track_path).stem
            ).strip()

            artist_dir = check_for_artist_folder(artist, str(destination_root))
            extension = Path(track_path).suffix.lower() or ".flac"
            output_path = artist_dir / f"{sanitize_filename(title)}{extension}"

            shutil.copy2(track_path, output_path)
            seen.add(identity)
            copied += 1
        except (OSError, TypeError, ValueError, RuntimeError) as error:
            print(f"Could not copy '{track_path}': {error}")

    print(f"Merged {copied} unique tracks into {destination_root}")


def metadata_identifier(metadata: dict[str, str], fallback_path: str) -> str:
    """Create a stable identifier used during consolidation deduplication."""
    title = (metadata.get("Title") or metadata.get("Filename") or Path(fallback_path).stem).strip()
    primary_artist = (
        metadata.get("Album artist")
        or metadata.get("Authors")
        or metadata.get("Contributing artists")
        or "Unknown"
    ).strip()
    return f"{title.casefold()}::{primary_artist.casefold()}"


def consolidate_library(config: AppConfig) -> None:
    """Copy unique tracks from source library to a single destination folder."""
    source_path = config.consolidate_source_filepath or input("Enter source library path to consolidate: ").strip()
    destination_path = config.consolidate_destination_filepath or input("Enter destination folder for consolidated tracks: ").strip()

    source_library = Library(source_path)
    destination_root = Path(destination_path)
    destination_root.mkdir(parents=True, exist_ok=True)

    seen_identifiers: set[str] = set()
    copied = 0
    total = len(source_library.get_song_paths_unstripped())

    for index, file_path in enumerate(source_library.get_song_paths_unstripped(), start=1):
        path = Path(file_path)
        if path.suffix.lower() not in ALLOWED_FILETYPES:
            continue

        try:
            metadata = get_file_metadata(file_path)
            identifier = metadata_identifier(metadata, file_path)
            if identifier in seen_identifiers:
                continue

            seen_identifiers.add(identifier)
            cleaned_name = sanitize_filename(path.stem) + path.suffix.lower()
            target_path = destination_root / cleaned_name

            shutil.copy2(file_path, target_path)
            copied += 1
            print(f"{index}/{total} copied: {path.name}")
        except (OSError, ValueError, RuntimeError) as error:
            print(f"Could not process '{file_path}': {error}")

    print(f"Consolidation complete. Copied {copied} unique tracks to {destination_root}")


def sort_downloaded_files(config: AppConfig) -> None:
    """Sort downloaded playlist files, preferring environment config values."""
    source = config.current_playlist_filepath or input("Enter source download folder path: ").strip()
    destination = config.destination_filepath or input("Enter destination music folder path: ").strip()
    result = sort_files_script(source, destination)
    print(
        f"Sort complete. Moved: {result.moved}, "
        f"Skipped invalid name: {result.skipped_invalid_name}, "
        f"Skipped unsupported type: {result.skipped_unsupported_type}"
    )


def main() -> None:
    """Main CLI entry point for all music organization workflows."""
    config = AppConfig.from_environment()
    selection = get_function()

    if selection == 1:
        sort_downloaded_files(config)
    elif selection == 2:
        compare_libraries(config)
    elif selection == 3:
        consolidate_library(config)


if __name__ == "__main__":
    main()