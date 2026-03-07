"""Alarm storage module - handles persistence of alarms to JSON file."""
import json
import os
from typing import List, Dict, Any, Optional
from datetime import datetime


class AlarmStore:
    """Manages alarm persistence using a JSON file."""
    
    def __init__(self, filepath: str = "alarms.json") -> None:
        """Initialize the alarm store with a filepath.
        
        Args:
            filepath: Path to the JSON file for storing alarms.
        """
        self.filepath = filepath
        self._alarms: List[Dict[str, Any]] = []
        self._load()
    
    def _load(self) -> None:
        """Load alarms from the JSON file."""
        if os.path.exists(self.filepath):
            try:
                with open(self.filepath, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    self._alarms = data.get('alarms', [])
            except (json.JSONDecodeError, IOError) as e:
                print(f"Warning: Could not load alarms: {e}")
                self._alarms = []
        else:
            self._alarms = []
    
    def _save(self) -> None:
        """Save alarms to the JSON file."""
        try:
            with open(self.filepath, 'w', encoding='utf-8') as f:
                json.dump({'alarms': self._alarms}, f, indent=2)
        except IOError as e:
            print(f"Error: Could not save alarms: {e}")
    
    def get_all(self) -> List[Dict[str, Any]]:
        """Get all alarms.
        
        Returns:
            List of alarm dictionaries.
        """
        return self._alarms.copy()
    
    def add(self, time_str: str) -> Optional[Dict[str, Any]]:
        """Add a new alarm.
        
        Args:
            time_str: Time in HH:MM format (24-hour).
            
        Returns:
            The created alarm dict, or None if invalid time.
        """
        if not self._validate_time(time_str):
            return None
        
        alarm = {
            'id': self._generate_id(),
            'time': time_str,
            'enabled': True
        }
        self._alarms.append(alarm)
        self._save()
        return alarm
    
    def delete(self, alarm_id: str) -> bool:
        """Delete an alarm by ID.
        
        Args:
            alarm_id: The ID of the alarm to delete.
            
        Returns:
            True if deleted, False if not found.
        """
        for i, alarm in enumerate(self._alarms):
            if alarm['id'] == alarm_id:
                self._alarms.pop(i)
                self._save()
                return True
        return False
    
    def delete_by_time(self, time_str: str) -> int:
        """Delete all alarms with a specific time.
        
        Args:
            time_str: Time in HH:MM format.
            
        Returns:
            Number of alarms deleted.
        """
        original_count = len(self._alarms)
        self._alarms = [a for a in self._alarms if a['time'] != time_str]
        deleted = original_count - len(self._alarms)
        if deleted > 0:
            self._save()
        return deleted
    
    def clear_triggered(self, time_str: str) -> None:
        """Remove all alarms that have triggered (for cleanup).
        
        Args:
            time_str: Current time to compare against.
        """
        self._alarms = [a for a in self._alarms if a['time'] > time_str]
        self._save()
    
    @staticmethod
    def _validate_time(time_str: str) -> bool:
        """Validate HH:MM time format.
        
        Args:
            time_str: Time string to validate.
            
        Returns:
            True if valid, False otherwise.
        """
        try:
            if len(time_str) != 5 or time_str[2] != ':':
                return False
            datetime.strptime(time_str, '%H:%M')
            return True
        except ValueError:
            return False
    
    def _generate_id(self) -> str:
        """Generate a unique alarm ID.
        
        Returns:
            Unique identifier string.
        """
        import uuid
        return str(uuid.uuid4())[:8]
