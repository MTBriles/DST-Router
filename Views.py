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

""" Takes the DICOMEcho class from DICOM_Utiles.py file and assigns it to a global var here in the Views.py.  
 It is used in the dicom_echo func in Class Devices."""
dcm_util = DICOM_Utils.DICOMEcho


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
    Notes: get_item is more accurately call remove_device. It calls SQL.remove_device from the SQL.py file.
        Its attached to the remove device button.  It was named get_item because initially handled just getting what
        row was selected. Too late to go back now.
    """

    def device_added(self):
        print('test2')
        ae = ()
        ip = ()
        name = ()
        port = ()
        threads = ()
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
        if len(self.entry_threads.get()) == 0:
            self.label_blank_threads.grid(row=7, column=2, sticky=tk.W, columnspan=2)
        else:
            threads = self.entry_threads.get()
        SQL.add_device(name, ip, port, ae, threads)
        self.label_device_added.grid(row=7, column=2)
        self.refresh_w()

    def refresh_w(self):
        Devices.destroy(self)
        Devices()

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

        self.label_thread = tk.Label(self, text='Threads:', bg='gray16', fg='alice blue')
        self.label_thread.grid(row=8, column=0, sticky=tk.E, pady=10)

        self.entry_threads = tk.Entry(self, bg='gray14', fg='alice blue', bd=2)
        self.entry_threads.grid(row=8, column=1, sticky=tk.W, pady=10)

        self.button_add_source = tk.Button(self, text='ADD Device', bg='gray14',
                                           fg='darkorange1', command=self.device_added)
        self.button_add_source.grid(row=4, column=2, sticky=tk.W)

        self.button_remove_source = tk.Button(self, text='Remove Device', bg='gray14', fg='darkorange1', command=self.get_item)
        self.button_remove_source.grid(row=6, column=2, sticky=tk.W)

        self.button_echo = tk.Button(self, text='DICOM ECHO', bg='gray14', fg='darkorange1', command=self.dicom_echo)
        self.button_echo.grid(row=5, column=2, sticky=tk.W)

        self.label_device_added = tk.Label(self, text='Device Added!', bg='gray16', fg='red')

        self.label_device_removed = tk.Label(self, text='Device Removed!', bg='gray16', fg='red')

        self.label_association_fail = tk.Label(self, text='PORT IS OPEN BUT DICOM ASSOCIATION FAILED', bg='gray16',
                                               fg='RED')

        self.label_port_fail = tk.Label(self, text='PORT IS BLOCKED BUT YOU CAN PING THE IP', bg='gray16', fg='RED')

        self.label_ping_fail = tk.Label(self, text='COULD NOT PING IP', bg='gray16', fg='RED')

        self.label_echo_success = tk.Label(self, text='SUCCESS', bg='gray16', fg='GREEN')

        self.label_blank_ae = tk.Label(self, text='***AE cannot have NULL Value***', bg='gray16', fg='red')
        self.label_blank_port = tk.Label(self, text='***PORT cannot have NULL Value***', bg='gray16', fg='red')
        self.label_blank_ip = tk.Label(self, text='***IP cannot have NULL Value***', bg='gray16', fg='red')
        self.label_blank_name = tk.Label(self, text='***Device Name cannot have NULL Value***', bg='gray16', fg='red')
        self.label_blank_threads = tk.Label(self, text='***Threads cannot have NULL Value***', bg='gray16', fg='red')


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
        self.label_device_removed.grid(row=7, column=2)
        self.refresh_w()


c_headers = ['ID', 'Name', 'IP', 'Port', 'AE', 'Threads']


class Rules(tk.Toplevel):
    """As of right now this just makes a blank window"""
    def __init__(self, *args, **kwargs):
        tk.Toplevel.__init__(self, *args, **kwargs)
        self.title('Add/Remove Rules')
        self.geometry('950x525')
        self.configure(bg='gray16')
        self.tree = None
        self._setup_widgets()
        self._build_tree()

        self.label_sources = tk.Label(self, text=('Rules' + ' :'), bg='gray16', fg='alice blue', font=('', 14))
        self.label_sources.grid(row=0, column=2, sticky=tk.W)

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

        self.button_activate = tk.Button(self, text='Activate', bg='gray14', fg='darkorange1')
        self.button_activate.grid(row=3, column=2, pady=15, sticky=tk.W)
        self.button_deactivate = tk.Button(self, text='Deactivate', bg='gray14', fg='darkorange1')
        self.button_deactivate.grid(row=4, column=2, pady=15, sticky=tk.W)
        self.button_delete = tk.Button(self, text='Delete', bg='gray14', fg='darkorange1')
        self.button_delete.grid(row=5, column=2, pady=15, sticky=tk.W)


    def _build_tree(self):
        for col in a_headers:
            self.tree.heading(col, text=col.title())
            # adjust the columns width to the header string
            self.tree.column(col, width=tkFont.Font().measure(col.title()))

        for item in rules:
            print(self.tree.insert('', 'end', values=item))
            # adjust columns width if necessary to fit each value
            for ix, val in enumerate(item):
                col_w = tkFont.Font().measure(val)
                if self.tree.column(a_headers[ix], width=130):
                    self.tree.column(a_headers[ix], width=col_w)


a_headers = ['ID', 'Source', 'Rule', 'Destination', 'Active']
rules = [('TestID', 'Test Source', 'Trule', 'TDestination', 'False')]


class BuildRules(tk.Toplevel):
    """ This is a view that the user uses to build a new rule."""
    def __init__(self, *args, **kwargs):
        tk.Toplevel.__init__(self, *args, **kwargs)
        self.title('Active Rules')
        self.geometry('1087x500')
        self.configure(bg='gray16')

        self.label_build = tk.Label(self, text='Build Rule:', bg='gray16', fg='alice blue', font=('', 20))
        self.label_build.grid(row=0, column=2, pady=20)
        self.label_sources = tk.Label(self, text='Pick a Source', bg='gray16', fg='alice blue', font=('', 12))
        self.label_sources.grid(row=1, column=0, pady=10)
        self.label_destination = tk.Label(self, text='Pick a Destination', bg='gray16', fg='alice blue', font=('', 12))
        self.label_destination.grid(row=1, column=4, pady=10)
        self.label_options = tk.Label(self, text='Options', bg='gray16', fg='alice blue', font=('', 12))
        self.label_options.grid(row=3, column=1, pady=10)
        self.label_operators = tk.Label(self, text='Operators', bg='gray16', fg='alice blue', font=('', 12))
        self.label_operators.grid(row=3, column=2, pady=10)
        self.label_criteria = tk.Label(self, text='Criteria', bg='gray16', fg='alice blue', font=('', 12))
        self.label_criteria.grid(row=3, column=3)

        self.entry_criteria = tk.Entry(self, bg='gray14', fg='alice blue', width=25)
        self.entry_criteria.grid(row=4, column=3)

        self.button_add_rule = tk.Button(self, text='Add Rule', bg='gray14', fg='darkorange1')
        self.button_add_rule.grid(row=7, column=2, pady=15)

        self.button_anonymize = tk.Checkbutton(self, text='Anonymize ?', bg='gray16', fg='dodger blue')
        self.button_anonymize.grid(row=5, column=2, pady=10)

        self.button_active = tk.Checkbutton(self, text='Make Active ?', bg='gray16', fg='dodger blue')
        self.button_active.grid(row=6, column=2, pady=10)

        options = SQL.get_list()
        self.strv = tk.StringVar()
        self.strv.set(options[0])
        self.option_sources = tk.OptionMenu(self, self.strv, *options)
        self.option_sources.grid(row=2, column=0, pady=0)
        self.option_sources.config(width=50, bg='gray14', fg='alice blue', relief=tk.GROOVE)

        options = SQL.get_list()
        self.strv = tk.StringVar()
        self.strv.set(options[0])
        self.option_destination = tk.OptionMenu(self, self.strv, *options)
        self.option_destination.grid(row=2, column=4, pady=0)
        self.option_destination.config(width=50, bg='gray14', fg='alice blue', relief=tk.GROOVE)

        options = ['Modality', 'Other Stuff']
        self.strv = tk.StringVar()
        self.strv.set(options[0])
        self.option_options = tk.OptionMenu(self, self.strv, *options)
        self.option_options.grid(row=4, column=1, pady=0)
        self.option_options.config(width=10, bg='gray14', fg='alice blue', relief=tk.GROOVE)

        options = ['=', '!=']
        self.strv = tk.StringVar()
        self.strv.set(options[0])
        self.option_operators = tk.OptionMenu(self, self.strv, *options)
        self.option_operators.grid(row=4, column=2, pady=0)
        self.option_operators.config(width=5, bg='gray14', fg='alice blue', relief=tk.GROOVE)


class Anonymize(tk.Toplevel):
    """ Handles view for the anonymize window when its seleceted from the menubar"""
    def __init__(self, *args, **kwargs):
        tk.Toplevel.__init__(self, *args, **kwargs)

        anon_list = SQL.anony_config()

        self.title('Active Rules')
        self.geometry('345x600')
        self.configure(bg='gray16')

        self.label_anon_header = tk.Label(self, text='Anonymize Configurator', bg='gray16', fg='alice blue',
                                          font=('', 17))
        self.label_anon_header.grid(row=0, column=0, pady=12)

        self.label_select_device = tk.Label(self, text='Select Device: ', bg='gray16', fg='alice blue', font=('', 14))
        self.label_select_device.grid(row=1, column=0, pady=10)

        options = SQL.get_list()
        self.strv = tk.StringVar()
        self.strv.set(options[0])
        self.option_destination = tk.OptionMenu(self, self.strv, *options)
        self.option_destination.grid(row=2, column=0, pady=0)
        self.option_destination.config(width=50, bg='gray14', fg='alice blue', relief=tk.GROOVE)

        self.label_sendtodir = tk.Label(self, text='Send to Directory?', bg='gray16', fg='alice blue', font=('', 14))
        self.label_sendtodir.grid(row=3, column=0, pady=10)

        tf_options = ['True', 'False']
        self.str = tk.StringVar()
        self.str.set(tf_options[0])
        self.tf_options = tk.OptionMenu(self, self.str, *tf_options)
        self.tf_options.grid(row=4, column=0, pady=0)
        self.tf_options.config(width=30, bg='gray14', fg='alice blue', relief=tk.GROOVE)

        self.label_dirpath = tk.Label(self, text='Directory Path: ', bg='gray16', fg='alice blue', font=('', 12))
        self.label_dirpath.grid(row=5, column=0, pady=10)
        self.entry_dirpath = tk.Entry(self, bg='gray14', fg='alice blue', width='30')
        self.entry_dirpath.insert(0, anon_list[4])
        self.entry_dirpath.grid(row=6, column=0, pady=0)

        self.label_localae = tk.Label(self, text='Local AE: ', bg='gray16', fg='alice blue', font=('', 12))
        self.label_localae.grid(row=7, column=0, pady=10)
        self.entry_localae = tk.Entry(self, bg='gray14', fg='alice blue', width='20')
        self.entry_localae.insert(0, anon_list[5])
        self.entry_localae.grid(row=8, column=0, pady=0)

        self.label_localport = tk.Label(self, text='Local Port:', bg='gray16', fg='alice blue', font=('', 12))
        self.label_localport.grid(row=9, column=0, pady=10)
        self.entry_localport = tk.Entry(self, bg='gray14', fg='alice blue', width=15)
        self.entry_localport.insert(0, anon_list[1])
        self.entry_localport.grid(row=10, column=0, pady=0)

        self.label_local_threads = tk.Label(self, text='Local Max Threads:', bg='gray16', fg='alice blue', font=('', 12))
        self.label_local_threads.grid(row=11, column=0, pady=10)
        self.entry_local_threads = tk.Entry(self, bg='gray14', fg='alice blue', width=10)
        self.entry_local_threads.insert(0, anon_list[6])
        self.entry_local_threads.grid(row=12, column=0, pady=0)

        self.button_update = tk.Button(self, text='UPDATE', bg='gray14', fg='darkorange1', command=self.get_destination)
        self.button_update.grid(row=13, column=0, pady=25)

    def get_destination(self):
        """ Should be named 'get info from entrys and pass to SQL.anony config to update DB table' but that seemed a bit
        much."""
        nw_dest = self.strv.get()
        nw_dir = self.str.get()
        nw_dpath = self.entry_dirpath.get()
        nw_l_ae = self.entry_localae.get()
        nw_l_port = self.entry_localport.get()
        nw_l_threads = self.entry_local_threads.get()
        dest_list = nw_dest.split(',')
        dest_port_1 = str(dest_list[3].replace(' ', ''))
        dest_port = dest_port_1.replace("'", '')
        dest_ip_1 = str(dest_list[2].replace(' ', ''))
        dest_ip = dest_ip_1.replace("'", '')
        dest_ae_1 = str(dest_list[1].replace(' ', ''))
        dest_ae = dest_ae_1.replace("'", '')

        print(nw_dir)

        SQL.update_anony_config(dest_port, dest_ip, dest_ae, nw_dir, nw_dpath, nw_l_ae, nw_l_port, nw_l_threads)

        Anonymize.destroy(self)
