import os
import tkinter as tk
import win32serviceutil
import psutil

currentpath2 = r'%s' % os.getcwd().replace('\\', '/')
currentpath = (currentpath2 + '/')
exefile = str(currentpath + 'nssm.exe')


class service_control(tk.Toplevel):

    def createservice():
        installservice = (exefile+' install DSTools_Router '+currentpath+'DSTools_Router.exe')
        os.system(installservice)

    def stopservice():
        stopservice = (exefile + ' stop DSTools_Router')
        os.system(stopservice)

    def removeservice():
        removeservice = (exefile + ' remove DSTools_Router')
        os.system(removeservice)

    def startservice():
        startservice = (exefile + ' start DSTools_Router')
        os.system(startservice)

    def checkservice():
        try:
            service = psutil.win_service_get('DSTools_Router')
            service = service.as_dict()
        except Exception as ex:
            print('did not work', str(ex))
            return 'Not_Installed'

        if service:
            if service['status'] == 'running':
                print('service running')
                return 'Running'
            else:
                print('service not started')
                return 'Stopped'
        else:
            print('service not found')
            return 'Not_Installed'








