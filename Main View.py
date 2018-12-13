# import modules
import tkinter as tk
import pydicom
import pynetdicom3
import os
from pydicom.filereader import read_dicomdir
from tkinter import *
from tkinter import messagebox
import image_file
import Views
import pyodbc
import run_services
from threading import Timer
import sys
import time

# assigning the image_file to a global var here in the Main View.py. Its used in the Class Labels
main_image = image_file.main_image_string
services = run_services
var = Tk()


def label(self, text,  row, column, font=None, pady=None, sticky=None, columnspan=None, padx=None):
    _l = tk.Label(self, text=text, bg='gray16', fg='alice blue', font=font)
    _l.grid(row=row, column=column, pady=pady, sticky=sticky, columnspan=columnspan, padx=padx)


def button(self, text, command, row, column, sticky=None, pady=None):
    _b = tk.Button(self, text=text, command=command, bg='gray14', fg='darkorange1')
    _b.grid(row=row, column=column, sticky=sticky, pady=pady)


class Main(tk.Frame):

    def open_readme(self):
        # opens the readme doc
        os.system('ReadMe.txt')

    def __init__(self, master):
        tk.Frame.__init__(self, master)
        master.title('DST DICOM Router')
        master.geometry('1200x900')
        master.configure(bg='gray16', highlightbackground='gray16', highlightcolor='gray16')

        menubar = Menu(self.master)
        self.master.config(menu=menubar)
        devices = Menu(menubar, tearoff=0)
        rules = Menu(menubar, tearoff=0)
        anonymize = Menu(menubar, tearoff=0)
        service = Menu(menubar, tearoff=0)
        help = Menu(menubar, tearoff=0)
        menubar.add_cascade(label='Devices', menu=devices)
        menubar.add_cascade(label='Rules', menu=rules)
        menubar.add_cascade(label='Configure', menu=anonymize)
        menubar.add_cascade(label='Services', menu=service)
        menubar.add_cascade(label='Help', menu=help)
        devices.add_command(label='Add/Remove Device', command=Views.Devices)
        rules.add_command(label='Activate/Delete Rules', command=Views.Rules)
        rules.add_command(label='Build Rules', command=Views.BuildRules)
        anonymize.add_command(label='DSTools Config', command=Views.DSTConfig)
        service.add_command(label='Create Service', command=services.create_service)
        service.add_command(label='Remove Service', command=services.remove_service)
        help.add_command(label='Read Me', command=self.open_readme)

        self.image = tk.PhotoImage(data=main_image)
        self.label_logo = tk.Label(master, image=self.image, bg='gray16')
        self.label_logo.grid(row=0, column=1, pady=15)

        label(master, '', 2, 0, padx=125, sticky=tk.NSEW)
        label(master, 'Server Status: ', 1, 1, font=('', 14))

        button(master, 'Start Server', services.start_service, 3, 1, pady=15)
        button(master, 'Stop Server', services.stop_service, 4, 1, pady=15)

        self.var = StringVar()
        self.label_status = tk.Label(master, textvariable=self.var, bg='gray16', fg='red', font=('', 12))
        self.label_status.grid(row=2, column=1, pady=15)

        self.text_logs = tk.Text(master, bg='gray14', fg='alice blue', borderwidth=2, highlightbackground='gray16')
        self.text_logs.grid(row=5, column=1, pady=10)

        self.var = StringVar()
        self.label_status = tk.Label(master, textvariable=self.var, bg='gray16', fg='red', font=('', 12))
        self.label_status.grid(row=2, column=1, pady=15)
        self.check()

    def check(self):
        if services.check_service() == 'Not_Installed':
            self.var.set('***Service not installed***')
            self.label_status.configure(fg='red')
            self.label_status.after(1000, self.check)

        elif services.check_service() == 'Running':
            self.var.set('***Running***')
            self.label_status.configure(fg='green')
            self.label_status.after(1000, self.check)
        elif services.check_service() == 'Stopped':
            self.var.set('***Stopped***')
            self.label_status.configure(fg='red')
            self.label_status.after(1000, self.check)
        else:
            self.check.quit()


def on_closing():
    if messagebox.askokcancel('Quit', 'Do you want to quit?'):
        var.destroy()
        sys.exit()


c = Main(var)
var.protocol('WM_DELETE_WINDOW', on_closing)
var.mainloop()

