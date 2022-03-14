import requests
import json
from . import errors

class RegistryCli:
    def __init__(self, url):
        self.url = url

    def ping(self):
        # Will raise exception: https://docs.python-requests.org/en/latest/user/quickstart/#errors-and-exceptions
        requests.get('{URL}/v2'.format(URL=self.url))

    def catalogs(self):
        response = requests.get('{URL}/v2/_catalog'.format(URL=self.url))
        content = json.loads(str(response.content, 'utf-8'))
        if content.get('errors'):
            raise errors.RegistryError(content)
        return content.get('repositories')

    def list_tags(self, image):
        response = requests.get('{URL}/v2/{NAME}/tags/list'.format(URL=self.url, NAME=image))
        content = json.loads(str(response.content, 'utf-8'))
        if content.get('errors'):
            raise errors.RegistryError(content)
        return content.get('tags')
