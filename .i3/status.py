#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from multiprocessing import cpu_count
from Xlib import display
from Xlib.ext import randr
import netifaces as net
import json
import os

from keyring.backends.SecretService import Keyring

from i3pystatus import Status, Module, IntervalModule


CONFIG_FILE = f"{os.environ['HOME']}/.i3/status.conf.json"


def get_screen_count():
    disp = display.Display()
    scr = disp.screen()
    win = scr.root.create_window(0, 0, 1, 1, 1, scr.root_depth)
    return len(randr.get_screen_resources(win).outputs)

def get_eth_devs():
    return [ n for n in net.interfaces() if \
                                n != 'lo' and \
                                net.AF_LINK in net.ifaddresses(n) ]

def get_wifi_devs():
    try:
        from wireless import Wireless
        w = Wireless()
        return w.interfaces()
    except:
        return []


class RestartReminder(IntervalModule):
    settings = required = ()

    def run(self):
        if os.path.exists("/lib/modules/" + os.uname().release):
            self.output = None
        else:
            self.output = {
                "full_text": "Reboot required!",
                "color": "#FF3333",
            }


class ShutdownButton(Module):
    output = {
        "full_text": "\uF3A9",
    }
    def on_leftclick(self):
        import subprocess
        subprocess.Popen(["dmenu_runstate"])


class Config:
    def __init__(self, json_config_file, layout):
        self.entities, self.config = \
                self.load_conf(json_config_file, layout)

    def load_conf(self, filename, layout):
        with open(filename) as data_file:
            data = json.load(data_file)
        return (data["layouts"][layout], data["config"])


class Entity:
    def __init__(self, bar, etype, conf):
        self.bar = bar
        self.etype = etype
        try:
            self.conf = conf[etype]
        except KeyError:
            self.conf = {}

    def update(self, data):
        self.etype.update(data)

    def register(self):
        self.bar.register(self.etype, **self.conf)


class Bar:
    def __init__(self, conf, layout):
        self.conf = conf
        self.entities = []

        self.bar = Status(standalone=True)

        self.bar.register(RestartReminder())
        self.bar.register(ShutdownButton())

        def gen_ent(e, itr):
            for i in itr:
                ent = Entity(self.bar, e, conf.config)
                ent.update({"interface": i})
                self.entities.append(ent)

        for e in conf.entities:
            if e.startswith('network'):
                gen_ent(e, get_eth_devs())
            elif e == 'wireless':
                gen_ent(e, get_wifi_devs())
            else:
                self.entities.append(Entity(self.bar, e, conf.config))

    def run(self):
        [ e.register() for e in self.entities ]
        self.bar.run()


if __name__ == "__main__":
    import sys
    try:
        layout = sys.argv[1]
    except IndexError:
        raise ValueError("Please supply the layout as the only argument.")

    c = Config(CONFIG_FILE, layout)
    b = Bar(c, layout)
    b.run()

