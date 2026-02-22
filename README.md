# Downloaded-Music-Sorter

A Python CLI tool to organize downloaded tracks, compare music libraries, and consolidate duplicates into a clean destination library.

## Features

- **Downloaded file sorting**
	- Sorts files from a download folder into artist-based directories.
	- Uses filename pattern: `track_no - artist - title.ext`.
	- Reports summary counts for moved/skipped files.

- **Library comparison + merge**
	- Recursively scans two libraries and compares normalized track names.
	- Prints tracks missing from each side.
	- Optionally merges unique tracks into a destination folder using metadata-aware deduplication.

- **Library consolidation**
	- Consolidates a library into one destination folder.
	- Uses Windows shell metadata to identify duplicates.
	- Copies only unique tracks.

## Architecture

- `main.py`
	- CLI entrypoint and user workflows.
	- Contains small, focused functions for each command.

- `library.py`
	- Recursive library scanner with normalized naming.
	- Exposes reusable track/path APIs.

- `sort_files_script.py`
	- Download-folder sorting logic.
	- No module-level global state.

- `music_file.py`
	- Shared config model and filename parsing utilities.
	- Filename sanitization helpers for safe Windows paths.

- `get_file_metadata.py`
	- Windows shell metadata adapter (`pywin32`).

## Requirements

- Python 3.10+
- Windows (metadata mode uses `pywin32` shell APIs)

Install dependencies:

```bash
pip install -r requirements.txt
```

## Configuration (Optional)

Filepath declarations can be stored in `.env` so workflows can run without prompts.

- `CURRENT_PLAYLIST_FILEPATH`
- `DESTINATION_FILEPATH`
- `COMPARE_LIBRARY_ONE_FILEPATH`
- `COMPARE_LIBRARY_TWO_FILEPATH`
- `MERGE_DESTINATION_FILEPATH`
- `CONSOLIDATE_SOURCE_FILEPATH`
- `CONSOLIDATE_DESTINATION_FILEPATH`

Example `.env`:

```env
CURRENT_PLAYLIST_FILEPATH=C:\\Music\\Downloads
DESTINATION_FILEPATH=C:\\Music\\Artists
COMPARE_LIBRARY_ONE_FILEPATH=D:\\Music\\LibraryA
COMPARE_LIBRARY_TWO_FILEPATH=E:\\Music\\LibraryB
MERGE_DESTINATION_FILEPATH=G:\\Music\\Merged
CONSOLIDATE_SOURCE_FILEPATH=E:\\Music
CONSOLIDATE_DESTINATION_FILEPATH=G:\\Music\\Consolidated
```

## Usage

```bash
python main.py
```

Then choose one of the menu options:

1. Sort downloaded files into artist folders
2. Compare two libraries and optionally merge unique tracks
3. Consolidate a library into a deduplicated destination folder

## Extending the Project

- Add new file types by updating extension sets in `library.py` and `sort_files_script.py`.
- Add new workflows by creating a focused function in `main.py` and registering it in `FUNCTIONS`.
- Reuse `Library` for any future operations that need recursive music-file discovery.

## Notes

- Sorting workflow expects downloaded filenames to include artist/title segments separated by ` - `.
- Consolidation relies on Windows metadata availability; fallback behavior is file-name based when tags are missing.
