"""Command-line interface for the alarm clock."""
import argparse
import sys
import time
from typing import Optional
from alarm_store import AlarmStore
from scheduler import AlarmScheduler


def format_alarm_list(alarms: list) -> str:
    """Format a list of alarms for display.
    
    Args:
        alarms: List of alarm dictionaries.
        
    Returns:
        Formatted string representation.
    """
    if not alarms:
        return "No alarms set."
    
    lines = ["ID        | Time  | Status"]
    lines.append("-" * 30)
    for alarm in alarms:
        status = "enabled" if alarm.get('enabled', True) else "disabled"
        lines.append(f"{alarm['id']:<9} | {alarm['time']:<5} | {status}")
    
    return "\n".join(lines)


def add_alarm(store: AlarmStore, time_str: str) -> None:
    """Add a new alarm.
    
    Args:
        store: AlarmStore instance.
        time_str: Time in HH:MM format.
    """
    alarm = store.add(time_str)
    if alarm:
        print(f"Alarm added: {time_str} (ID: {alarm['id']})")
    else:
        print(f"Error: Invalid time format '{time_str}'. Use HH:MM (24-hour).")
        sys.exit(1)


def list_alarms(store: AlarmStore) -> None:
    """List all alarms.
    
    Args:
        store: AlarmStore instance.
    """
    alarms = store.get_all()
    print(format_alarm_list(alarms))


def delete_alarm(store: AlarmStore, alarm_id: str) -> None:
    """Delete an alarm by ID.
    
    Args:
        store: AlarmStore instance.
        alarm_id: ID of the alarm to delete.
    """
    if store.delete(alarm_id):
        print(f"Alarm {alarm_id} deleted successfully.")
    else:
        print(f"Error: Alarm {alarm_id} not found.")
        sys.exit(1)


def delete_alarm_by_time(store: AlarmStore, time_str: str) -> None:
    """Delete all alarms at a specific time.
    
    Args:
        store: AlarmStore instance.
        time_str: Time in HH:MM format.
    """
    count = store.delete_by_time(time_str)
    if count > 0:
        print(f"Deleted {count} alarm(s) at {time_str}.")
    else:
        print(f"No alarms found at {time_str}.")


def run_monitor_mode(store: AlarmStore) -> None:
    """Run in monitor mode - continuously check for alarms.
    
    Args:
        store: AlarmStore instance.
    """
    scheduler = AlarmScheduler(store)
    scheduler.start()
    
    print("Alarm monitor started. Press Ctrl+C to stop.")
    print(f"Current alarms: {len(store.get_all())}")
    
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\nStopping alarm monitor...")
        scheduler.stop()


def main(args: Optional[list] = None) -> int:
    """Main entry point for CLI.
    
    Args:
        args: Command-line arguments.
        
    Returns:
        Exit code (0 for success, 1 for error).
    """
    parser = argparse.ArgumentParser(
        description="Alarm Clock CLI - Manage your alarms from the command line."
    )
    
    subparsers = parser.add_subparsers(dest='command', help='Available commands')
    
    # Add command
    add_parser = subparsers.add_parser('add', help='Add a new alarm')
    add_parser.add_argument('time', help='Alarm time in HH:MM format (24-hour)')
    
    # List command
    subparsers.add_parser('list', help='List all alarms')
    
    # Delete command
    delete_parser = subparsers.add_parser('delete', help='Delete an alarm')
    delete_parser.add_argument('id', help='Alarm ID to delete')
    
    # Delete-by-time command
    deltime_parser = subparsers.add_parser(
        'delete-time', help='Delete all alarms at a specific time'
    )
    deltime_parser.add_argument('time', help='Time in HH:MM format')
    
    # Monitor command
    subparsers.add_parser(
        'monitor', help='Run in monitor mode (watch for alarms)'
    )
    
    parsed = parser.parse_args(args)
    
    store = AlarmStore()
    
    if parsed.command == 'add':
        add_alarm(store, parsed.time)
    elif parsed.command == 'list':
        list_alarms(store)
    elif parsed.command == 'delete':
        delete_alarm(store, parsed.id)
    elif parsed.command == 'delete-time':
        delete_alarm_by_time(store, parsed.time)
    elif parsed.command == 'monitor':
        run_monitor_mode(store)
    else:
        parser.print_help()
        return 1
    
    return 0


if __name__ == '__main__':
    sys.exit(main())
