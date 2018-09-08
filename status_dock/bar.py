# -*- coding: utf-8 -*-

from multiprocessing import cpu_count
from Xlib import display
from Xlib.ext import randr
import netifaces as net
import json
import os
import re

from keyring.backends.SecretService import Keyring

from i3pystatus import Status, Module, IntervalModule

from status_dock.util import snake2camel
from status_dock import modules


class Config:
    def __init__(self, json_config_file, layout):
        self.entities, self.config = \
                self.load_conf(json_config_file, layout)

    def load_conf(self, filename, layout):
        with open(filename, encoding='utf-8') as data_file:
            data = json.load(data_file)
        return (data["layouts"][layout], data["config"])


class ModFacade:
    def __init__(self, etype, conf):
        self.mod = getattr(modules, snake2camel(etype))(conf)

    def get_mods(self):
        #print(self.mod)
        if hasattr(self.mod, '__iter__'):
            return self.mod._list
        else:
            return [self.mod]


class Bar:
    def __init__(self, conf_file, layout):
        self.conf = Config(conf_file, layout)
        self.entities = []
        self.bar = Status(standalone=True)

        for e in self.conf.entities:
            self.entities.append(ModFacade(e, self.conf.config))

    def run(self):
        for ent in self.entities:
            [ m.register(self.bar) for m in ent.get_mods() ]
        self.bar.run()
