import os
try:
    import tkinter as tk
    import tkinter.scrolledtext as tkst
    import SQL
    import DICOM_Utils
    import tkinter.font as tkFont
    import tkinter.ttk as ttk
    import tag_dict
except ImportError:
    print('Failed to import required methods')

""" Takes the DICOMEcho class from DICOM_Utiles.py file and assigns it to a global var here in the Views.py.  
 It is used in the dicom_echo func in Class Devices."""
tags = tag_dict.dictlist


def label(self, text,  row, column, font=None, pady=None, sticky=None, columnspan=None):
    _l = tk.Label(self, text=text, bg='gray16', fg='alice blue', font=font)
    _l.grid(row=row, column=column, pady=pady, sticky=sticky, columnspan=columnspan)


def button(self, text, command, row, column, sticky=None, pady=None):
    _b = tk.Button(self, text=text, command=command, bg='gray14', fg='darkorange1')
    _b.grid(row=row, column=column, sticky=sticky, pady=pady)


class Devices(tk.Toplevel):
    """This class handles the Add/Remove Devices view thats populated from the Menubar in the Main View.py file.
    Notes: device_added func is attached to the Add Device button. It checks that no entry fields are blank and then
        passes them to SQL.add_device func located in the SQL.py file.
    Notes: refresh_w func destroys and then opens the Devices window. Poor mans refresh. Its called in both device_added
        and the get_item funcs
    Notes: dicom_echo func is bound to the Dicom Echo button. It calls the dicom echo func from the DICOM_Utils.py file.
        It also calls the check func which checks to see what label to display based on results returned from the DICOM
        Echo func in DICOM_Utils.py. It may be redundantly called. Something I will need to review.
    Notes: The init builds the window and calls the widgets and tree funcs to build.
    Notes: setup_widgets is what builds the list box as well as other various labels and buttons on the page.
    Notes: build_tree handles building the columns/rows. The important thing is that it calls c_headers and SQL.get_list
        which populate the headers and the list of devices in the SQL DB table.
    Notes: get_item should more accurately call remove_device. It calls SQL.remove_device from the SQL.py file.
        Its attached to the remove device button.  It was named get_item because initially handled just getting what
        row was selected. Too late to go back now.
    """

    def device_added(self):
        print('test2')
        SQL.add_device(self.entry_name.get(),self.entry_ip.get(), self.entry_port.get(), self.entry_ae.get()
                       , self.entry_threads.get())
        self.refresh_w()

    def refresh_w(self):
        Devices.destroy(self)
        Devices()

    def dicom_echo(self):
        print('DICOM Echo')
        curItem = self.tree.focus()
        dict = self.tree.item(curItem)
        row = ''.join('{}'.format(val) for val in dict.items())
        row_l = (row.split(', ['))
        row_ls = row_l[1]
        new_row_ls = (row_ls.split(','))
        _ip = new_row_ls[2].replace(' ', '')
        ip = _ip.replace("'", '')
        port = int(new_row_ls[3].replace(' ', ''))
        self.dcm = DICOM_Utils.dcm_echo(ip, port)
        self.check()

    def check(self):
        print('checking')
        if str(self.dcm) == 'association':
            print('assoc')
            label(self, '***PORT IS OPEN BUT DICOM ASSOCIATION FAILED***', 7, 2, sticky=tk.W, columnspan=2)
        elif str(self.dcm) == 'port':
            print('port')
            label(self, '***PORT IS BLOCKED BUT YOU CAN PING IP***', 7, 2, sticky=tk.W, columnspan=2)
        elif str(self.dcm) == 'ping':
            print('ping')
            label(self, '***COULD NOT PING IP***', 7, 2, sticky=tk.W, columnspan=2)
        elif str(self.dcm) == 'success':
            print('success')
            label(self, '***SUCCESS***', 7, 2, sticky=tk.W, columnspan=2)

    def __init__(self):
        tk.Toplevel.__init__(self)

        self.configure(bg='gray16')
        self.geometry('950x525')
        self.tree = None
        self._setup_widgets()
        self._build_tree()
        label(self, 'Devices :', 0, 2, font=('', 14), sticky=tk.W)
        label(self, 'Add New Device', 3, 2, font=('', 14), sticky=tk.W)

    def _setup_widgets(self):
        # create a treeview with scrollbar
        container = ttk.Frame(self)

        self.tree = ttk.Treeview(self, columns=c_headers, show='headings')
        vsb = ttk.Scrollbar(self, orient='vertical', command=self.tree.yview)

        self.tree.configure(yscrollcommand=vsb.set)
        self.tree.grid(row=2, column=1, columnspan=2)
        vsb.grid(row=2, column=3, sticky=tk.W + tk.N + tk.S)

        container.grid_columnconfigure(0, weight=1)
        container.grid_rowconfigure(0, weight=1)
        label(self, 'AE:', 4, 0, pady=10, sticky=tk.E)
        label(self, 'IP/Path:', 5, 0, sticky=tk.E, pady=10)
        label(self, 'Port:', 6, 0, sticky=tk.E, pady=10)
        label(self, 'Device Name:', 7, 0, sticky=tk.E, pady=10)
        label(self, 'Threads:', 8, 0, sticky=tk.E, pady=10)

        self.entry_ae = tk.Entry(self, bg='gray14', fg='alice blue', bd=2)
        self.entry_ae.grid(row=4, column=1, sticky=tk.W, pady=10)
        self.entry_ip = tk.Entry(self, bg='gray14', fg='alice blue', bd=2)
        self.entry_ip.grid(row=5, column=1, sticky=tk.W, pady=10)
        self.entry_port = tk.Entry(self, bg='gray14', fg='alice blue', bd=2)
        self.entry_port.grid(row=6, column=1, sticky=tk.W, pady=10)
        self.entry_name = tk.Entry(self, bg='gray14', fg='alice blue', bd=2)
        self.entry_name.grid(row=7, column=1, sticky=tk.W, pady=10)
        self.entry_threads = tk.Entry(self, bg='gray14', fg='alice blue', bd=2)
        self.entry_threads.grid(row=8, column=1, sticky=tk.W, pady=10)

        button(self, 'Add Device', self.device_added, 4, 2, sticky=tk.W)
        button(self, 'Remove Device', self.get_item, 6, 2, sticky=tk.W)
        button(self, 'DICOM Echo', self.dicom_echo, 5, 2, sticky=tk.W)

    def _build_tree(self):
        for col in c_headers:
            self.tree.heading(col, text=col.title())
            # adjust the columns width to the header string
            self.tree.column(col, width=tkFont.Font().measure(col.title()))

        for item in SQL.get_list():
            print(self.tree.insert('', 'end', values=item))
            # adjust columns width if necessary to fit each value
            for ix, val in enumerate(item):
                col_w = tkFont.Font().measure(val)
                if self.tree.column(c_headers[ix], width=130): # <col_w:
                    self.tree.column(c_headers[ix], width=col_w)

    def get_item(self):
        curItem = self.tree.focus()
        dict = self.tree.item(curItem)
        row = ''.join('{}'.format(val) for val in dict.items())
        row_l = (row.split(', ['))
        row_ls = row_l[1]
        new_row_ls = (row_ls.split(','))
        row_id = new_row_ls[0]
        SQL.remove_device(row_id)
        self.refresh_w()


c_headers = ['ID', 'Name', 'IP', 'Port', 'AE', 'Threads']


class Rules(tk.Toplevel):
    """As of right now this just makes a blank window"""
    def __init__(self, *args, **kwargs):
        tk.Toplevel.__init__(self, *args, **kwargs)
        self.title('Activate/Remove Rules')
        self.geometry('800x450')
        self.configure(bg='gray16')
        self.tree = None
        self._setup_widgets()
        self._build_tree()
        SQL.get_rules()
        label(self, 'Rules:', 0, 2, sticky=tk.W, font=('', 14))

    def _setup_widgets(self):
        # create a treeview with scorllbar
        container = ttk.Frame(self)

        self.tree = ttk.Treeview(self, columns=a_headers, show='headings')
        vsb = ttk.Scrollbar(self, orient='vertical', command=self.tree.yview)

        self.tree.configure(yscrollcommand=vsb.set)
        self.tree.grid(row=2, column=1, columnspan=2)
        vsb.grid(row=2, column=3, sticky=tk.W + tk.N + tk.S)

        container.grid_columnconfigure(0, weight=1)
        container.grid_rowconfigure(0, weight=1)

        button(self, 'Activate', self.activate_rule, 3, 2, pady=15, sticky=tk.W)
        button(self, 'Deactivate', self.deactivate_rule, 4, 2, pady=15, sticky=tk.W)
        button(self, 'Delete', self.remove_rule, 5, 2, pady=15, sticky=tk.W)

    def _build_tree(self):
        for col in a_headers:
            self.tree.heading(col, text=col.title())
            # adjust the columns width to the header string
            self.tree.column(col, width=tkFont.Font().measure(col.title()))

        for item in SQL.get_rules():
            print(self.tree.insert('', 'end', values=item))
            # adjust columns width if necessary to fit each value
            for ix, val in enumerate(item):
                col_w = tkFont.Font().measure(val)
                if self.tree.column(a_headers[ix], width=130):
                    self.tree.column(a_headers[ix], width=col_w)

    def remove_rule(self):
        curItem = self.tree.focus()
        dict = self.tree.item(curItem)
        row = ''.join('{}'.format(val) for val in dict.items())
        row_l = (row.split(', ['))
        row_ls = row_l[1]
        new_row_ls = (row_ls.split(','))
        row_id = new_row_ls[0]
        SQL.remove_rule(row_id)
        self.refresh_w()

    def activate_rule(self):
        curItem = self.tree.focus()
        dict = self.tree.item(curItem)
        row = ''.join('{}'.format(val) for val in dict.items())
        row_l = (row.split(', ['))
        row_ls = row_l[1]
        new_row_ls = (row_ls.split(','))
        row_id = new_row_ls[0]
        SQL.activate_rule(row_id)
        self.refresh_w()

    def deactivate_rule(self):
        curItem = self.tree.focus()
        dict = self.tree.item(curItem)
        row = ''.join('{}'.format(val) for val in dict.items())
        row_l = (row.split(', ['))
        row_ls = row_l[1]
        new_row_ls = (row_ls.split(','))
        row_id = new_row_ls[0]
        SQL.deactivate_rule(row_id)
        self.refresh_w()

    def refresh_w(self):
        Rules.destroy(self)
        Rules()


a_headers = ['ID', 'Source', 'Rule', 'Destination', 'Active', 'Anony']


class BuildRules(tk.Toplevel):
    """ This is a view that the user uses to build a new rule."""
    def __init__(self, *args, **kwargs):
        tk.Toplevel.__init__(self, *args, **kwargs)
        self.title('Active Rules')
        self.geometry('1208x500')
        self.configure(bg='gray16')

        label(self, 'Build Rule:', 0, 2, font=('', 20), pady=20)
        label(self, 'Pick a Source', 1, 0, pady=10, font=('', 12))
        label(self, 'Pick a Destination', 1, 4, pady=10, font=('', 12))
        label(self, 'Options', 3, 1, pady=10, font=('', 12))
        label(self, 'Operators', 3, 2, pady=10, font=('', 12))
        label(self, 'Criteria', 3, 3, font=('', 12))

        self.entry_criteria = tk.Entry(self, bg='gray14', fg='alice blue', width=25)
        self.entry_criteria.grid(row=4, column=3)

        self.button_add_rule = tk.Button(self, text='Add Rule', bg='gray14', fg='darkorange1', command=self.get_rules)
        self.button_add_rule.grid(row=7, column=2, pady=15)

        self.butt_anony = tk.IntVar()
        self.button_anonymize = tk.Checkbutton(self, text='Anonymize ?', variable=self.butt_anony,
                                               bg='gray16', fg='dodger blue')
        self.button_anonymize.grid(row=5, column=2, pady=10)

        self.butt_active = tk.IntVar()
        self.button_active = tk.Checkbutton(self, text='Make Active ?', variable=self.butt_active,
                                            bg='gray16', fg='dodger blue')
        self.button_active.grid(row=6, column=2, pady=10)

        options = SQL.get_list()
        self.strvs = tk.StringVar()
        self.strvs.set(options[0])
        self.option_sources = tk.OptionMenu(self, self.strvs, *options)
        self.option_sources.grid(row=2, column=0, pady=0)
        self.option_sources.config(width=50, bg='gray14', fg='alice blue', relief=tk.GROOVE)

        options = SQL.get_list()
        self.strvd = tk.StringVar()
        self.strvd.set(options[0])
        self.option_destination = tk.OptionMenu(self, self.strvd, *options)
        self.option_destination.grid(row=2, column=4, pady=0)
        self.option_destination.config(width=50, bg='gray14', fg='alice blue', relief=tk.GROOVE)

        options = list(tags)
        self.strvopt = tk.StringVar()
        self.strvopt.set(options[0])
        self.option_options = tk.OptionMenu(self, self.strvopt, *options)
        self.option_options.grid(row=4, column=1, pady=0)
        self.option_options.config(width=30, bg='gray14', fg='alice blue', relief=tk.GROOVE)

        options = ['=', '!=', 'Contains', 'Not Contains', '<>', '<', '>', '>=', '<=']
        self.strvops = tk.StringVar()
        self.strvops.set(options[0])
        self.option_operators = tk.OptionMenu(self, self.strvops, *options)
        self.option_operators.grid(row=4, column=2, pady=0)
        self.option_operators.config(width=12, bg='gray14', fg='alice blue', relief=tk.GROOVE)

    def get_rules(self):
        sour = (self.strvs.get()).split(',')
        _sour = (sour[2].replace(' ', '').replace("'", ''))
        dest = (self.strvd.get()).split(',')
        #_dest is the destination IP
        _dest = (dest[2].replace(' ', '').replace("'", ''))
        opt = (self.strvopt.get()).split(',')
        # _opt is the options stripped down.
        _opt = (opt[1].replace(' ', '')).replace(')', '').replace("'", '')
        operator = self.strvops.get()
        criteria = self.entry_criteria.get()
        active = self.butt_active.get()
        anony = self.butt_anony.get()
        rule = [_opt, operator, criteria]
        _rule = (','.join(rule)).replace('[]', '').replace("'", '')
        SQL.add_rules(_sour, _rule, _dest, active, anony)


class DSTConfig(tk.Toplevel):
    """ Handles view for the anonymize window when its seleceted from the menubar"""
    def __init__(self, *args, **kwargs):
        tk.Toplevel.__init__(self, *args, **kwargs)

        anon_list = SQL.anony_config()

        self.title('Active Rules')
        self.geometry('230x300')
        self.configure(bg='gray16')

        label(self, 'DSTools Configurator', 0, 0, font=('', 17), pady=12)
        label(self, 'Local AE: ', 7, 0, font=('', 12), pady=10)
        label(self, 'Local Port:', 9, 0, font=('', 12), pady=10)
        label(self, 'Local Max Threads:', 11, 0, font=('', 12), pady=10)

        self.entry_localae = tk.Entry(self, bg='gray14', fg='alice blue', width='20')
        self.entry_localae.insert(0, anon_list[0])
        self.entry_localae.grid(row=8, column=0, pady=0)
        self.entry_localport = tk.Entry(self, bg='gray14', fg='alice blue', width=15)
        self.entry_localport.insert(0, anon_list[2])
        self.entry_localport.grid(row=10, column=0, pady=0)
        self.entry_local_threads = tk.Entry(self, bg='gray14', fg='alice blue', width=10)
        self.entry_local_threads.insert(0, anon_list[1])
        self.entry_local_threads.grid(row=12, column=0, pady=0)

        button(self, 'UPDATE', self.get_destination, 13, 0, pady=25)

    def get_destination(self):
        """ Should be named get info from entrys and pass to SQL.anony config to update DB table' but that seemed a bit
        much."""
        SQL.update_anony_config(self.entry_localae.get(), self.entry_localport.get(), self.entry_local_threads.get())
        Anonymize.destroy(self)
