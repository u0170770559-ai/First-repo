"""Unit tests for alarm clock modules."""
import json
import os
import tempfile
import time
import threading
from datetime import datetime
import pytest

from alarm_store import AlarmStore
from scheduler import AlarmScheduler


class TestAlarmStore:
    """Tests for the AlarmStore class."""
    
    def test_init_creates_empty_store(self):
        """Test that a new store starts empty."""
        with tempfile.NamedTemporaryFile(delete=False, suffix='.json') as f:
            filepath = f.name
        
        try:
            store = AlarmStore(filepath)
            assert store.get_all() == []
        finally:
            os.unlink(filepath)
    
    def test_add_valid_alarm(self):
        """Test adding a valid alarm."""
        with tempfile.NamedTemporaryFile(delete=False, suffix='.json') as f:
            filepath = f.name
        
        try:
            store = AlarmStore(filepath)
            alarm = store.add("08:30")
            
            assert alarm is not None
            assert alarm['time'] == "08:30"
            assert alarm['enabled'] is True
            assert 'id' in alarm
            assert len(store.get_all()) == 1
        finally:
            os.unlink(filepath)
    
    def test_add_invalid_alarm(self):
        """Test adding an invalid alarm time."""
        with tempfile.NamedTemporaryFile(delete=False, suffix='.json') as f:
            filepath = f.name
        
        try:
            store = AlarmStore(filepath)
            
            assert store.add("25:00") is None  # Invalid hour
            assert store.add("12:60") is None  # Invalid minute
            assert store.add("not-a-time") is None  # Invalid format
            assert store.add("8:30") is None  # Missing leading zero
            assert len(store.get_all()) == 0
        finally:
            os.unlink(filepath)
    
    def test_delete_alarm(self):
        """Test deleting an alarm."""
        with tempfile.NamedTemporaryFile(delete=False, suffix='.json') as f:
            filepath = f.name
        
        try:
            store = AlarmStore(filepath)
            alarm = store.add("09:00")
            alarm_id = alarm['id']
            
            assert store.delete(alarm_id) is True
            assert len(store.get_all()) == 0
            assert store.delete(alarm_id) is False  # Already deleted
        finally:
            os.unlink(filepath)
    
    def test_delete_by_time(self):
        """Test deleting alarms by time."""
        with tempfile.NamedTemporaryFile(delete=False, suffix='.json') as f:
            filepath = f.name
        
        try:
            store = AlarmStore(filepath)
            store.add("10:00")
            store.add("10:00")
            store.add("11:00")
            
            assert store.delete_by_time("10:00") == 2
            assert len(store.get_all()) == 1
            assert store.get_all()[0]['time'] == "11:00"
        finally:
            os.unlink(filepath)
    
    def test_persistence(self):
        """Test that alarms persist to disk."""
        with tempfile.NamedTemporaryFile(delete=False, suffix='.json') as f:
            filepath = f.name
        
        try:
            # Create store and add alarm
            store1 = AlarmStore(filepath)
            store1.add("14:30")
            
            # Create new store instance with same file
            store2 = AlarmStore(filepath)
            alarms = store2.get_all()
            
            assert len(alarms) == 1
            assert alarms[0]['time'] == "14:30"
        finally:
            os.unlink(filepath)
    
    def test_validate_time(self):
        """Test time validation."""
        assert AlarmStore._validate_time("00:00") is True
        assert AlarmStore._validate_time("23:59") is True
        assert AlarmStore._validate_time("12:30") is True
        assert AlarmStore._validate_time("24:00") is False
        assert AlarmStore._validate_time("12:61") is False
        assert AlarmStore._validate_time("abc") is False


class TestAlarmScheduler:
    """Tests for the AlarmScheduler class."""
    
    def test_scheduler_initialization(self):
        """Test scheduler initialization."""
        with tempfile.NamedTemporaryFile(delete=False, suffix='.json') as f:
            filepath = f.name
        
        try:
            store = AlarmStore(filepath)
            scheduler = AlarmScheduler(store)
            
            assert scheduler.store == store
            assert scheduler._running is False
        finally:
            os.unlink(filepath)
    
    def test_scheduler_start_stop(self):
        """Test starting and stopping the scheduler."""
        with tempfile.NamedTemporaryFile(delete=False, suffix='.json') as f:
            filepath = f.name
        
        try:
            store = AlarmStore(filepath)
            scheduler = AlarmScheduler(store)
            
            scheduler.start()
            assert scheduler._running is True
            assert scheduler._thread is not None
            assert scheduler._thread.is_alive()
            
            scheduler.stop()
            assert scheduler._running is False
        finally:
            os.unlink(filepath)
    
    def test_get_upcoming_alarms(self):
        """Test getting upcoming alarms."""
        with tempfile.NamedTemporaryFile(delete=False, suffix='.json') as f:
            filepath = f.name
        
        try:
            store = AlarmStore(filepath)
            scheduler = AlarmScheduler(store)
            
            now = datetime.now()
            past_time = f"{(now.hour - 1) % 24:02d}:00"
            future_time = f"{(now.hour + 1) % 24:02d}:00"
            
            store.add(past_time)
            store.add(future_time)
            
            upcoming = scheduler.get_upcoming_alarms()
            
            # Should only include future alarms
            assert len(upcoming) == 1
            assert upcoming[0]['time'] == future_time
        finally:
            os.unlink(filepath)
    
    def test_trigger_callback(self):
        """Test that trigger callback is called."""
        with tempfile.NamedTemporaryFile(delete=False, suffix='.json') as f:
            filepath = f.name
        
        try:
            store = AlarmStore(filepath)
            triggered = []
            
            def on_trigger(time_str):
                triggered.append(time_str)
            
            scheduler = AlarmScheduler(store, on_trigger=on_trigger)
            scheduler._trigger_alarm("12:00")
            
            assert len(triggered) == 1
            assert triggered[0] == "12:00"
        finally:
            os.unlink(filepath)


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
