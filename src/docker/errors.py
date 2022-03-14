class RegistryError(Exception):
    def __init__(self, response):
        self.code = response.get('errors')[0].get('code')
        self.msg = response.get('errors')[0].get('message')

    def __str__(self):
        return '[{CODE}]: {MSG}'.format(CODE=self.code, MSG=self.msg)