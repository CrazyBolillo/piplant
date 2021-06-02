import json

from dotmap import DotMap


class PiplantSettings:

    def __init__(self):
        self.settings = DotMap()

    def load(self, fp):
        self.settings = DotMap(json.load(fp))

    def __getattr__(self, item):
        return self.settings[item]


settings = PiplantSettings()
