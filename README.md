# Alarm Clock

A simple cross-platform alarm clock application written in Python with both CLI and GUI interfaces.

## Features

- **Command-line interface (CLI)** for setting, listing, and deleting alarms
- **Graphical user interface (GUI)** built with Tkinter
- **Persistent storage** using JSON file
- **Cross-platform sound notifications** (with fallback beep)
- **Popup notifications** when alarms trigger
- **Real-time clock display** in GUI

## Requirements

- Python 3.7+
- Tkinter (usually included with Python)

## Installation

No additional dependencies required! The application uses only Python standard library modules.

```bash
# Clone or download the repository
git clone <repository-url>
cd <repository-directory>
```

## Usage

### GUI Mode (Default)

Run the application without any arguments to start the GUI:

```bash
python main.py
# or
python main.py --gui
```

The GUI provides:
- Real-time clock display
- Input fields to set alarms (HH:MM format)
- List of upcoming alarms
- Delete functionality for alarms
- Popup notifications when alarms trigger

### CLI Mode

Run with `--cli` flag followed by commands:

```bash
# Add an alarm
python main.py --cli add 08:30

# List all alarms
python main.py --cli list

# Delete an alarm by ID
python main.py --cli delete <alarm-id>

# Delete all alarms at a specific time
python main.py --cli delete-time 08:30

# Run in monitor mode (watch for alarms)
python main.py --cli monitor

# Get help
python main.py --cli --help
```

## Project Structure

```
.
├── main.py           # Entry point - choose CLI or GUI
├── cli.py            # Command-line interface
├── gui.py            # Tkinter graphical interface
├── alarm_store.py    # JSON persistence for alarms
├── scheduler.py      # Alarm monitoring and triggering
├── tests/
│   └── test_alarm.py # Unit tests
└── README.md         # This file
```

## Testing

Run the unit tests using pytest:

```bash
# Install pytest if not already installed
pip install pytest

# Run tests
pytest tests/test_alarm.py -v
```

The tests cover:
- Alarm storage and persistence
- Time validation
- Adding, deleting, and listing alarms
- Scheduler initialization and operation

## How It Works

1. **Alarm Storage**: Alarms are stored in `alarms.json` with a unique ID, time (HH:MM), and enabled status.

2. **Scheduler**: A background thread continuously checks if any alarm times match the current time.

3. **Notifications**: When an alarm triggers:
   - A sound is played (platform-specific or beep fallback)
   - A popup notification is shown

4. **GUI**: Tkinter provides an intuitive interface with auto-updating time display and alarm management.

## Platform Support

- **macOS**: Uses `afplay` for sounds
- **Windows**: Uses `winsound` module
- **Linux**: Uses `paplay` or `aplay`
- **All platforms**: Falls back to terminal bell character

## License

MIT License - feel free to use and modify as needed.