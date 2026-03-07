#!/usr/bin/env python3
"""Alarm Clock - Main entry point.

Provides both CLI and GUI interfaces for managing alarms.
Usage:
    python main.py --cli [command]    # Run CLI mode
    python main.py --gui              # Run GUI mode (default)
    python main.py -h                 # Show help
"""
import argparse
import sys


def main() -> int:
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="Alarm Clock - Cross-platform alarm clock with CLI and GUI"
    )
    parser.add_argument(
        '--cli', action='store_true',
        help='Run in CLI mode instead of GUI'
    )
    parser.add_argument(
        'cli_args', nargs='*',
        help='Arguments to pass to CLI (when using --cli)'
    )
    
    args = parser.parse_args()
    
    if args.cli:
        # Import and run CLI
        from cli import main as cli_main
        return cli_main(args.cli_args if args.cli_args else None)
    else:
        # Import and run GUI
        from gui import main as gui_main
        gui_main()
        return 0


if __name__ == '__main__':
    sys.exit(main())
