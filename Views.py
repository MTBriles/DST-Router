import os
try:
    import tkinter as tk
    import tkinter.scrolledtext as tkst
    import SQL
    import DICOM_Utils
    import tkinter.font as tkFont
    import tkinter.ttk as ttk
except ImportError:
    print('Failed to import required methods')

dcm_util = DICOM_Utils.DICOMEcho


class Devices(tk.Toplevel):

    def device_added(self):
        print('test2')
        ae = ()
        ip = ()
        name = ()
        port = ()
        if len(self.entry_ae.get()) == 0:
            self.label_blank_ae.grid(row=7, column=2, sticky=tk.W, columnspan=2)
        else:
            ae = self.entry_ae.get()
        if len(self.entry_ip.get()) == 0:
            self.label_blank_ip.grid(row=7, column=2, sticky=tk.W, columnspan=2)
        else:
            ip = self.entry_ip.get()
        if len(self.entry_name.get()) == 0:
            self.label_blank_name.grid(row=7, column=2, sticky=tk.W, columnspan=2)
        else:
            name = self.entry_name.get()
        if len(self.entry_port.get()) == 0:
            self.label_blank_port.grid(row=7, column=2, sticky=tk.W, columnspan=2)
        else:
            port = self.entry_port.get()
        self.sql_add = str(ae+','+ip+','+name+','+port)
        print(sql_add)
        #SQL.add_device()
        self.label_device_added.grid(row=7, column=2)
        #print('test3')
        return self.sql_add

    def dicom_echo(self):
        print('DICOM Echo')
        self.dcm = dcm_util.dcm_echo(self)
        self.check()

    def check(self):
        if str(self.dcm) == 'association':
            self.label_association_fail.grid(row=7, column=2, sticky=tk.W, columnspan=2)
        elif str(self.dcm) == 'port':
            self.label_port_fail.grid(row=7, column=2, sticky=tk.W, columnspan=2)
        elif str(self.dcm) == 'ping':
            self.label_ping_fail.grid(row=7, column=2, sticky=tk.W, columnspan=2)
        elif str(self.dcm) == 'success':
            self.label_echo_success.grid(row=7, column=2, sticky=tk.W, columnspan=2)

    def __init__(self):
        tk.Toplevel.__init__(self)

        self.configure(bg='gray16')
        self.geometry('950x525')
        self.tree = None
        self._setup_widgets()
        self._build_tree()

        self.label_sources = tk.Label(self, text=('Devices' + ' :'), bg='gray16', fg='alice blue', font=('', 14))
        self.label_sources.grid(row=0, column=2, sticky=tk.W)

        self.label_new_source = tk.Label(self, text='Add New Device', bg='gray16', fg='alice blue', font=('', 12))
        self.label_new_source.grid(row=3, column=2, sticky=tk.W)

    def _setup_widgets(self):
        # create a treeview with scorllbar
        container = ttk.Frame(self)

        self.tree = ttk.Treeview(self, columns=c_headers, show='headings')
        vsb = ttk.Scrollbar(self, orient='vertical', command=self.tree.yview)

        self.tree.configure(yscrollcommand=vsb.set)
        self.tree.grid(row=2, column=1, columnspan=2)
        vsb.grid(row=2, column=3, sticky=tk.W + tk.N + tk.S)

        container.grid_columnconfigure(0, weight=1)
        container.grid_rowconfigure(0, weight=1)

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

        self.button_add_source = tk.Button(self, text='ADD Device', bg='gray14',
                                           fg='red', command=self.device_added)
        self.button_add_source.grid(row=4, column=2, sticky=tk.W)

        self.button_remove_source = tk.Button(self, text='Remove Device', bg='gray14', fg='red')
        self.button_remove_source.grid(row=6, column=2, sticky=tk.W)

        self.button_echo = tk.Button(self, text='DICOM ECHO', bg='gray14', fg='red', command=self.dicom_echo)
        self.button_echo.grid(row=5, column=2, sticky=tk.W)

        self.label_device_added = tk.Label(self, text='Device Added!', bg='gray16', fg='red')

        self.label_association_fail = tk.Label(self, text='PORT IS OPEN BUT DICOM ASSOCIATION FAILED', bg='gray16',
                                               fg='RED')

        self.label_port_fail = tk.Label(self, text='PORT IS BLOCKED BUT YOU CAN PING THE IP', bg='gray16', fg='RED')

        self.label_ping_fail = tk.Label(self, text='COULD NOT PING IP', bg='gray16', fg='RED')

        self.label_echo_success = tk.Label(self, text='SUCCESS', bg='gray16', fg='GREEN')

        self.label_blank_ae = tk.Label(self, text='***AE cannot have NULL Value***', bg='gray16', fg='red')
        self.label_blank_port = tk.Label(self, text='***PORT cannot have NULL Value***', bg='gray16', fg='red')
        self.label_blank_ip = tk.Label(self, text='***IP cannot have NULL Value***', bg='gray16', fg='red')
        self.label_blank_name = tk.Label(self, text='***Device Name cannot have NULL Value***', bg='gray16', fg='red')


    def _build_tree(self):
        for col in c_headers:
            self.tree.heading(col, text=col.title())
            # adjust the columns width to the header string
            self.tree.column(col, width=tkFont.Font().measure(col.title()))

        for item in c_list:
            print(self.tree.insert('', 'end', values=item))
            # adjust columns width if necessary to fit each value
            for ix, val in enumerate(item):
                col_w = tkFont.Font().measure(val)
                if self.tree.column(c_headers[ix], width=130): # <col_w:
                    self.tree.column(c_headers[ix], width=col_w)

    def selection(self, event):
        """"
        gets selected item id and prints them
        """
        id = self.tree.identify_row(event.y)
        print('selection', id)


c_headers = ['ID', 'Name', 'IP', 'AE', 'PORT', 'Threads']
c_list = [
    ('1', 'PACS', 'IP1', 'AE1', 'port1', 'thread1'),
    ('2', 'PACS2', 'IP2', 'AE2', 'port2', 'thread2'),
    ('3', 'PACS3', 'IP3', 'AE3', 'port3', 'thread3')
]


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

"""
if __name__ == '__main__':
    root = tk.Tk()
    Devices(root).grid()
    root.mainloop()

root = tk.Tk()
root.wm_title('Devices')
listbox = Devices(root)
root.mainloop()
"""
