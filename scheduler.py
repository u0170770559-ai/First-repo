"""Scheduler module - monitors and triggers alarms."""
import threading
import time
import sys
import os
from datetime import datetime
from typing import Callable, List, Dict, Any, Optional
from alarm_store import AlarmStore


class AlarmScheduler:
    """Monitors alarms and triggers them when their time is reached."""
    
    def __init__(self, store: AlarmStore, 
                 on_trigger: Optional[Callable[[str], None]] = None) -> None:
        """Initialize the scheduler.
        
        Args:
            store: AlarmStore instance for alarm persistence.
            on_trigger: Callback function called with alarm time when triggered.
        """
        self.store = store
        self.on_trigger = on_trigger
        self._running = False
        self._thread: Optional[threading.Thread] = None
        self._triggered_today: set = set()
        self._lock = threading.Lock()
    
    def start(self) -> None:
        """Start the scheduler in a background thread."""
        if self._running:
            return
        
        self._running = True
        self._thread = threading.Thread(target=self._run, daemon=True)
        self._thread.start()
    
    def stop(self) -> None:
        """Stop the scheduler."""
        self._running = False
        if self._thread and self._thread.is_alive():
            self._thread.join(timeout=1.0)
    
    def _run(self) -> None:
        """Main scheduler loop - checks for alarms every second."""
        last_date = datetime.now().date()
        
        while self._running:
            now = datetime.now()
            current_time = now.strftime('%H:%M')
            current_date = now.date()
            
            # Reset triggered set on new day
            if current_date != last_date:
                with self._lock:
                    self._triggered_today.clear()
                last_date = current_date
            
            # Check all alarms
            alarms = self.store.get_all()
            for alarm in alarms:
                if alarm.get('enabled', True) and alarm['time'] == current_time:
                    alarm_key = f"{alarm['id']}:{current_date}"
                    with self._lock:
                        if alarm_key not in self._triggered_today:
                            self._triggered_today.add(alarm_key)
                            self._trigger_alarm(alarm['time'])
            
            time.sleep(1)
    
    def _trigger_alarm(self, alarm_time: str) -> None:
        """Handle alarm trigger - play sound and show notification.
        
        Args:
            alarm_time: The time string of the triggered alarm.
        """
        self._play_sound()
        
        if self.on_trigger:
            self.on_trigger(alarm_time)
        else:
            self._default_notification(alarm_time)
    
    def _play_sound(self) -> None:
        """Play an alarm sound using cross-platform methods."""
        # Try platform-specific methods in order of preference
        if sys.platform == 'darwin':  # macOS
            try:
                os.system('afplay /System/Library/Sounds/Glass.aiff')
            except Exception:
                pass
        elif sys.platform == 'win32':  # Windows
            try:
                import winsound
                winsound.MessageBeep(winsound.MB_ICONEXCLAMATION)
            except Exception:
                pass
        elif sys.platform == 'linux':  # Linux
            try:
                os.system('paplay /usr/share/sounds/freedesktop/stereo/alarm-clock-elapsed.oga 2>/dev/null || aplay /usr/share/sounds/alsa/Front_Center.wav 2>/dev/null')
            except Exception:
                pass
        
        # Fallback: print bell character
        print('\a', end='', flush=True)
    
    def _default_notification(self, alarm_time: str) -> None:
        """Default notification for CLI mode.
        
        Args:
            alarm_time: The time of the triggered alarm.
        """
        print(f"\n{'='*40}")
        print(f"  ALARM! Time: {alarm_time}")
        print(f"{'='*40}\n")
    
    def get_upcoming_alarms(self) -> List[Dict[str, Any]]:
        """Get all upcoming (not yet triggered today) enabled alarms.
        
        Returns:
            List of upcoming alarm dictionaries.
        """
        current_time = datetime.now().strftime('%H:%M')
        all_alarms = self.store.get_all()
        upcoming = []
        
        for alarm in all_alarms:
            if alarm.get('enabled', True) and alarm['time'] > current_time:
                upcoming.append(alarm)
        
        return sorted(upcoming, key=lambda x: x['time'])
