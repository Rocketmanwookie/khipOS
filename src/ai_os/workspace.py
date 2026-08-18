from __future__ import annotations

from pathlib import Path


IGNORED_NAMES = {".git", "__pycache__", ".pytest_cache"}


class WorkspaceExplorer:
    def __init__(self, root: Path, max_entries: int = 200):
        self.root = root.resolve()
        self.max_entries = max_entries

    def _resolve(self, relative_path: str = ".") -> Path:
        if not relative_path.strip():
            relative_path = "."
        requested = Path(relative_path)
        if requested.is_absolute():
            raise ValueError("Workspace paths must be relative")
        resolved = (self.root / requested).resolve()
        if resolved != self.root and self.root not in resolved.parents:
            raise ValueError("Workspace path escapes the configured root")
        return resolved

    def list_entries(self, relative_path: str = ".") -> dict:
        directory = self._resolve(relative_path)
        if not directory.exists():
            raise ValueError(f"Workspace path does not exist: {relative_path}")
        if not directory.is_dir():
            raise ValueError(f"Workspace path is not a directory: {relative_path}")

        entries = []
        for child in sorted(directory.iterdir(), key=lambda path: (path.is_file(), path.name.lower())):
            if child.name in IGNORED_NAMES:
                continue
            child_relative = child.relative_to(self.root).as_posix()
            entries.append(
                {
                    "name": child.name,
                    "path": child_relative,
                    "type": "directory" if child.is_dir() else "file",
                    "size_bytes": child.stat().st_size if child.is_file() else None,
                }
            )
            if len(entries) >= self.max_entries:
                break

        return {
            "root": str(self.root),
            "path": directory.relative_to(self.root).as_posix() if directory != self.root else ".",
            "entries": entries,
            "truncated": len(entries) >= self.max_entries,
        }
