import re
import subprocess

class SkopeoUtil:
    CHECK = 'skopeo inspect docker://{IMAGE}'
    CRED_CHECK = 'skopeo inspect --creds={CRED} docker://{IMAGE}'
    COPY = 'skopeo copy --dest-tls-verify=false docker://{IMAGE} docker://{DEST}/{IMAGE}'
    CRED_COPY = 'skopeo copy --src-creds={CRED} --dest-tls-verify=false docker://{IMAGE} docker://{DEST}/{IMAGE}'

    def __init__(self, docker_cred, quay_cred, gcr_cred, copy_to):
        self.profiles = {
            'docker.io': {'pattern': re.compile('^[a-z0-9.]*docker.io/'), 'cred': docker_cred},
            'docker.elastic.co': {'pattern': re.compile('^docker.elastic.co/'), 'cred': ''},
            'public.ecr.aws': {'pattern': re.compile('^public.ecr.aws/'), 'cred': ''},
            'quay.io': {'pattern': re.compile('^[a-z0-9.]*quay.io/'), 'cred': quay_cred},
            'gcr': {'pattern': re.compile('^[a-z0-9.]*gcr.io/'), 'cred': gcr_cred}
        }
        self.copy_to = copy_to

    def inspect(self, name):
        cmd = self.CRED_CHECK.format(IMAGE=name, CRED=self.profiles['docker.io']['cred'])
        for profile in self.profiles.values():
            if profile['pattern'].search(name) != None:
                if profile['cred']:
                    cmd = self.CRED_CHECK.format(IMAGE=name, CRED=profile['cred'])
                else:
                    cmd = self.CHECK.format(IMAGE=name)
                break
        try:
            # print(cmd)
            subprocess.run(cmd, check=True, shell=True, capture_output=True).check_returncode()
            return (name, True, '')
        except subprocess.SubprocessError as e:
            return (name, False, str(e.stderr, 'utf-8'))

    def copy(self, name):
        cmd = self.CRED_COPY.format(IMAGE=name, CRED=self.profiles['docker.io']['cred'], DEST=self.copy_to)
        for profile in self.profiles.values():
            if profile['pattern'].search(name) != None:
                if profile['cred']:
                    cmd = self.CRED_COPY.format(IMAGE=name, CRED=profile['cred'], DEST=self.copy_to)
                else:
                    cmd = self.COPY.format(IMAGE=name, DEST=self.copy_to)
                break
        try:
            # print(cmd)
            subprocess.run(cmd, check=True, shell=True, capture_output=True).check_returncode()
            return (name, True, '')
        except subprocess.SubprocessError as e:
            return (name, False, str(e.stderr, 'utf-8'))