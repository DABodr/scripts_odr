import subprocess
import tkinter as tk
from tkinter import ttk, messagebox
import threading
import queue
import signal
import os

class DABApp:
    def __init__(self, root):
        self.root = root
        self.root.title("DAB Command Line Interface")
        self.frequency = tk.StringVar(value="9A")
        self.running = False
        self.process = None
        self.queue = queue.Queue()

        self.snr_line_index = None  # Variable to track the line index of SNR output

        self.create_widgets()

    def create_widgets(self):
        ttk.Label(self.root, text="Choisir la fréquence:").grid(column=0, row=0, padx=10, pady=10)

        self.freq_combobox = ttk.Combobox(self.root, textvariable=self.frequency)
        self.freq_combobox['values'] = ["5A", "5B", "5C", "5D", "6A", "6B", "6C", "6D",
                                        "7A", "7B", "7C", "7D", "8A", "8B", "8C", "8D",
                                        "9A", "9B", "9C", "9D", "10A", "10B", "10C", "10D",
                                        "11A", "11B", "11C", "11D", "12A", "12B", "12C", "12D",
                                        "13A", "13B", "13C", "13D", "13E", "13F"]
        self.freq_combobox.grid(column=1, row=0, padx=10, pady=10)

        self.dablin_button = ttk.Button(self.root, text="Dablin", command=self.run_dablin)
        self.dablin_button.grid(column=2, row=0, padx=10, pady=10)

        self.start_button = ttk.Button(self.root, text="Démarrer", command=self.start_script)
        self.start_button.grid(column=0, row=1, padx=10, pady=10)

        self.stop_button = ttk.Button(self.root, text="Arrêter", command=self.stop_script)
        self.stop_button.grid(column=1, row=1, padx=10, pady=10)

        self.status_button = ttk.Button(self.root, text="Statut", command=self.status_script)
        self.status_button.grid(column=2, row=1, padx=10, pady=10)

        self.log_text = tk.Text(self.root, state='disabled', width=80, height=20)
        self.log_text.grid(column=0, row=2, columnspan=3, padx=10, pady=10)

    def read_output(self, pipe):
        for line in iter(pipe.readline, ''):
            if line.strip().isdigit() or self.is_unwanted_line(line):
                continue  # Skip lines that are just numbers or unwanted
            if "estimated snr" in line and "fibquality" in line:
                self.queue.put(("snr", line))
            else:
                self.queue.put(("log", line))
        pipe.close()

    def is_unwanted_line(self, line):
        # Define criteria for unwanted lines
        unwanted_patterns = ["estimated snr"]
        return any(pattern in line for pattern in unwanted_patterns) and not line.startswith("estimated snr")

    def run_command(self):
        command = f"eti-cmdline-rtlsdr -D 5 -C {self.frequency.get()} -Q | /home/$USER/dab/eti-tools/eti2zmq -v -a -d -o zmq+tcp://*:18081"
        self.queue.put(("log", f"Démarrage de la commande: {command}\n"))
        self.process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, preexec_fn=os.setsid)

        threading.Thread(target=self.read_output, args=(self.process.stdout,)).start()
        threading.Thread(target=self.read_output, args=(self.process.stderr,)).start()

        self.process.wait()
        if not self.running:
            self.queue.put(("log", "La commande a été interrompue.\n"))

    def start_script(self):
        if not self.running:
            self.running = True
            threading.Thread(target=self.run_command).start()
            self.update_log()
            messagebox.showinfo("Info", f"Script démarré avec la fréquence: {self.frequency.get()}")
        else:
            messagebox.showwarning("Attention", "Le script est déjà en cours d'exécution.")

    def stop_script(self):
        if self.running:
            self.running = False
            if self.process:
                os.killpg(os.getpgid(self.process.pid), signal.SIGTERM)
            messagebox.showinfo("Info", "Arrêt du script.")
        else:
            messagebox.showwarning("Attention", "Le script n'est pas en cours d'exécution.")

    def status_script(self):
        if self.running:
            messagebox.showinfo("Info", f"Le script est en cours d'exécution avec la fréquence: {self.frequency.get()}")
        else:
            messagebox.showinfo("Info", "Le script est arrêté.")

    def update_log(self):
        while not self.queue.empty():
            message_type, line = self.queue.get()
            self.log_text.config(state='normal')
            if message_type == "snr":
                if self.snr_line_index is not None:
                    # Update the existing SNR line
                    self.log_text.delete(self.snr_line_index, f"{self.snr_line_index} lineend")
                    self.log_text.insert(self.snr_line_index, line)
                else:
                    # Insert the SNR line for the first time
                    self.log_text.insert('end', line)
                    self.snr_line_index = self.log_text.index('end-1c')
            else:
                self.log_text.insert('end', line)
            self.log_text.config(state='disabled')
            self.log_text.yview('end')
        if self.running:
            self.root.after(100, self.update_log)

    def run_dablin(self):
        command = f"/home/$USER/dab/mmbtools-aux/zmqtest/zmq-sub/zmq-sub localhost 18081 | /home/$USER/dab/dablin/build/src/dablin_gtk"
        subprocess.Popen(command, shell=True, preexec_fn=os.setsid)

if __name__ == "__main__":
    root = tk.Tk()
    app = DABApp(root)
    root.mainloop()
