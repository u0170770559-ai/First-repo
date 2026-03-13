"""
Alarm Clock Application

A tkinter-based alarm clock application for Windows with persistent storage.

Usage:
    python main.py

Author:
    Ridges bot

License:
    MIT License
"""

import tkinter as tk
from tkinter import ttk, messagebox
import winsound
import json
import threading
import time
import os
from datetime import datetime, timedelta
from typing import List, Dict, Optional
import sys


class Alarm:
    """Represents a single alarm with time, description, and state.
    
    Attributes:
        hour: Hour of the alarm (0-23)
        minute: Minute of the alarm (0-59)
        second: Second of the alarm (0-59)
        description: Description of the alarm
        enabled: Whether the alarm is enabled
        repeat: Whether the alarm repeats
    
    Example:
        >>> alarm = Alarm(7, 30, 0, "Morning Alarm", True, True)
    """
    
    def __init__(self, hour: int, minute: int, second: int = 0, description: str = "",
                 enabled: bool = True, repeat: bool = False):
        self.hour = hour
        self.minute = minute
        self.second = second
        self.description = description
        self.enabled = enabled
        self.repeat = repeat
        self.next_fire_time: Optional[datetime] = None
        self.fired = False
    
    def to_dict(self) -> Dict:
        """Convert alarm to dictionary for JSON serialization.
        
        Returns:
            Dictionary representation of the alarm.
        
    @classmethod
    def from_dict(cls, data: Dict) -> 'Alarm':
        """Create alarm from dictionary.
        
        Args:
            data: Dictionary representation of the alarm.
        
        Returns:
    
    class AlarmManager:
        """Manages a collection of alarms with persistence.
        
    class AlarmClockApp:
        """Main application class for the alarm clock GUI.
        
    if __name__ == "__main__":
        root = tk.Tk()
        app = AlarmClockApp(root)
    root.mainloop()
