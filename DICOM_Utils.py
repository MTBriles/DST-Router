from pynetdicom3 import AE
from pynetdicom3.sop_class import VerificationSOPClass
import tkinter as tk
import os
import socket

ip1 = "10.232.200.22"
port = 11112
retry = 5
delay = 10
timeout = 3


class DICOMEcho(tk.Toplevel):

    def __init__(self, *args, **kwargs):
        tk.Toplevel.__init__(self, *args, **kwargs)

        ae = AE()
        ae.add_requested_context(VerificationSOPClass)
        # Associate with the peer at IP address and Port
        assoc = ae.associate(ip1, port)
        if assoc.is_established:
            status = assoc.send_c_echo()

            # Output the response from the peer
            if status:
                self.title('Connection SUCCESS')
                self.geometry('400x200')
                self.configure(bg='gray16')
                self.resizable(False, False)
                self.label_status = tk.Label(self, text='C-ECHO Response: 0x{0:04x}'.format(status.Status), bg='gray16', fg='GREEN', font=('', 12))
                self.label_status.pack(pady=15)
                # Do something with the association
                pass
                # Once we are finished, release the association
                assoc.release()
        elif assoc.is_rejected or assoc.is_aborted:
            var = 'ping ' + ip1

            if os.system(var) == 0:

                def isOpen(ip1, port):
                    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    s.settimeout(timeout)
                    try:
                        s.connect((ip1, int(port)))
                        s.shutdown(socket.SHUT_RDWR)
                        return True
                    except:
                        return False
                    finally:
                        s.close()

                if isOpen(ip1, port):
                    self.title('Connection FAILED')
                    self.geometry('400x100')
                    self.configure(bg='gray16')
                    self.resizable(False, False)
                    self.label_status = tk.Label(self, text='PORT IS OPEN BUT DICOM ASSOCIATION FAILED', bg='gray16', fg='RED', font=('', 12))
                    self.label_status.pack(pady=15)
                else:
                    self.title('Connection FAILED')
                    self.geometry('400x100')
                    self.configure(bg='gray16')
                    self.resizable(False, False)
                    self.label_status = tk.Label(self, text='PORT IS BLOCKED BUT YOU CAN PING THE IP', bg='gray16', fg='RED', font=('', 12))
                    self.label_status.pack(pady=15)
            else:
                self.title('Connection FAILED')
                self.geometry('200x100')
                self.configure(bg='gray16')
                self.resizable(False, False)
                self.label_status = tk.Label(self, text='COULD NOT PING IP', bg='gray16', fg='RED', font=('', 12))
                self.label_status.pack(pady=15)

