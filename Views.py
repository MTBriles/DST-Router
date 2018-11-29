import tkinter as tk
import tkinter.scrolledtext as tkst


class Devices(tk.Toplevel):

    def __init__(self, *args, **kwargs):
        tk.Toplevel.__init__(self, *args, **kwargs)
        self.title('Devices')
        self.geometry('900x600')
        self.configure(bg='gray16')
        self.resizable(False, False)

        self.label_sources = tk.Label(self, text=('Devices' + ' :'), bg='gray16', fg='alice blue', font=('', 14))
        self.label_sources.grid(row=0, column=2, sticky=tk.W)

        scrollbar = tk.Scrollbar(self, orient=tk.VERTICAL, bg='gray14')

        lb = tk.Listbox(self, width=130, height=20, yscrollcommand=scrollbar.set, bg='alice blue', fg='gray14')
        lb.grid(row=2, column=1, columnspan=2)
        scrollbar.grid(row=2, column=3, sticky=tk.N+tk.S)

        for x in range(50):
            lb.insert(tk.END, str(x))

        self.label_new_source = tk.Label(self, text='Add New Device', bg='gray16', fg='alice blue', font=('', 12))
        self.label_new_source.grid(row=3, column=2, sticky=tk.W)

        self.label_ae = tk.Label(self, text='AE:', bg='gray16', fg='alice blue')
        self.label_ae.grid(row=4, column=0, sticky=tk.E, pady=10)

        self.entry_ae = tk.Entry(self, bg='gray14', fg='alice blue', bd=2)
        self.entry_ae.grid(row=4, column=1, sticky=tk.W, pady=10)

        self.label_ip = tk.Label(self, text='IP:', bg='gray16', fg='alice blue')
        self.label_ip.grid(row=5, column=0, sticky=tk.E, pady=10)

        self.entry_ip = tk.Entry(self, bg='gray14', fg='alice blue', bd=2)
        self.entry_ip.grid(row=5, column=1, sticky=tk.W, pady=10)

        self.label_port = tk.Label(self, text='Port:', bg='gray16', fg='alice blue')
        self.label_port.grid(row=6, column=0, sticky=tk.E, pady=10)

        self.entry_port = tk.Entry(self, bg='gray14', fg='alice blue', bd=2)
        self.entry_port.grid(row=6, column=1, sticky=tk.W, pady=10)

        self.label_name = tk.Label(self, text='Device Name:', bg='gray16', fg='alice blue')
        self.label_name.grid(row=7, column=0, sticky=tk.E, pady=10)

        self.entry_name = tk.Entry(self, bg='gray14', fg='alice blue', bd=2)
        self.entry_name.grid(row=7, column=1, sticky=tk.W, pady=10)

        self.button_add_source = tk.Button(self, text='ADD Device', bg='gray14', fg='red')
        self.button_add_source.grid(row=4, column=2, sticky=tk.W)

        self.button_remove_source = tk.Button(self, text='Remove Device', bg='gray14', fg='red')
        self.button_remove_source.grid(row=6, column=2, sticky=tk.W)

        self.button_echo = tk.Button(self, text='DICOM ECHO', bg='gray14', fg='red')
        self.button_echo.grid(row=5, column=2, sticky=tk.W)


class Rules(tk.Toplevel):

    def __init__(self, *args, **kwargs):
        tk.Toplevel.__init__(self, *args, **kwargs)
        self.title('Routing Rules')
        self.geometry('330x300')
        self.configure(bg='gray16')


class ActiveRules(tk.Toplevel):

    def __init__(self, *args, **kwargs):
        tk.Toplevel.__init__(self, *args, **kwargs)
        self.title('Active Rules')
        self.geometry('330x300')
        self.configure(bg='gray16')


if __name__ == '__main__':
    root = tk.Tk()
    Sources(root).pack()
    root.mainloop()
