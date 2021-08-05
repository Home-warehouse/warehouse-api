import json


class integration:
    '''Boilerplate class for all integrations'''
    def __init__(self, config):
        self.config = json.loads(config)

    def raport(self):
        ...

    def product(self):
        ...

    def location(self):
        ...
