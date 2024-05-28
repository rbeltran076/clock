import tkinter as tk
from threading import Timer
import time
import json
import os

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

        self.date = tk.StringVar()
        self.date_label = tk.Label(self.root, text="Enter date (YYYY-MM-DD):")
        self.date_label.pack()
        self.date_entry = tk.Entry(self.root, textvariable=self.date)
        self.date_entry.pack()

        self.title = tk.StringVar()
        self.title_label = tk.Label(self.root, text="Enter title (optional):")
        self.title_label.pack()
        self.title_entry = tk.Entry(self.root, textvariable=self.title)
        self.title_entry.pack()

        self.set_hourly_rate_button = tk.Button(self.root, text="Set hourly rate", command=self.set_hourly_rate)
        self.set_hourly_rate_button.pack()

        self.see_saves_button = tk.Button(self.root, text="See saves", command=self.see_saves)
        self.see_saves_button.pack()

    def set_hourly_rate(self):
        try:
            self.hourly_rate_value = float(self.hourly_rate.get())
            self.date_value = self.date.get()
            self.title_value = self.title.get()
            self.hourly_rate_label.pack_forget()
            self.hourly_rate_entry.pack_forget()
            self.date_label.pack_forget()
            self.date_entry.pack_forget()
            self.title_label.pack_forget()
            self.title_entry.pack_forget()
            self.set_hourly_rate_button.pack_forget()
            self.see_saves_button.pack_forget()
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

        self.save_button = tk.Button(self.root, text="Save", command=self.save)
        self.save_button.place(relx=0.5, rely=0.8, anchor=tk.CENTER)

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
            self.timer.cancel()  # Cancel the Timer
            self.pause_button.config(text="Resume", command=self.resume)

    def resume(self):
        self.paused = False
        self.timer = Timer(1, self.increment_time)  # Create a new Timer
        self.timer.start()
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

    def save(self):
        data = {
            'hourly_rate': self.hourly_rate_value,
            'time': self.label.cget('text'),
            'pay': float(self.pay_label.cget('text').split('$')[1])
        }
        
        if os.path.exists('saves.json'):
            with open('saves.json', 'r') as file:
                saves = json.load(file)
                if self.date_value in saves:
                    if self.title_value in saves[self.date_value]:
                        saves[self.date_value][self.title_value].append(data)
                    else:
                        saves[self.date_value][self.title_value] = [data]
                else:
                    saves[self.date_value] = {self.title_value: [data]}
            with open('saves.json', 'w') as file:
                json.dump(saves, file, indent=4)
        else:
            with open('saves.json', 'w') as file:
                json.dump({self.date_value: {self.title_value: [data]}}, file, indent=4)

    def see_saves(self):
        self.hourly_rate_label.pack_forget()
        self.hourly_rate_entry.pack_forget()
        self.date_label.pack_forget()
        self.date_entry.pack_forget()
        self.title_label.pack_forget()
        self.title_entry.pack_forget()
        self.set_hourly_rate_button.pack_forget()
        self.see_saves_button.pack_forget()

        if os.path.exists('saves.json'):
            with open('saves.json', 'r') as file:
                saves = json.load(file)
                text = tk.Text(self.root)
                text.pack()
                text.insert(tk.END, json.dumps(saves, indent=4))

if __name__ == "__main__":
    chronometer = Chronometer()
    chronometer.root.mainloop()