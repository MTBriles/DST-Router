
import os
import sys
import psutil
import subprocess

import pysc


class anonyservice:


    def createservice():
        script_fullpath = os.path.realpath('Anonymize.exe')
        pysc.create(
        service_name='Anonymize',
        cmd=[sys.executable, script_fullpath]
        )

    def stopservice():
        s = psutil.win_service_get('Anonymize')
        p = str(s.pid())
        anonykillcmd = 'taskkill /f /pid ' + p
        subprocess.check_call(anonykillcmd)

    def removeservice():
        pysc.delete('Anonymize')

    def startservice():
        pysc.start('Anonymize')



