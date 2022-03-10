import subprocess

class Command:
    def run(self, cmd):
        try:
            # print(cmd)
            subprocess.run(cmd, check=True, shell=True, capture_output=True).check_returncode()
            return (True, '')
        except subprocess.SubprocessError as e:
            return (False, str(e.stderr, 'utf-8'))