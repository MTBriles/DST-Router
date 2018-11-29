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

main_image = image_file.main_image_string


class App(tk.Frame):

    def open_readme(self):
        os.system('ReadMe.txt')

    def __init__(self, parent, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)
        parent.title('DST DICOM Router')
        parent.geometry('1200x900')
        parent.configure(bg='gray16')

        parent.label = Labels(self, bg='gray16')
        parent.label.pack()

        menubar = Menu(self.master)
        self.master.config(menu=menubar)
        devices = Menu(menubar, tearoff=0)
        rules = Menu(menubar, tearoff=0)
        help = Menu(menubar, tearoff=0)
        menubar.add_cascade(label='Devices', menu=devices)
        menubar.add_cascade(label='Rules', menu=rules)
        menubar.add_cascade(label='Help', menu=help)
        devices.add_command(label='Add/Remove Device', command=Views.Devices)
        rules.add_command(label='Add/Delete Rules', command=Views.Rules)
        rules.add_command(label='Active Rules', command=Views.ActiveRules)
        help.add_command(label='Read Me', command=self.open_readme)


class Labels(tk.Label):

    def __init__(self, *args, **kwargs):
        tk.Label.__init__(self, *args, **kwargs)

        self.image = tk.PhotoImage(data=main_image)
        self.label_logo = tk.Label(self, image=self.image)
        self.label_logo.pack(pady=15)

        self.label = tk.Label(self, text='Server Status: ', bg='gray16', fg='alice blue', font=('', 14))
        self.label.pack()

        self.label_status = tk.Label(self, text='Status', bg='gray16', fg='red', font=('', 12))
        self.label_status.pack(pady=15)

        self.button_start_server = tk.Button(self, text='Start Server', bg='gray20', fg='alice blue')
        self.button_start_server.pack(pady=15)

        self.button_stop_server = tk.Button(self, text='Stop Server', bg='gray20', fg='alice blue')
        self.button_stop_server.pack(pady=15)

        self.text_logs = tk.Text(self, bg='gray14', fg='alice blue', borderwidth=2)
        self.text_logs.pack(pady=10)


class Main(tk.Frame):

    def __init__(self, master, *args, **kwargs):
        tk.Frame.__init__(self, master, *args, **kwargs)
        self.app = App(master).pack()



if __name__ == '__main__':
    root = tk.Tk()
    Main(root).pack()
    root.mainloop()
