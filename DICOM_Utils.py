from pynetdicom3 import AE
from pynetdicom3.sop_class import VerificationSOPClass
import tkinter as tk
import os
import socket


def dcm_echo(ip, port):
    _ip = ip
    _port = port
    print('working')
    ae = AE(ae_title='DSTools', port=104)
    ae.add_requested_context(VerificationSOPClass)
    # Associate with the peer at IP address and Port
    assoc = ae.associate(_ip, _port)
    if assoc.is_established:
        string = 'success'
        assoc.release()
        print('success')
    else:
        var = 'ping ' + _ip
        if os.system(var) == 0:
            print('pinging')

            def isOpen(_ip, _port):
                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                s.settimeout(3)
                try:
                    s.connect((_ip, int(_port)))
                    s.shutdown(socket.SHUT_RDWR)
                    return True
                except:
                    return False
                finally:
                    s.close()

            if isOpen(_ip, _port):
                print('association')
                string = 'association'
            else:
                print('port')
                string = 'port'
        else:
            print('ping')
            string = 'ping'

    return string


