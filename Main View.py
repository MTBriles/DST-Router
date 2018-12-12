# import modules
import tkinter as tk
import pydicom
import pynetdicom3
import os
from pydicom.filereader import read_dicomdir
from tkinter import *
import image_file
import Views
import pyodbc

# assigning the image_file to a global var here in the Main View.py. Its used in the Class Labels
main_image = image_file.main_image_string


class App(tk.Frame):
    # this is the main window/title screen when the app launches

    def open_readme(self):
        # opens the readme doc
        os.system('ReadMe.txt')

    def __init__(self, parent, *args, **kwargs):
        """This is the display configs for the main view that loads when app launches.  The  Menubar section has
        the following notes: each 'add_command' references a Class in the Views.py file."""

        tk.Frame.__init__(self, parent, *args, **kwargs)
        parent.title('DST DICOM Router')
        parent.geometry('1200x900')
        parent.configure(bg='gray16')

        parent.label = Labels(self, bg='gray16')
        parent.label.grid(row=1)

        menubar = Menu(self.master)
        self.master.config(menu=menubar)
        devices = Menu(menubar, tearoff=0)
        rules = Menu(menubar, tearoff=0)
        anonymize = Menu(menubar, tearoff=0)
        help = Menu(menubar, tearoff=0)
        menubar.add_cascade(label='Devices', menu=devices)
        menubar.add_cascade(label='Rules', menu=rules)
        menubar.add_cascade(label='Anonymize', menu=anonymize)
        menubar.add_cascade(label='Help', menu=help)
        devices.add_command(label='Add/Remove Device', command=Views.Devices)
        rules.add_command(label='Add/Delete Rules', command=Views.Rules)
        rules.add_command(label='Build Rules', command=Views.BuildRules)
        anonymize.add_command(label='Anonymize Config', command=Views.Anonymize)
        help.add_command(label='Read Me', command=self.open_readme)


class Labels(tk.Label):

    def __init__(self, *args, **kwargs):
        """These are the labels/buttons that populate the main view in the Class App."""

        tk.Label.__init__(self, *args, **kwargs)

        self.image = tk.PhotoImage(data=main_image)
        self.label_logo = tk.Label(self, image=self.image)
        self.label_logo.grid(row=0, column=1, pady=15)

        self.label_empty = Label(self, bg='gray16')
        self.label_empty.grid(row=2, column=0, padx=125)

        self.label = tk.Label(self, text='Server Status: ', bg='gray16', fg='alice blue', font=('', 14))
        self.label.grid(row=1, column=1)

        self.label_status = tk.Label(self, text='Status', bg='gray16', fg='red', font=('', 12))
        self.label_status.grid(row=2, column=1, pady=15)

        self.button_start_server = tk.Button(self, text='Start Server', bg='gray20', fg='darkorange1')
        self.button_start_server.grid(row=3, column=1, pady=15)

        self.button_stop_server = tk.Button(self, text='Stop Server', bg='gray20', fg='darkorange1')
        self.button_stop_server.grid(row=4, column=1, pady=15)

        self.text_logs = tk.Text(self, bg='gray14', fg='alice blue', borderwidth=2)
        self.text_logs.grid(row=5, column=1, pady=10)


class Main(tk.Frame):

    def __init__(self, master, *args, **kwargs):
        tk.Frame.__init__(self, master, *args, **kwargs)
        self.app = App(master).grid()


if __name__ == '__main__':
    root = tk.Tk()
    Main(root).grid()
    root.mainloop()
