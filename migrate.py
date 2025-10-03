#!/usr/bin/env python3
"""
Database migration management script.

Usage:
    python migrate.py create "migration name"  # Create new migration
    python migrate.py upgrade                  # Apply all pending migrations
    python migrate.py downgrade -1             # Downgrade by 1 revision
    python migrate.py current                  # Show current revision
    python migrate.py history                  # Show migration history
"""

import subprocess
import sys
from pathlib import Path

# Add project root to Python path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))


def run_alembic_command(args: list[str]) -> int:
    """Run alembic command with uv."""
    cmd = ["uv", "run", "alembic"] + args
    result = subprocess.run(cmd, capture_output=True, text=True)

    if result.stdout:
        print(result.stdout)
    if result.stderr:
        print(result.stderr, file=sys.stderr)

    return result.returncode


def main() -> None:
    """Main function."""
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)

    command = sys.argv[1].lower()

    if command == "create":
        if len(sys.argv) < 3:
            print("Usage: python migrate.py create 'migration name'")
            sys.exit(1)

        migration_name = sys.argv[2]
        exit_code = run_alembic_command(["revision", "--autogenerate", "-m", migration_name])

    elif command == "upgrade":
        target = sys.argv[2] if len(sys.argv) > 2 else "head"
        exit_code = run_alembic_command(["upgrade", target])

    elif command == "downgrade":
        target = sys.argv[2] if len(sys.argv) > 2 else "-1"
        exit_code = run_alembic_command(["downgrade", target])

    elif command == "current":
        exit_code = run_alembic_command(["current"])

    elif command == "history":
        exit_code = run_alembic_command(["history"])

    elif command == "show":
        if len(sys.argv) < 3:
            print("Usage: python migrate.py show <revision>")
            sys.exit(1)

        revision = sys.argv[2]
        exit_code = run_alembic_command(["show", revision])

    else:
        print(f"Unknown command: {command}")
        print(__doc__)
        sys.exit(1)

    sys.exit(exit_code)


if __name__ == "__main__":
    main()
