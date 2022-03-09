import re
import subprocess

class Command:
    def __init__(self, cmd):
        self.cmd = cmd

    def run(self):
        try:
            print(self.cmd)
            subprocess.run(self.cmd, check=True, shell=True, capture_output=True).check_returncode()
            return (True, '')
        except subprocess.SubprocessError as e:
            return (False, str(e.stderr, 'utf-8'))