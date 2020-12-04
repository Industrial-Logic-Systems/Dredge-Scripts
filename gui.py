from tkinter import Toplevel, Listbox, END, PhotoImage
from tkinter.ttk import Label, Button, Entry
from ttkthemes import ThemedTk
import threading
import logging
import datetime

import Dredge_Data_Log
import backup
import config


def log_loop():
    logging.debug("Loop Starting")
    my_label.config(text="Log Loop Running")
    while True:
        Dredge_Data_Log.log()
    my_label.config(text="Log Loop Not Running")


def manual_backup():
    filename = datetime.datetime.today().strftime("%Y-%m-%d")
    backup.backup_files(filename)


root = ThemedTk()
root.title("ILS Dredge Data Logging")
# root.geometry("400x400")
root.set_theme("black", toplevel=True, themebg=True)
root.iconbitmap("resources/ILS-logo.ico")


def change_config():
    def save_config():
        config.port_name = port_config.get()
        config.json_path = json_config.get()
        config.csv_path = csv_config.get()
        config.remote_server = remote_config.get()
        config.remote_server_path = dir_config.get()

        config.email_list = []
        email_box_ls = email_box.get(0, email_box.size())
        for item in email_box_ls:
            config.email_list.append(item)

        config.save_config()

    def rm_sel():
        email_box.delete(email_box.curselection())

    def add():
        email_box.insert(END, new_email.get())

    config_win = Toplevel(root)
    config_win.title("Config")
    # config_win.geometry("800x400")

    Label(config_win, text="Config Window").grid(
        row=1, column=1, padx=10, pady=10, columnspan=6
    )

    # Port
    Label(config_win, text="Serial Port Name:").grid(row=2, column=1, padx=10, pady=10)
    port_config = Entry(config_win, width=40)
    port_config.insert(0, config.port_name)
    port_config.grid(row=2, column=2, padx=10, pady=10, columnspan=2)

    # JSON
    Label(config_win, text="JSON Folder Name:").grid(row=3, column=1, padx=10, pady=10)
    json_config = Entry(config_win, width=40)
    json_config.insert(0, config.json_path)
    json_config.grid(row=3, column=2, padx=10, pady=10, columnspan=2)

    # CSV
    Label(config_win, text="CSV Folder Name:").grid(row=4, column=1, padx=10, pady=10)
    csv_config = Entry(config_win, width=40)
    csv_config.insert(0, config.csv_path)
    csv_config.grid(row=4, column=2, padx=10, pady=10, columnspan=2)

    # Remote IP
    Label(config_win, text="Remote IP:").grid(row=5, column=1, padx=10, pady=10)
    remote_config = Entry(config_win, width=40)
    remote_config.insert(0, config.remote_server)
    remote_config.grid(row=5, column=2, padx=10, pady=10, columnspan=2)

    # Remote DIR
    Label(config_win, text="Remote Dir:").grid(row=6, column=1, padx=10, pady=10)
    dir_config = Entry(config_win, width=40)
    dir_config.insert(0, config.remote_server_path)
    dir_config.grid(row=6, column=2, padx=10, pady=10, columnspan=2)

    # Emails
    Label(config_win, text="Email List:").grid(
        row=2, column=4, padx=10, pady=10, sticky="nw"
    )
    Button(config_win, text="Remove Selected", command=rm_sel).grid(
        row=3, column=4, padx=10, pady=10, sticky="nw"
    )
    email_box = Listbox(config_win, width=40)
    for email in config.email_list:
        email_box.insert(END, email)
    email_box.grid(row=2, column=5, padx=10, pady=10, columnspan=2, rowspan=4)
    new_email = Entry(config_win, width=40)
    new_email.grid(row=6, column=4, padx=10, pady=10, columnspan=2)
    Button(config_win, text="Add Email", command=add).grid(
        row=6, column=6, padx=10, pady=10
    )

    # Save Button
    save = Button(config_win, text="Save Config", command=save_config)
    save.grid(row=7, column=6, padx=10, pady=10)


ils_logo = PhotoImage(file="resources/ILS-logo.png")
Label(root, image=ils_logo).grid(row=0, column=1, sticky="w", padx=10, pady=10)
Label(root, text="ILS Dredge Data Logger").grid(
    row=0, column=1, columnspan=2, padx=10, pady=10, sticky="e"
)

# Label that tell's the use the loop is running
my_label = Label(root, text="Hello!")
my_label.grid(row=1, column=1, padx=10, pady=10, columnspan=2)
# Button to start a manual backup
Button(root, text="Manual Backup", command=manual_backup).grid(
    row=2, column=1, padx=10, pady=10
)
# Button to access the config menu
Button(root, text="Config", command=change_config).grid(
    row=2, column=2, padx=10, pady=10
)

# Start the logging loop in its own thread
logging.debug("Starting Thread")
threading.Thread(target=log_loop).start()

# Start the GUI
logging.debug("Starting GUI main loop")
root.mainloop()