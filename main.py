import tkinter as tk
from threading import Timer
import time

class Chronometer:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Chronometer")
        self.root.geometry("600x300")

        self.hourly_rate = tk.StringVar()
        self.hourly_rate_label = tk.Label(self.root, text="Enter hourly rate:")
        self.hourly_rate_label.pack()
        self.hourly_rate_entry = tk.Entry(self.root, textvariable=self.hourly_rate)
        self.hourly_rate_entry.pack()
        self.set_hourly_rate_button = tk.Button(self.root, text="Set hourly rate", command=self.set_hourly_rate)
        self.set_hourly_rate_button.pack()

    def set_hourly_rate(self):
        try:
            self.hourly_rate_value = float(self.hourly_rate.get())
            self.hourly_rate_label.pack_forget()
            self.hourly_rate_entry.pack_forget()
            self.set_hourly_rate_button.pack_forget()
            self.create_chronometer()
        except ValueError:
            self.hourly_rate_label.config(text="Invalid hourly rate. Please enter a number.")

    def create_chronometer(self):
        self.pay_label = tk.Label(self.root, text="Total pay: $0.00", font=("Helvetica", 24))
        self.pay_label.place(relx=0.5, rely=0.2, anchor=tk.CENTER)

        self.label = tk.Label(self.root, text="00:00:00", font=("Helvetica", 48))
        self.label.place(relx=0.5, rely=0.4, anchor=tk.CENTER)

        self.seconds = 0
        self.running = False
        self.paused = False

        self.start_button = tk.Button(self.root, text="Start", command=self.start)
        self.start_button.place(relx=0.3, rely=0.7, anchor=tk.CENTER)

        self.pause_button = tk.Button(self.root, text="Pause", command=self.pause)
        self.pause_button.place(relx=0.7, rely=0.7, anchor=tk.CENTER)

    def start(self):
        if not self.running:
            self.running = True
            self.start_button.config(text="Reset", command=self.reset)
            # Create a Timer to increment the time every second
            self.timer = Timer(1, self.increment_time)
            self.timer.start()

    def pause(self):
        if self.running:
            self.paused = True
            self.pause_button.config(text="Resume", command=self.resume)
        else:
            self.paused = False
            self.pause_button.config(text="Pause", command=self.pause)

    def resume(self):
        self.paused = False
        self.pause_button.config(text="Pause", command=self.pause)

    def reset(self):
        self.running = False
        self.paused = False
        self.seconds = 0
        self.label.config(text="00:00:00")
        self.pay_label.config(text="Total pay: $0.00")
        self.start_button.config(text="Start", command=self.start)
        # Cancel the Timer
        self.timer.cancel()

    def increment_time(self):
        if self.running and not self.paused:
            self.seconds += 1
            self.label.config(text=time.strftime("%H:%M:%S", time.gmtime(self.seconds)))
            self.pay_label.config(text=f"Total pay: ${self.hourly_rate_value * self.seconds / 3600:.2f}")
            # Create a new Timer to increment the time every second
            self.timer = Timer(1, self.increment_time)
            self.timer.start()

if __name__ == "__main__":
    chronometer = Chronometer()
    chronometer.root.mainloop()
