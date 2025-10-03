#!/usr/bin/env python3
"""Backup and Disaster Recovery automation for RJW-IDD."""

from __future__ import annotations

import argparse
import json
import shutil
import subprocess
import sys
import time
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from pathlib import Path
from typing import Any, Dict, List, Optional

from tools.logging_config import get_logger, setup_logging

logger = get_logger(__name__)


@dataclass
class BackupConfig:
    """Configuration for backup operations."""

    source_paths: List[Path]
    backup_root: Path
    retention_days: int = 30
    compression: bool = True
    encryption_key: Optional[str] = None
    exclude_patterns: List[str] = field(default_factory=list)

    def __post_init__(self) -> None:
        self.backup_root.mkdir(parents=True, exist_ok=True)


@dataclass
class BackupResult:
    """Result of a backup operation."""

    success: bool
    backup_path: Optional[Path]
    size_bytes: int
    duration_seconds: float
    error_message: Optional[str] = None
    timestamp: datetime = field(default_factory=datetime.now)


class BackupManager:
    """Manage backup and restore operations."""

    def __init__(self, config: BackupConfig):
        self.config = config
        self.logger = get_logger(f"{__name__}.backup")

    def create_backup(self, name: Optional[str] = None) -> BackupResult:
        """Create a backup of configured paths."""
        start_time = time.time()
        timestamp = datetime.now()

        if name:
            backup_name = f"{name}_{timestamp.strftime('%Y%m%d_%H%M%S')}"
        else:
            backup_name = timestamp.strftime('%Y%m%d_%H%M%S')

        backup_path = self.config.backup_root / backup_name

        try:
            backup_path.mkdir(parents=True, exist_ok=True)

            total_size = 0
            for source_path in self.config.source_paths:
                if not source_path.exists():
                    self.logger.warning(f"Source path does not exist: {source_path}")
                    continue

                # Copy files with exclusion
                dest_path = backup_path / source_path.name
                self._copy_with_exclusions(source_path, dest_path)
                total_size += self._get_directory_size(dest_path)

            # Create metadata
            metadata = {
                "timestamp": timestamp.isoformat(),
                "sources": [str(p) for p in self.config.source_paths],
                "size_bytes": total_size,
                "compression": self.config.compression,
                "retention_days": self.config.retention_days,
            }

            metadata_file = backup_path / "backup_metadata.json"
            with metadata_file.open('w') as f:
                json.dump(metadata, f, indent=2)

            duration = time.time() - start_time
            self.logger.info(f"Backup completed: {backup_path} ({total_size} bytes in {duration:.2f}s)")

            return BackupResult(
                success=True,
                backup_path=backup_path,
                size_bytes=total_size,
                duration_seconds=duration
            )

        except Exception as e:
            duration = time.time() - start_time
            error_msg = f"Backup failed: {e}"
            self.logger.error(error_msg)

            # Clean up failed backup
            if backup_path.exists():
                shutil.rmtree(backup_path)

            return BackupResult(
                success=False,
                backup_path=None,
                size_bytes=0,
                duration_seconds=duration,
                error_message=error_msg
            )

    def restore_backup(self, backup_path: Path, restore_to: Path) -> BackupResult:
        """Restore from a backup."""
        start_time = time.time()

        try:
            if not backup_path.exists():
                raise FileNotFoundError(f"Backup does not exist: {backup_path}")

            # Validate backup metadata
            metadata_file = backup_path / "backup_metadata.json"
            if metadata_file.exists():
                with metadata_file.open() as f:
                    metadata = json.load(f)
                self.logger.info(f"Restoring backup from {metadata.get('timestamp', 'unknown')}")

            # Restore files
            total_size = 0
            for item in backup_path.iterdir():
                if item.name == "backup_metadata.json":
                    continue

                dest_path = restore_to / item.name
                if item.is_file():
                    shutil.copy2(item, dest_path)
                    total_size += item.stat().st_size
                elif item.is_dir():
                    shutil.copytree(item, dest_path, dirs_exist_ok=True)
                    total_size += self._get_directory_size(item)

            duration = time.time() - start_time
            self.logger.info(f"Restore completed: {total_size} bytes in {duration:.2f}s")

            return BackupResult(
                success=True,
                backup_path=backup_path,
                size_bytes=total_size,
                duration_seconds=duration
            )

        except Exception as e:
            duration = time.time() - start_time
            error_msg = f"Restore failed: {e}"
            self.logger.error(error_msg)

            return BackupResult(
                success=False,
                backup_path=backup_path,
                size_bytes=0,
                duration_seconds=duration,
                error_message=error_msg
            )

    def cleanup_old_backups(self) -> int:
        """Remove backups older than retention period."""
        cutoff_date = datetime.now() - timedelta(days=self.config.retention_days)
        removed_count = 0

        for backup_dir in self.config.backup_root.iterdir():
            if not backup_dir.is_dir():
                continue

            try:
                # Try to parse timestamp from directory name
                # Format: YYYYMMDD_HHMMSS or name_YYYYMMDD_HHMMSS
                name_parts = backup_dir.name.split('_')
                if len(name_parts) >= 2:
                    date_str = name_parts[-2] + '_' + name_parts[-1]
                    if len(date_str) == 15:  # YYYYMMDD_HHMMSS
                        backup_date = datetime.strptime(date_str, '%Y%m%d_%H%M%S')
                        if backup_date < cutoff_date:
                            shutil.rmtree(backup_dir)
                            removed_count += 1
                            self.logger.info(f"Removed old backup: {backup_dir}")
            except (ValueError, OSError) as e:
                self.logger.warning(f"Could not process backup directory {backup_dir}: {e}")

        return removed_count

    def list_backups(self) -> List[Dict[str, Any]]:
        """List all available backups."""
        backups = []

        for backup_dir in self.config.backup_root.iterdir():
            if not backup_dir.is_dir():
                continue

            metadata_file = backup_dir / "backup_metadata.json"
            metadata = {}

            if metadata_file.exists():
                try:
                    with metadata_file.open() as f:
                        metadata = json.load(f)
                except (OSError, json.JSONDecodeError):
                    pass

            backups.append({
                "path": backup_dir,
                "name": backup_dir.name,
                "size_bytes": self._get_directory_size(backup_dir),
                "metadata": metadata,
            })

        return sorted(backups, key=lambda x: x["name"], reverse=True)

    def _copy_with_exclusions(self, src: Path, dst: Path) -> None:
        """Copy directory tree with exclusion patterns."""
        import fnmatch

        if dst.exists():
            shutil.rmtree(dst)
        dst.mkdir(parents=True)

        for item in src.rglob('*'):
            if item.is_file():
                # Check exclusion patterns
                relative_path = item.relative_to(src)
                should_exclude = any(
                    fnmatch.fnmatch(str(relative_path), pattern)
                    for pattern in self.config.exclude_patterns
                )

                if not should_exclude:
                    dest_file = dst / relative_path
                    dest_file.parent.mkdir(parents=True, exist_ok=True)
                    shutil.copy2(item, dest_file)

    def _get_directory_size(self, path: Path) -> int:
        """Get total size of directory in bytes."""
        total_size = 0
        for item in path.rglob('*'):
            if item.is_file():
                total_size += item.stat().st_size
        return total_size


def create_default_config(project_root: Path) -> BackupConfig:
    """Create default backup configuration for RJW-IDD project."""
    return BackupConfig(
        source_paths=[
            project_root / "artifacts",
            project_root / "research",
            project_root / "logs",
            project_root / "specs",
        ],
        backup_root=project_root / "backups",
        retention_days=30,
        exclude_patterns=[
            "*.pyc",
            "__pycache__",
            ".pytest_cache",
            "*.log",
            "*.tmp",
        ]
    )


def main() -> int:
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(description="RJW-IDD Backup Manager")
    parser.add_argument("--config", type=Path, help="Backup configuration file")
    parser.add_argument("--project-root", type=Path, default=Path.cwd(),
                       help="Project root directory")
    parser.add_argument("--backup", action="store_true", help="Create backup")
    parser.add_argument("--restore", type=Path, help="Restore from backup path")
    parser.add_argument("--restore-to", type=Path, help="Restore destination")
    parser.add_argument("--cleanup", action="store_true", help="Cleanup old backups")
    parser.add_argument("--list", action="store_true", help="List available backups")
    parser.add_argument("--name", help="Backup name prefix")

    args = parser.parse_args()

    setup_logging()

    if args.config and args.config.exists():
        # Load config from file (future enhancement)
        config = create_default_config(args.project_root)
    else:
        config = create_default_config(args.project_root)

    manager = BackupManager(config)

    if args.backup:
        result = manager.create_backup(args.name)
        if result.success:
            print(f"✅ Backup created: {result.backup_path}")
            return 0
        else:
            print(f"❌ Backup failed: {result.error_message}")
            return 1

    elif args.restore:
        if not args.restore_to:
            print("❌ --restore-to is required for restore operation")
            return 1

        result = manager.restore_backup(args.restore, args.restore_to)
        if result.success:
            print(f"✅ Restore completed from {args.restore}")
            return 0
        else:
            print(f"❌ Restore failed: {result.error_message}")
            return 1

    elif args.cleanup:
        removed = manager.cleanup_old_backups()
        print(f"✅ Cleaned up {removed} old backups")
        return 0

    elif args.list:
        backups = manager.list_backups()
        if not backups:
            print("No backups found")
            return 0

        print("Available backups:")
        for backup in backups:
            size_mb = backup["size_bytes"] / (1024 * 1024)
            timestamp = backup["metadata"].get("timestamp", "unknown")
            print(f"  {backup['name']} ({size_mb:.1f} MB) - {timestamp}")
        return 0

    else:
        parser.print_help()
        return 1


if __name__ == "__main__":
    sys.exit(main())