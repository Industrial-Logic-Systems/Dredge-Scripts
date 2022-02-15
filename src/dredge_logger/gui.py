import datetime
import logging
import os
import threading
import time
import tkinter as tk
import tkinter.ttk as ttk

from dredge_logger import backup
from dredge_logger import Log
from dredge_logger.config import config
from ttkthemes import ThemedTk

_logger = logging.getLogger(__name__)


class LogGUI(ThemedTk):
    def __init__(self, *args, **kwargs):
        ThemedTk.__init__(self, *args, **kwargs)

        # Set Window properties
        self.winfo_toplevel().title("ILS Logger")
        self.iconbitmap(config._proj_dir + "/resources/ILS-logo.ico")
        self.set_theme("black", toplevel=True, themebg=True)
        self.geometry("800x600")

        # Create Container that holds all frames
        container = tk.Frame(self)
        container.place(x=0, y=0, relwidth=1, relheight=1)

        # Create all the frames
        self.frames = {}
        for F in [StartPage, Config]:
            page_name = F.__name__
            frame = F(parent=container, controller=self)
            self.frames[page_name] = frame

            frame.place(x=0, y=0, relwidth=1, relheight=1)

        self.show_frame("StartPage")

    def show_frame(self, page_name):
        """Set the current frame"""
        frame = self.frames[page_name]
        frame.tkraise()

    def manual_backup(self):
        """Manually Run a Backup"""
        _logger.debug("Manual Backup Started")
        filename = self.frames["StartPage"].backup_date.get()
        if not filename:
            filename = datetime.datetime.today().strftime("%Y-%m-%d")

        threading.Thread(target=backup.backup_files, args=(filename,)).start()

    def log_loop(self):
        """Will start a while loop that calls the log function"""
        _logger.info("Starting Log")
        self.frames["StartPage"].status_label.config(text="Log Loop Running")
        while True:
            result = Log.log()
            if result[0]:
                self.frames["StartPage"].status_label.config(text="Log Loop Running")
                self.frames["StartPage"].msg_time_label.config(text=result[1]["msg_time"])
                self.frames["StartPage"].latitude_label.config(text=result[1]["latitude"])
                self.frames["StartPage"].longitude_label.config(text=result[1]["longitude"])
            else:
                self.frames["StartPage"].status_label.config(text="Loging Failed retrying in 2 seconds...")
                time.sleep(2)


class StartPage(ttk.Frame):
    def __init__(self, parent, controller):
        ttk.Frame.__init__(self, parent)
        self.controller = controller

        self.style = ttk.Style()
        self.style.configure("my.TButton", font=("Helvetica", 15), anchor=tk.CENTER)

        self.ils_logo = tk.PhotoImage(file=config._proj_dir + "\\resources\\ILS-logo_100x100.png")
        self.logo_image = ttk.Label(self, image=self.ils_logo)
        self.logo_image.place(x=20, y=5)

        self.greeting = ttk.Label(self, text="ILS Dredge Data Logger", font=("Helvetica", 20))
        self.greeting.place(x=140, y=35)

        left_x1 = 20
        left_x2 = 160

        self.status = ttk.Label(self, text="Logger Status:", font=("Helvetica", 15))
        self.status.place(x=left_x1, y=110)
        self.status_label = ttk.Label(self, text="Not Started", font=("Helvetica", 15))
        self.status_label.place(x=left_x2, y=110)

        self.msg_time = ttk.Label(self, text="MSG Time:", font=("Helvetica", 15))
        self.msg_time.place(x=left_x1, y=140)
        self.msg_time_label = ttk.Label(self, text="Not Received Yet", font=("Helvetica", 15))
        self.msg_time_label.place(x=left_x2, y=140)

        self.latitude = ttk.Label(self, text="Latitude:", font=("Helvetica", 15))
        self.latitude.place(x=left_x1, y=170)
        self.latitude_label = ttk.Label(self, text="Not Received Yet", font=("Helvetica", 15))
        self.latitude_label.place(x=left_x2, y=170)

        self.longitude = ttk.Label(self, text="Longitude:", font=("Helvetica", 15))
        self.longitude.place(x=left_x1, y=200)
        self.longitude_label = ttk.Label(self, text="Not Received Yet", font=("Helvetica", 15))
        self.longitude_label.place(x=left_x2, y=200)

        button_x = 610
        button_width = 15
        button_padding = 40
        button_y_start = 400
        buttons = [
            ["Config", lambda: controller.show_frame("Config")],
            ["Open Data Dir", lambda: os.startfile(config._dirs.user_data_dir)],
            ["Open CSV Dir", lambda: os.startfile(config.vars["csv_path"])],
            ["Open JSON Dir", lambda: os.startfile(config.vars["json_path"])],
            ["Open XML Dir", lambda: os.startfile(config.vars["xml_path"])],
        ]

        for i, button in enumerate(buttons):
            buttons[i] = ttk.Button(self, text=button[0], style="my.TButton", width=button_width, command=button[1])
            buttons[i].place(x=button_x, y=button_y_start + (i * button_padding))

        self.backup_label = ttk.Label(
            self, text="Enter Date to backup, leave BLANK for Today, (YYYY-MM-DD)", font=("Helvetica")
        )
        self.backup = ttk.Button(
            self, text="Manual Backup", style="my.TButton", width=button_width, command=self.controller.manual_backup
        )
        self.backup_date = ttk.Entry(self, width=20, font=("Helvetica", 15))

        self.backup_label.place(x=10, y=530)
        self.backup.place(x=10, y=560)
        self.backup_date.place(x=200, y=562)


class Config(ttk.Frame):
    def __init__(self, parent, controller):
        ttk.Frame.__init__(self, parent)
        self.controller = controller

        self.style = ttk.Style()
        self.style.configure("menu.TFrame", background="gray20")
        self.style.configure("menu.TButton", font=("Helvetica", 15), anchor=tk.CENTER)
        self.style.configure("config.TCheckbutton", font=("Helvetica", 15))
        self.style.configure("mb.TButton", font=("Helvetica", 15), anchor=tk.CENTER)
        self.style.configure("e.TButton", font=("Helvetica", 15), anchor=tk.CENTER)
        self.style.configure("i.TButton", font=("Helvetica", 15), anchor=tk.CENTER)

        # Create frames
        self.menu = ttk.Frame(self, style="menu.TFrame")
        self.general = ttk.Frame(self)
        self.modbus = ttk.Frame(self)
        self.email = ttk.Frame(self)
        self.image = ttk.Frame(self)

        self.frames = {}
        self.frames["general"] = self.general
        self.frames["modbus"] = self.modbus
        self.frames["email"] = self.email
        self.frames["image"] = self.image

        # Menu Buttons
        button_x_start = 10
        button_y = 15
        button_width = 8
        button_padding = 135
        buttons = [
            ["General", lambda: self.show_frame("general")],
            ["Modbus", lambda: self.show_frame("modbus")],
            ["Email", lambda: self.show_frame("email")],
            ["Images", lambda: self.show_frame("image")],
            ["Save", lambda: self.save_config()],
            ["Back", lambda: controller.show_frame("StartPage")],
        ]

        for i, button in enumerate(buttons):
            buttons[i] = ttk.Button(self, text=button[0], style="menu.TButton", width=button_width, command=button[1])
            buttons[i].place(x=button_x_start + (i * button_padding), y=button_y)

        # General Frame
        self.general_frame()

        # Modbus Frame
        self.modbus_frame()

        # Email Frame
        self.email_frame()

        # Image Frame
        self.image_frame()

        # Place Frames
        self.menu.place(x=0, y=0, relwidth=1, height=60)
        self.general.place(x=0, y=60, relwidth=1, height=540)
        self.modbus.place(x=0, y=60, relwidth=1, height=540)
        self.email.place(x=0, y=60, relwidth=1, height=540)
        self.image.place(x=0, y=60, relwidth=1, height=540)

        self.show_frame("general")

    def general_frame(self):
        """Dredge Type, Dredge Name, Port, JSON Path, CSV Path, XML Path, Image Path, PLC IP, Email, Freeboard Name, CSV0600"""
        self.gTitle = ttk.Label(self.general, text="General Settings", font=("Helvetica", 20), anchor=tk.CENTER)
        self.gTitle.place(x=0, y=0, relwidth=1)

        start_x = 10
        entry_x = 175
        start_y = 50
        padding = 30
        entry_width = 55

        text_configs = [
            ["Port", "port"],
            ["Dredge Type", "dredge_type"],
            ["Dredge Name", "dredge_name"],
            ["JSON Path", "json_path"],
            ["CSV Path", "csv_path"],
            ["XML Path", "xml_path"],
            ["Image Path", "image_path"],
            ["PLC IP", "plc_ip"],
            ["Email", "email"],
            ["Freeboard Name", "freeboard_name"],
        ]

        self.gEntries = {}
        for i, cfg in enumerate(text_configs):
            self.gEntries[cfg[1]] = [
                ttk.Label(self.general, text=f"{cfg[0]}:", font=("Helvetica", 15)),
                ttk.Entry(self.general, width=entry_width, font=("Helvetica", 15)),
            ]
            self.gEntries[cfg[1]][1].insert(0, config.vars[cfg[1]])
            self.gEntries[cfg[1]][0].place(x=start_x, y=start_y + (i * padding))
            self.gEntries[cfg[1]][1].place(x=entry_x, y=start_y + (i * padding))

        self.gCSV0600 = ttk.Checkbutton(self.general, text="CSV0600", style="config.TCheckbutton")
        if config.vars["csv0600"]:
            self.gCSV0600.state(["selected"])
        else:
            self.gCSV0600.state(["!selected"])
        self.gCSV0600.place(x=10, y=400)

    def modbus_frame(self):
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
            self.save_config()

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

        def mbSel():
            self.mbAddress.delete(0, tk.END)
            self.mbAddress.insert(0, config.vars["modbus_bits"][self.mbModbusList.get()]["address"])

        def mbSave():
            config.vars["modbus_bits"][self.mbModbusList.get()]["address"] = self.mbAddress.get()
            self.save_config()

        def mbRemove():
            name = self.mbModbusList.get()
            self.mbValues.remove(name)
            del config.vars["modbus_bits"][name]
            self.mbModbusList["values"] = self.mbValues
            self.mbModbusList.current(0)
            mbSel()

        def mbAdd():
            name = self.mbNew.get()
            if name not in self.mbValues:
                self.mbValues.append(name)
            if name not in config.vars["modbus_bits"]:
                config.vars["modbus_bits"][name] = {}
                config.vars["modbus_bits"][name]["name"] = name
                config.vars["modbus_bits"][name]["address"] = "0"
            self.mbModbusList["values"] = self.mbValues
            self.mbModbusList.set(name)
            mbSel()

        self.mTitle = ttk.Label(self.modbus, text="Modbus Settings", font=("Helvetica", 20), anchor=tk.CENTER)
        self.mTitle.place(x=0, y=0, relwidth=1)

        self.MB = ttk.Frame(self.modbus)
        self.MBB = ttk.Frame(self.modbus)

        # Modbus Registers
        self.mValues = []
        for name in config.vars["modbus"]:
            self.mValues.append(name)

        self.mTitle = ttk.Label(self.MB, text="ModBus", font=("Helvetica", 18), anchor=tk.CENTER)
        self.mModbusList = ttk.Combobox(self.MB, values=self.mValues, height=20)
        self.mSel = ttk.Button(self.MB, text="Select", style="mb.TButton", command=mSel)
        self.mAddressTitle = ttk.Label(self.MB, text="Address:", font=("Helvetica", 15))
        self.mAddress = ttk.Entry(self.MB, width=10, font=("Helvetica", 15))
        self.mFloatTitle = ttk.Label(self.MB, text="Float:", font=("Helvetica", 15))
        self.mFloat = ttk.Checkbutton(self.MB)
        self.mSave = ttk.Button(self.MB, text="Save", style="mb.TButton", command=mSave)
        self.mRemove = ttk.Button(self.MB, text="Remove", style="mb.TButton", command=mRemove)
        self.mNew = ttk.Entry(self.MB, width=20, font=("Helvetica", 15))
        self.mAdd = ttk.Button(self.MB, text="Add", style="mb.TButton", command=mAdd)

        if config.vars["modbus"]:
            self.mModbusList.current(0)
            mSel()

        mb_x2 = 280

        self.mTitle.place(x=0, y=0, relwidth=1)
        self.mModbusList.place(x=20, y=55)
        self.mSel.place(x=mb_x2, y=50)
        self.mAddressTitle.place(x=20, y=80)
        self.mAddress.place(x=mb_x2, y=85)
        self.mFloatTitle.place(x=20, y=110)
        self.mFloat.place(x=mb_x2, y=115)
        self.mSave.place(x=20, y=140)
        self.mRemove.place(x=mb_x2, y=140)
        self.mNew.place(x=20, y=180)
        self.mAdd.place(x=mb_x2, y=180)

        # Modbus Bits
        self.mbValues = []
        for name in config.vars["modbus_bits"]:
            self.mbValues.append(name)

        self.mbTitle = ttk.Label(self.MBB, text="ModBus Bits", font=("Helvetica", 18), anchor=tk.CENTER)
        self.mbModbusList = ttk.Combobox(self.MBB, values=self.mbValues, height=20)
        self.mbSel = ttk.Button(self.MBB, text="Select", style="mb.TButton", command=mbSel)
        self.mbAddressTitle = ttk.Label(self.MBB, text="Address:", font=("Helvetica", 15))
        self.mbAddress = ttk.Entry(self.MBB, width=10, font=("Helvetica", 15))
        self.mbSave = ttk.Button(self.MBB, text="Save", style="mb.TButton", command=mbSave)
        self.mbRemove = ttk.Button(self.MBB, text="Remove", style="mb.TButton", command=mbRemove)
        self.mbNew = ttk.Entry(self.MBB, width=20, font=("Helvetica", 15))
        self.mbAdd = ttk.Button(self.MBB, text="Add", style="mb.TButton", command=mbAdd)

        if config.vars["modbus_bits"]:
            self.mbModbusList.current(0)
            mbSel()

        mb_x2 = 280

        self.mbTitle.place(x=0, y=0, relwidth=1)
        self.mbModbusList.place(x=20, y=55)
        self.mbSel.place(x=mb_x2, y=50)
        self.mbAddressTitle.place(x=20, y=80)
        self.mbAddress.place(x=mb_x2, y=85)
        self.mbSave.place(x=20, y=110)
        self.mbRemove.place(x=mb_x2, y=110)
        self.mbNew.place(x=20, y=150)
        self.mbAdd.place(x=mb_x2, y=150)

        self.MB.place(x=0, y=40, relwidth=1, height=250)
        self.MBB.place(x=0, y=290, relwidth=1, height=250)

    def email_frame(self):
        def rm_sel():
            """Remove selected email from listbox"""
            self.eEmail_box.delete(self.eEmail_box.curselection())

        def add():
            """Add an email to listbox"""
            self.eEmail_box.insert(tk.END, self.eNew.get())

        self.eTitle = ttk.Label(self.email, text="Email Settings", font=("Helvetica", 20), anchor=tk.CENTER)
        self.eTitle.place(x=0, y=0, relwidth=1)

        self.eEmail_box = tk.Listbox(self.email, font=("Helvetica", 15))
        self.eRemove = ttk.Button(self.email, text="Remove Selected", style="e.TButton", command=rm_sel)
        self.eAdd = ttk.Button(self.email, text="Add Email", style="e.TButton", command=add)
        self.eNew = ttk.Entry(self.email, width=40, font=("Helvetica", 15))

        for email in config.vars["email_list"]:
            self.eEmail_box.insert(tk.END, email)

        self.eEmail_box.place(x=0, y=0, relwidth=1, height=490)
        self.eRemove.place(x=2, y=500, width=180)
        self.eNew.place(x=182, y=502)
        self.eAdd.place(x=632, y=500, width=165)

    def image_frame(self):
        def iSel():
            self.iUnit.delete(0, tk.END)
            self.iUnit.insert(0, config.vars["images"]["graphs"][self.iImageList.get()]["unit"])
            self.iVar.delete(0, tk.END)
            self.iVar.insert(0, config.vars["images"]["graphs"][self.iImageList.get()]["variable"])

        def iSave():
            config.vars["images"]["graphs"][self.iImageList.get()]["unit"] = self.iUnit.get()
            config.vars["images"]["graphs"][self.iImageList.get()]["variable"] = self.iVar.get()

        def iRemove():
            name = self.iImageList.get()
            self.iImages.remove(name)
            del config.vars["images"]["graphs"][name]
            self.iImageList["values"] = self.iImages
            self.iImageList.current(0)
            iSel()

        def iAdd():
            name = self.iNew.get()
            if name not in self.iImages:
                self.iImages.append(name)
            if name not in config.vars["images"]["graphs"]:
                config.vars["images"]["graphs"][name] = {}
                config.vars["images"]["graphs"][name]["name"] = name
                config.vars["images"]["graphs"][name]["unit"] = ""
                config.vars["images"]["graphs"][name]["variable"] = ""
            self.iImageList["values"] = self.iImages
            self.iImageList.set(name)
            iSel()

        self.iTitle = ttk.Label(self.image, text="Image Settings", font=("Helvetica", 20), anchor=tk.CENTER)
        self.iTitle.place(x=0, y=0, relwidth=1)

        self.iCreateImages = ttk.Checkbutton(self.image, text="Generate?", style="config.TCheckbutton")
        if config.vars["images"]["save"]:
            self.iCreateImages.state(["selected"])
        else:
            self.iCreateImages.state(["!selected"])

        self.iTimeLabel = ttk.Label(self.image, text="Time Variable", font=("Helvetica", 15), anchor=tk.CENTER)
        self.iTime = ttk.Entry(self.image, width=20, font=("Helvetica", 15))
        self.iTime.insert(0, config.vars["images"]["time"])

        self.iImages = []
        for name in config.vars["images"]["graphs"]:
            if name not in ["save", "time"]:
                self.iImages.append(name)

        self.iImageList = ttk.Combobox(self.image, values=self.iImages, height=20)
        self.iSel = ttk.Button(self.image, text="Select", width=19, style="i.TButton", command=iSel)
        self.iUnitTitle = ttk.Label(self.image, text="Unit:", font=("Helvetica", 15))
        self.iUnit = ttk.Entry(self.image, width=20, font=("Helvetica", 15))
        self.iVarTitle = ttk.Label(self.image, text="Variable:", font=("Helvetica", 15))
        self.iVar = ttk.Entry(self.image, width=20, font=("Helvetica", 15))
        self.iSave = ttk.Button(self.image, text="Save", width=19, style="i.TButton", command=iSave)
        self.iRemove = ttk.Button(self.image, text="Remove", width=19, style="i.TButton", command=iRemove)
        self.iNew = ttk.Entry(self.image, width=20, font=("Helvetica", 15))
        self.iAdd = ttk.Button(self.image, text="Add", width=19, style="i.TButton", command=iAdd)

        if config.vars["images"]["graphs"]:
            self.iImageList.current(0)
            iSel()

        i_x1 = 10
        i_x2 = 280

        self.iCreateImages.place(x=i_x1, y=60)
        self.iTimeLabel.place(x=i_x1, y=90)
        self.iTime.place(x=i_x2, y=90)
        self.iImageList.place(x=i_x1, y=125)
        self.iSel.place(x=i_x2, y=120)
        self.iUnitTitle.place(x=i_x1, y=150)
        self.iUnit.place(x=i_x2, y=152)
        self.iVarTitle.place(x=i_x1, y=180)
        self.iVar.place(x=i_x2, y=180)
        self.iSave.place(x=i_x1, y=210)
        self.iRemove.place(x=i_x2, y=210)
        self.iNew.place(x=i_x1, y=250)
        self.iAdd.place(x=i_x2, y=250)

    def show_frame(self, page_name):
        """Set the current frame"""
        frame = self.frames[page_name]
        frame.tkraise()

    def save_config(self):
        """Save the config changes"""

        config.vars["port"] = self.gEntries["port"][1].get()
        config.vars["dredge_type"] = self.gEntries["dredge_type"][1].get()
        config.vars["dredge_name"] = self.gEntries["dredge_name"][1].get()
        config.vars["json_path"] = self.gEntries["json_path"][1].get()
        config.vars["csv_path"] = self.gEntries["csv_path"][1].get()
        config.vars["xml_path"] = self.gEntries["xml_path"][1].get()
        config.vars["image_path"] = self.gEntries["image_path"][1].get()
        config.vars["plc_ip"] = self.gEntries["plc_ip"][1].get()
        config.vars["email"] = self.gEntries["email"][1].get()
        config.vars["freeboard_name"] = self.gEntries["freeboard_name"][1].get()
        config.vars["csv0600"] = self.gCSV0600.instate(["selected"])

        config.vars["email_list"] = []
        email_box_ls = self.eEmail_box.get(0, self.eEmail_box.size())
        for item in email_box_ls:
            config.vars["email_list"].append(item)

        config.vars["images"]["save"] = self.iCreateImages.instate(["selected"])
        config.vars["images"]["time"] = self.iTime.get()

        config.vars["header"] = config.genHeader()

        _logger.info("Saving Config")
        config.save_config()
        _logger.info("Config Saved")


if __name__ == "__main__":
    _logger.debug("Creating GUI")
    app = LogGUI()

    # _logger.debug("Starting Thread")
    # threading.Thread(target=app.log_loop, daemon=True).start()

    _logger.debug("Launching GUI")
    app.mainloop()
