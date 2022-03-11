import subprocess

class Command:
    def run(self, cmd):
        try:
            # print(cmd)
            subprocess.run(cmd, check=True, shell=True, stderr=subprocess.PIPE).check_returncode()
            return (True, '')
        except subprocess.SubprocessError as e:
            return (False, str(e.stderr, 'utf-8'))


def main():
    print('test...')
    cmd = Command()

    ok, msg = cmd.run('ls -al')
    if not ok:
        print(msg)

    ok, msg = cmd.run('ls aaa')
    if not ok:
        print(msg)

if __name__ == '__main__':
    main()