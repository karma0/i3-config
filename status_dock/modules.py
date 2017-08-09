# -*- coding: utf-8 -*-

from multiprocessing import cpu_count
import os
import subprocess

from i3pystatus import Module, IntervalModule

from status_dock.util import camel2snake, get_eth_devs, get_wifi_devs
from status_dock.entity import Entity, EntityFactory, ETypeMixin, \
                               NetTypeMixin, ModClassicMixin


#####
## i3pystatus Modules
###

class RestartReminder(IntervalModule, ETypeMixin, ModClassicMixin):
    etype = "restart_reminder"
    settings = required = ()

    def __init__(self, conf):
        try:
            self.conf = conf[self.etype]
        except KeyError:
            self.conf = {}

    def run(self):
        if os.path.exists("/lib/modules/" + os.uname().release):
            self.set_output(None)
        else:
            self.output = self.conf


class ShutdownButton(Module, ETypeMixin, ModClassicMixin):
    etype = "shutdown_button"

    def __init__(self, conf):
        try:
            self.output = conf[self.etype]
        except KeyError:
            self.output = {}

    def on_leftclick(self):
        subprocess.Popen([f"{os.environ['HOME']}/.i3/dmenu_runstate"])


#####
## Entity-type Modules
###

class Alsa(Entity): pass
class Battery(Entity): pass
class Clock(Entity): pass

class CpuUsageGraph(Entity):
    def __init__(self, *a, **kw):
        super().__init__(*a, **kw)
        fmt_str = "{cpu_graph}:"
        for c in range(cpu_count()):
            fmt_str += "{usage_cpu"+str(c)+":02},"
        self.conf.update({ "format": fmt_str[:-1] })

class Disk(Entity): pass
class Load(Entity): pass
class MemBar(Entity): pass

class Net(Entity):
    etype = "network"

class Network(EntityFactory, NetTypeMixin):
    etype = "network"
    def __init__(self, c):
        self.conf = c[self.etype] if self.etype in c else {}
        self.gen_ent(Net, get_eth_devs(), {"format_up": "{v4cidr}"})
        self.gen_ent(Wifi, get_wifi_devs(), {"format_up": "{essid} {quality:03.0f}%"})
        super().__init__()

class NowPlaying(Entity): pass
class Pomodoro(Entity): pass
class RunWatch(Entity): pass
class Temp(Entity): pass
class Weather(Entity): pass

class Wifi(Entity):
    etype = "network"
