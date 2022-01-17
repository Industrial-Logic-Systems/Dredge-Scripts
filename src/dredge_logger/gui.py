from dredge_logger.config import config

from ttkthemes import ThemedTk
import datetime
import logging
import threading
import time
import tkinter as tk
import tkinter.ttk as ttk

from dredge_logger import backup
from dredge_logger import Log

_logger = logging.getLogger(__name__)


class LogGUI(ThemedTk):
    def __init__(self, *args, **kwargs):
        ThemedTk.__init__(self, *args, **kwargs)

        # Set Window properties
        self.winfo_toplevel().title("ILS Logger")
        self.iconbitmap(config._proj_dir + "/resources/ILS-logo.ico")
        self.set_theme("black", toplevel=True, themebg=True)

        # Create Container that holds all frames
        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)

        # Create all the frames
        self.frames = {}
        for F in (StartPage, Config):
            page_name = F.__name__
            frame = F(parent=container, controller=self)
            self.frames[page_name] = frame

            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame("StartPage")
        # self.show_frame("Config")

    def show_frame(self, page_name):
        """Set the current frame"""
        frame = self.frames[page_name]
        frame.tkraise()

    def manual_backup(self):
        """Manually Run a Backup"""
        _logger.debug("Manual Backup Started")
        filename = datetime.datetime.today().strftime("%Y-%m-%d")
        threading.Thread(target=backup.backup_files, args=(filename,)).start()

    def log_loop(self):
        """Will start a while loop that calls the log function"""
        _logger.info("Starting Log")
        self.frames["StartPage"].log_status.config(text="Log Loop Running")
        while True:
            result = Log.log()
            if result[0]:
                self.frames["StartPage"].log_status.config(text="Log Loop Running")
                self.frames["StartPage"].json_preview.config(text=result[1])
            else:
                self.frames["StartPage"].log_status.config(text="Loging Failed retrying in 2 seconds...")
                time.sleep(2)


class StartPage(ttk.Frame):
    def __init__(self, parent, controller):
        ttk.Frame.__init__(self, parent)
        self.controller = controller

        # Create Frames
        self.top = ttk.Frame(self)
        self.middle = ttk.Frame(self)
        self.bottom = ttk.Frame(self)

        # Create widgets for frame
        self.ils_logo = tk.PhotoImage(file=config._proj_dir + "\\resources\\ILS-logo.png")
        self.image1 = ttk.Label(self.top, image=self.ils_logo)
        self.label1 = ttk.Label(self.top, text="ILS Dredge Data Logger")

        self.image1.pack(side="left", padx=5, pady=5)
        self.label1.pack(side="right", padx=5, pady=5)

        self.log_status = ttk.Label(self.middle, text="Logger Status")
        self.json_preview = ttk.Label(self.middle, text="JSON String Preview", width=70)

        self.log_status.pack(side="top", padx=5, pady=5, anchor="w")
        self.json_preview.pack(side="bottom", padx=5, pady=5, anchor="w")

        self.button1 = ttk.Button(
            self.bottom,
            text="Manual Backup",
            command=lambda: controller.manual_backup(),
        )
        self.button2 = ttk.Button(self.bottom, text="Config", command=lambda: controller.show_frame("Config"))

        self.button1.pack(side="left", padx=5, pady=5)
        self.button2.pack(side="right", padx=5, pady=5)

        self.top.pack(side="top", anchor="w")
        self.middle.pack(anchor="w", fill="both")
        self.bottom.pack(side="bottom", anchor="w", fill="both")


class Config(ttk.Frame):
    def __init__(self, parent, controller):
        ttk.Frame.__init__(self, parent)
        self.controller = controller

        # Create frames
        self.left_menu = ttk.Frame(self)
        self.right_gen = ttk.Frame(self)
        self.right_email = ttk.Frame(self)
        self.right_mb = ttk.Frame(self)

        self.frames = {}
        self.frames["right_gen"] = self.right_gen
        self.frames["right_email"] = self.right_email
        self.frames["right_mb"] = self.right_mb

        # Create Widgets for frames
        self.general_button = ttk.Button(self.left_menu, text="General", command=lambda: self.show_frame("right_gen"))
        self.email_button = ttk.Button(
            self.left_menu,
            text="Emails",
            command=lambda: self.show_frame("right_email"),
        )
        self.modbus_button = ttk.Button(self.left_menu, text="ModBus", command=lambda: self.show_frame("right_mb"))
        self.save_button = ttk.Button(self.left_menu, text="Save Config", command=lambda: self.save_config())
        self.back_button = ttk.Button(
            self.left_menu,
            text="Back",
            command=lambda: controller.show_frame("StartPage"),
        )

        self.general_button.grid(row=0, padx=2, pady=2, sticky="w")
        self.email_button.grid(row=1, padx=2, pady=2, sticky="w")
        self.modbus_button.grid(row=2, padx=2, pady=2, sticky="w")
        self.save_button.grid(row=3, padx=2, pady=2, sticky="w")
        self.back_button.grid(row=4, padx=2, pady=2, sticky="w")

        # General Screen
        """ Port, Json Path, CSV Path, Email, PLC IP, Dredge Name, Freeboard Name """
        self.gTitle = ttk.Label(self.right_gen, text="General Settings")
        self.gTitle.grid(row=0, column=0, columnspan=2)

        # Port
        self.gPortTitle = ttk.Label(self.right_gen, text="Port: ")
        self.gPort = ttk.Entry(self.right_gen, width=40)
        self.gPort.insert(0, config.vars["port"])
        self.gPortTitle.grid(row=1, column=0, sticky="w")
        self.gPort.grid(row=1, column=1, sticky="w")

        # Json Path
        self.gJSONTitle = ttk.Label(self.right_gen, text="JSON Path: ")
        self.gJSON = ttk.Entry(self.right_gen, width=40)
        self.gJSON.insert(0, config.vars["json_path"])
        self.gJSONTitle.grid(row=2, column=0, sticky="w")
        self.gJSON.grid(row=2, column=1, sticky="w")

        # XML Path
        self.gXMLTitle = ttk.Label(self.right_gen, text="XML Path: ")
        self.gXML = ttk.Entry(self.right_gen, width=40)
        self.gXML.insert(0, config.vars["xml_path"])
        self.gXMLTitle.grid(row=2, column=0, sticky="w")
        self.gXML.grid(row=2, column=1, sticky="w")

        # CSV Path
        self.gCSVTitle = ttk.Label(self.right_gen, text="CSV Path: ")
        self.gCSV = ttk.Entry(self.right_gen, width=40)
        self.gCSV.insert(0, config.vars["csv_path"])
        self.gCSVTitle.grid(row=3, column=0, sticky="w")
        self.gCSV.grid(row=3, column=1, sticky="w")

        # Email
        self.gEmailTitle = ttk.Label(self.right_gen, text="Email: ")
        self.gEmail = ttk.Entry(self.right_gen, width=40)
        self.gEmail.insert(0, config.vars["email"])
        self.gEmailTitle.grid(row=4, column=0, sticky="w")
        self.gEmail.grid(row=4, column=1, sticky="w")

        # PLC IP
        self.gIPTitle = ttk.Label(self.right_gen, text="PLC IP: ")
        self.gIP = ttk.Entry(self.right_gen, width=40)
        self.gIP.insert(0, config.vars["plc_ip"])
        self.gIPTitle.grid(row=5, column=0, sticky="w")
        self.gIP.grid(row=5, column=1, sticky="w")

        # Dredge Name
        self.gDredgeTitle = ttk.Label(self.right_gen, text="Dredge Name: ")
        self.gDredge = ttk.Entry(self.right_gen, width=40)
        self.gDredge.insert(0, config.vars["dredge_name"])
        self.gDredgeTitle.grid(row=6, column=0, sticky="w")
        self.gDredge.grid(row=6, column=1, sticky="w")

        # Freeboard Name
        self.gFreeboardTitle = ttk.Label(self.right_gen, text="Freeboard Name: ")
        self.gFreeboard = ttk.Entry(self.right_gen, width=40)
        self.gFreeboard.insert(0, config.vars["freeboard_name"])
        self.gFreeboardTitle.grid(row=7, column=0, sticky="w")
        self.gFreeboard.grid(row=7, column=1, sticky="w")

        # Email Screen
        """ Email List """

        def rm_sel():
            """Remove selected email from listbox"""
            self.eEmail_box.delete(self.eEmail_box.curselection())

        def add():
            """Add an email to listbox"""
            self.eEmail_box.insert(tk.END, self.eNew.get())

        self.eEmailTitle = ttk.Label(self.right_email, text="Email List")
        self.eRemove = ttk.Button(self.right_email, text="Remove Selected", command=rm_sel)
        self.eAdd = ttk.Button(self.right_email, text="Add Email", command=add)
        self.eNew = ttk.Entry(self.right_email, width=40)
        self.eEmail_box = tk.Listbox(self.right_email, height=-1, width=50)

        for email in config.vars["email_list"]:
            self.eEmail_box.insert(tk.END, email)

        self.eEmailTitle.grid(row=0, column=0, columnspan=3)
        self.eEmail_box.grid(row=1, column=0, columnspan=3, sticky="w")
        self.eRemove.grid(row=3, column=0, sticky="w")
        self.eNew.grid(row=4, column=0, columnspan=2, sticky="w")
        self.eAdd.grid(row=4, column=2, sticky="w")

        # Modbus Screen
        """ Modbus Addresses """

        def mSel():
            self.mAddress.delete(0, tk.END)
            self.mAddress.insert(0, config.vars["modbus"][self.mModbusList.get()]["address"])
            if config.vars["modbus"][self.mModbusList.get()]["float"]:
                self.mFloat.state(["selected"])
            else:
                self.mFloat.state(["!selected"])

        def mSave():
            config.vars["modbus"][self.mModbusList.get()]["address"] = self.mAddress.get()
            config.vars["modbus"][self.mModbusList.get()]["float"] = self.mFloat.state() == "selected"

        def mRemove():
            name = self.mModbusList.get()
            self.mValues.remove(name)
            del config.vars["modbus"][name]
            self.mModbusList["values"] = self.mValues
            self.mModbusList.current(0)
            mSel()

        def mAdd():
            name = self.mNew.get()
            if name not in self.mValues:
                self.mValues.append(name)
            if name not in config.vars["modbus"]:
                config.vars["modbus"][name] = {}
                config.vars["modbus"][name]["name"] = name
                config.vars["modbus"][name]["address"] = "0"
                config.vars["modbus"][name]["float"] = False
            self.mModbusList["values"] = self.mValues
            self.mModbusList.set(name)
            mSel()

        self.mValues = []
        for name in config.vars["modbus"]:
            self.mValues.append(name)

        self.mTitle = ttk.Label(self.right_mb, text="ModBus Addresses")
        self.mModbusList = ttk.Combobox(self.right_mb, values=self.mValues)
        self.mSel = ttk.Button(self.right_mb, text="Select", command=mSel)
        self.mAddressTitle = ttk.Label(self.right_mb, text="Address:")
        self.mAddress = ttk.Entry(self.right_mb, width=10)
        self.mFloatTitle = ttk.Label(self.right_mb, text="Float:")
        self.mFloat = ttk.Checkbutton(self.right_mb)
        self.mSave = ttk.Button(self.right_mb, text="Save", command=mSave)
        self.mRemove = ttk.Button(self.right_mb, text="Remove", command=mRemove)
        self.mNew = ttk.Entry(self.right_mb, width=20)
        self.mAdd = ttk.Button(self.right_mb, text="Add", command=mAdd)

        if config.vars["modbus"]:
            self.mModbusList.current(0)
            mSel()

        self.mTitle.grid(row=0, column=0, columnspan=3)
        self.mModbusList.grid(row=1, column=0, sticky="w")
        self.mSel.grid(row=1, column=1, sticky="w")
        self.mAddressTitle.grid(row=2, column=0, sticky="w")
        self.mAddress.grid(row=2, column=1, sticky="w")
        self.mFloatTitle.grid(row=3, column=0, sticky="w")
        self.mFloat.grid(row=3, column=1, sticky="w")
        self.mSave.grid(row=4, column=0, sticky="w")
        self.mRemove.grid(row=4, column=1, sticky="w")
        self.mNew.grid(row=5, column=0, sticky="w")
        self.mAdd.grid(row=5, column=1, sticky="w")

        # Place Frames
        self.left_menu.grid(row=0, column=0, sticky="nse")
        self.right_gen.grid(row=0, column=1, sticky="nsew")
        self.right_email.grid(row=0, column=1, sticky="nsew")
        self.right_mb.grid(row=0, column=1, sticky="nsew")

        self.show_frame("right_gen")
        # self.show_frame("right_email")
        # self.show_frame("right_mb")

    def show_frame(self, page_name):
        """Set the current frame"""
        frame = self.frames[page_name]
        frame.tkraise()

    def save_config(self):
        """Save the config changes"""
        config.vars["header"] = config.genHeader()

        config.vars["port"] = self.gPort.get()
        config.vars["json_path"] = self.gJSON.get()
        config.vars["xml_path"] = self.gXML.get()
        config.vars["csv_path"] = self.gCSV.get()
        config.vars["plc_ip"] = self.gIP.get()
        config.vars["email"] = self.gEmail.get()
        config.vars["dredge_name"] = self.gDredge.get()
        config.vars["freeboard_name"] = self.gFreeboard.get()

        config.vars["email_list"] = []
        email_box_ls = self.eEmail_box.get(0, self.eEmail_box.size())
        for item in email_box_ls:
            config.vars["email_list"].append(item)

        _logger.info("Saving Config")
        config.save_config()
        _logger.info("Config Saved")


if __name__ == "__main__":
    _logger.debug("Creating GUI")
    app = LogGUI()

    _logger.debug("Starting Thread")
    threading.Thread(target=app.log_loop, daemon=True).start()

    _logger.debug("Launching GUI")
    app.mainloop()
