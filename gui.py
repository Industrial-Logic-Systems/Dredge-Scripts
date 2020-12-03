from tkinter import Tk, Label, Button
import threading
import logging
import datetime

import Dredge_Data_Log
import backup


def log_loop():
    logging.debug("Loop Starting")
    my_label.config(text="Log Loop Running")
    while True:
        Dredge_Data_Log.log()
    my_label.config(text="Log Loop Not Running")


def manual_backup():
    filename = datetime.datetime.today().strftime("%Y-%m-%d")
    backup.backup_files(filename)


root = Tk()

root.title("ILS Dredge Data Logging")
root.geometry("400x400")

my_label = Label(root, text="Hello!")
my_label.pack()

my_button = Button(root, text='Manual Backup', command=manual_backup)
my_button.pack()

logging.debug("Starting Thread")
threading.Thread(target=log_loop).start()

logging.debug("Starting GUI main loop")
root.mainloop()