import config

import tkinter as tk  # from tkinter import Toplevel, Listbox, END, PhotoImage
import tkinter.ttk as ttk  # from tkinter.ttk import Label, Button, Entry
from ttkthemes import ThemedTk
import threading
import logging
import datetime
import os  # os.path.dirname(__file__)+"\\resources\\ILS-logo.png"
import time

import Dredge_Data_Log
import backup


def log_loop():
    """ Will start a while loop that calls the log function """
    logging.info("Starting Log")
    my_label.config(text="Log Loop Running")
    while True:
        result = Dredge_Data_Log.log()
        if result:
            my_label.config(text="Log Loop Running")
        else:
            my_label.config(text="Loging Failed retrying in 2 seconds...")
            time.sleep(2)


def manual_backup():
    """ Will start a manual backup """
    logging.debug("Manual Backup Started")
    filename = datetime.datetime.today().strftime("%Y-%m-%d")
    threading.Thread(target=backup.backup_files, args=(filename,)).start()
    # backup.backup_files(filename)


# Creating the window
root = ThemedTk()
root.title("ILS")
# root.geometry("300x150")
root.set_theme("black", toplevel=True, themebg=True)
root.iconbitmap(config.proj_dir + "/resources/ILS-logo.ico")


def change_config():
    """Create Window for changing config"""

    def save_config():
        """Save Any changes made to config"""
        logging.info("Saving Config")
        config.port_name = port_config.get()
        config.json_path = json_config.get()
        config.csv_path = csv_config.get()
        config.remote_server = remote_config.get()
        config.remote_server_path = dir_config.get()
        config.enable_email = email_checkbox.instate(["selected"])
        config.enable_ssh = ssh_checkbox.instate(["selected"])

        config.email_list = []
        email_box_ls = email_box.get(0, email_box.size())
        for item in email_box_ls:
            config.email_list.append(item)

        config.save_config()
        logging.info("Config Saved")

    def rm_sel():
        """Remove selected email from listbox"""
        email_box.delete(email_box.curselection())

    def add():
        """Add an email to listbox"""
        email_box.insert(tk.END, new_email.get())

    config_win = tk.Toplevel(root)
    config_win.title("Config")
    config_win.iconbitmap(os.path.dirname(__file__) + "/resources/ILS-logo.ico")
    # config_win.geometry("800x400")

    ttk.Label(config_win, text="Config Window").grid(
        row=1, column=1, padx=10, pady=10, columnspan=6
    )

    # Port
    ttk.Label(config_win, text="Serial Port Name:").grid(
        row=2, column=1, padx=10, pady=10
    )
    port_config = ttk.Entry(config_win, width=40)
    port_config.insert(0, config.port_name)
    port_config.grid(row=2, column=2, padx=10, pady=10, columnspan=2)

    # JSON
    ttk.Label(config_win, text="JSON Folder Name:").grid(
        row=3, column=1, padx=10, pady=10
    )
    json_config = ttk.Entry(config_win, width=40)
    json_config.insert(0, config.json_path)
    json_config.grid(row=3, column=2, padx=10, pady=10, columnspan=2)

    # CSV
    ttk.Label(config_win, text="CSV Folder Name:").grid(
        row=4, column=1, padx=10, pady=10
    )
    csv_config = ttk.Entry(config_win, width=40)
    csv_config.insert(0, config.csv_path)
    csv_config.grid(row=4, column=2, padx=10, pady=10, columnspan=2)

    # Remote IP
    ttk.Label(config_win, text="Remote IP:").grid(row=5, column=1, padx=10, pady=10)
    remote_config = ttk.Entry(config_win, width=40)
    remote_config.insert(0, config.remote_server)
    remote_config.grid(row=5, column=2, padx=10, pady=10, columnspan=2)

    # Remote DIR
    ttk.Label(config_win, text="Remote Dir:").grid(row=6, column=1, padx=10, pady=10)
    dir_config = ttk.Entry(config_win, width=40)
    dir_config.insert(0, config.remote_server_path)
    dir_config.grid(row=6, column=2, padx=10, pady=10, columnspan=2)

    # Emails
    ttk.Label(config_win, text="Email List:").grid(
        row=2, column=4, padx=10, pady=10, sticky="nw"
    )
    ttk.Button(config_win, text="Remove Selected", command=rm_sel).grid(
        row=3, column=4, padx=10, pady=10, sticky="nw"
    )
    email_box = tk.Listbox(config_win, width=40)
    for email in config.email_list:
        email_box.insert(tk.END, email)
    email_box.grid(row=2, column=5, padx=10, pady=10, columnspan=2, rowspan=4)
    new_email = ttk.Entry(config_win, width=40)
    new_email.grid(row=6, column=4, padx=10, pady=10, columnspan=2)
    ttk.Button(config_win, text="Add Email", command=add).grid(
        row=6, column=6, padx=10, pady=10
    )

    # Enable Email
    email_checkbox = ttk.Checkbutton(config_win, text="Enable Email Backup")
    email_checkbox.grid(row=7, column=1, padx=10, pady=10)
    if config.enable_email:
        email_checkbox.state(["selected"])
    else:
        email_checkbox.state(["!selected"])

    # Enable SSH
    ssh_checkbox = ttk.Checkbutton(config_win, text="Enable SSH Backup")
    ssh_checkbox.grid(row=7, column=2, padx=10, pady=10)
    if config.enable_ssh:
        ssh_checkbox.state(["selected"])
    else:
        ssh_checkbox.state(["!selected"])

    # Save Button
    save = ttk.Button(config_win, text="Save Config", command=save_config)
    save.grid(row=7, column=6, padx=10, pady=10)


ils_logo = tk.PhotoImage(file=config.proj_dir + "/resources/ILS-logo.png")
ttk.Label(root, image=ils_logo).grid(row=0, column=0, padx=10, pady=10)
ttk.Label(root, text="ILS Dredge Data Logger").grid(
    row=0, column=1, columnspan=2, padx=10, pady=10
)

# Label that tell's the use the loop is running
my_label = ttk.Label(root, text="Logging will start soon...")
my_label.grid(row=1, column=0, padx=10, pady=10, columnspan=3)
# Button to start a manual backup
ttk.Button(root, text="Manual Backup", command=manual_backup).grid(
    row=2, column=0, padx=10, pady=10, columnspan=2
)
# Button to access the config menu
ttk.Button(root, text="Config", command=change_config).grid(
    row=2, column=2, padx=10, pady=10, columnspan=2
)


# Start the logging loop in its own thread
logging.debug("Starting Thread")
threading.Thread(target=log_loop, daemon=True).start()


def on_closing():
    quit()


# Start the GUI
logging.info("Starting GUI")
root.protocol("WM_DELETE_WINDOW", on_closing)
root.mainloop()
