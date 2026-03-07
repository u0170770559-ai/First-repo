"""GUI module for the alarm clock using Tkinter."""
import tkinter as tk
from tkinter import ttk, messagebox
import threading
from datetime import datetime
from typing import Optional
from alarm_store import AlarmStore
from scheduler import AlarmScheduler


class AlarmClockGUI:
    """Tkinter-based GUI for the alarm clock."""
    
    def __init__(self, root: Optional[tk.Tk] = None) -> None:
        """Initialize the GUI.
        
        Args:
            root: Optional Tk root window. Creates one if not provided.
        """
        self.root = root or tk.Tk()
        self.root.title("Alarm Clock")
        self.root.geometry("400x500")
        self.root.resizable(False, False)
        
        self.store = AlarmStore()
        self.scheduler = AlarmScheduler(self.store, on_trigger=self._on_alarm_trigger)
        
        self._setup_ui()
        self._start_scheduler()
        self._update_time()
        self._refresh_alarm_list()
    
    def _setup_ui(self) -> None:
        """Set up the user interface components."""
        # Main frame with padding
        main_frame = ttk.Frame(self.root, padding="20")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Current time display
        ttk.Label(main_frame, text="Current Time", font=('Helvetica', 12)).grid(
            row=0, column=0, columnspan=2, pady=(0, 5)
        )
        self.time_label = ttk.Label(
            main_frame, text="", font=('Helvetica', 32, 'bold')
        )
        self.time_label.grid(row=1, column=0, columnspan=2, pady=(0, 20))
        
        # Separator
        ttk.Separator(main_frame, orient='horizontal').grid(
            row=2, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=10
        )
        
        # Add alarm section
        ttk.Label(main_frame, text="Add Alarm (HH:MM)", font=('Helvetica', 11)).grid(
            row=3, column=0, columnspan=2, pady=(10, 5)
        )
        
        input_frame = ttk.Frame(main_frame)
        input_frame.grid(row=4, column=0, columnspan=2, pady=5)
        
        self.hour_var = tk.StringVar()
        self.minute_var = tk.StringVar()
        
        # Hour input
        ttk.Label(input_frame, text="Hour:").pack(side=tk.LEFT, padx=5)
        hour_spin = ttk.Spinbox(
            input_frame, from_=0, to=23, width=5, format='%02.0f',
            textvariable=self.hour_var
        )
        hour_spin.pack(side=tk.LEFT)
        hour_spin.set('00')
        
        ttk.Label(input_frame, text=":").pack(side=tk.LEFT)
        
        # Minute input
        ttk.Label(input_frame, text="Min:").pack(side=tk.LEFT, padx=5)
        min_spin = ttk.Spinbox(
            input_frame, from_=0, to=59, width=5, format='%02.0f',
            textvariable=self.minute_var
        )
        min_spin.pack(side=tk.LEFT)
        min_spin.set('00')
        
        add_btn = ttk.Button(main_frame, text="Add Alarm", command=self._add_alarm)
        add_btn.grid(row=5, column=0, columnspan=2, pady=10)
        
        # Separator
        ttk.Separator(main_frame, orient='horizontal').grid(
            row=6, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=10
        )
        
        # Alarm list section
        ttk.Label(main_frame, text="Upcoming Alarms", font=('Helvetica', 11)).grid(
            row=7, column=0, columnspan=2, pady=(10, 5)
        )
        
        # Listbox with scrollbar for alarms
        list_frame = ttk.Frame(main_frame)
        list_frame.grid(row=8, column=0, columnspan=2, sticky=(tk.W, tk.E, tk.N, tk.S), pady=5)
        
        self.alarm_listbox = tk.Listbox(
            list_frame, height=8, font=('Helvetica', 10)
        )
        self.alarm_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        scrollbar = ttk.Scrollbar(list_frame, orient=tk.VERTICAL)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.alarm_listbox.config(yscrollcommand=scrollbar.set)
        scrollbar.config(command=self.alarm_listbox.yview)
        
        # Delete button
        delete_btn = ttk.Button(
            main_frame, text="Delete Selected", command=self._delete_selected
        )
        delete_btn.grid(row=9, column=0, columnspan=2, pady=10)
        
        # Configure grid weights
        main_frame.columnconfigure(0, weight=1)
        main_frame.rowconfigure(8, weight=1)
    
    def _start_scheduler(self) -> None:
        """Start the alarm scheduler."""
        self.scheduler.start()
    
    def _update_time(self) -> None:
        """Update the current time display."""
        current_time = datetime.now().strftime('%H:%M:%S')
        self.time_label.config(text=current_time)
        self.root.after(1000, self._update_time)
    
    def _refresh_alarm_list(self) -> None:
        """Refresh the alarm list display."""
        self.alarm_listbox.delete(0, tk.END)
        alarms = self.scheduler.get_upcoming_alarms()
        
        for alarm in alarms:
            display_text = f"{alarm['time']} (ID: {alarm['id'][:6]})"
            self.alarm_listbox.insert(tk.END, display_text)
        
        # Refresh every 10 seconds to update upcoming status
        self.root.after(10000, self._refresh_alarm_list)
    
    def _add_alarm(self) -> None:
        """Add a new alarm from the input fields."""
        try:
            hour = int(self.hour_var.get())
            minute = int(self.minute_var.get())
            
            if not (0 <= hour <= 23 and 0 <= minute <= 59):
                raise ValueError("Invalid time range")
            
            time_str = f"{hour:02d}:{minute:02d}"
            alarm = self.store.add(time_str)
            
            if alarm:
                messagebox.showinfo("Success", f"Alarm added for {time_str}")
                self._refresh_alarm_list()
            else:
                messagebox.showerror("Error", "Failed to add alarm")
        except ValueError:
            messagebox.showerror("Error", "Please enter valid hour (0-23) and minute (0-59)")
    
    def _delete_selected(self) -> None:
        """Delete the selected alarm from the list."""
        selection = self.alarm_listbox.curselection()
        if not selection:
            messagebox.showwarning("Warning", "Please select an alarm to delete")
            return
        
        index = selection[0]
        alarms = self.scheduler.get_upcoming_alarms()
        
        if index < len(alarms):
            alarm_id = alarms[index]['id']
            if self.store.delete(alarm_id):
                messagebox.showinfo("Success", "Alarm deleted")
                self._refresh_alarm_list()
            else:
                messagebox.showerror("Error", "Failed to delete alarm")
    
    def _on_alarm_trigger(self, alarm_time: str) -> None:
        """Handle alarm trigger - show popup notification.
        
        Args:
            alarm_time: The time of the triggered alarm.
        """
        # Use after() to ensure messagebox runs on main thread
        self.root.after(0, lambda: self._show_alarm_popup(alarm_time))
    
    def _show_alarm_popup(self, alarm_time: str) -> None:
        """Show alarm popup notification.
        
        Args:
            alarm_time: The time of the triggered alarm.
        """
        messagebox.showinfo(
            "ALARM!",
            f"Alarm time reached: {alarm_time}",
            icon='warning'
        )
        self._refresh_alarm_list()
    
    def run(self) -> None:
        """Start the GUI main loop."""
        self.root.mainloop()
        self.scheduler.stop()


def main() -> None:
    """Main entry point for GUI."""
    app = AlarmClockGUI()
    app.run()


if __name__ == '__main__':
    main()
