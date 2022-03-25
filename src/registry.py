from docker.cli import RegistryCli as cli
from docker.errors import RegistryError

class Registry:
    def __init__(self, cli):
        cli.ping()
        self.cli = cli

    def exist(self, image):
        [name, tag] = image.split(':')
        try:
            tags = self.cli.list_tags(name)
            if tags is None:
                return False
            for t in tags:
                if t == tag:
                    return True
        except RegistryError as e:
            # print(e)
            return False
        return False

def main():
    c = cli.RegistryCli('http://192.168.0.3:30500')
    c.ping()
    print(c.catalogs())
    print(c.list_tags('quay.io/opstree/redis'))
    print(c.list_tags('ghcr.io/dexidp/dex'))

    registry = Registry(c)
    if registry.exist('quay.io/kiali/kiali:v1.21'):
        print('exist')
    else:
        print('no exist')

    if registry.exist('ghcr.io/dexidp/dex:v2.30.2'):
        print('exist')
    else:
        print('no exist')


if __name__ == '__main__':
    main()
