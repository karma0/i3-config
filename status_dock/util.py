from Xlib import display
from Xlib.ext import randr
import netifaces as net
import re


def snake2camel(name):
    return re.sub(r'(?:^|_)([a-z])', lambda x: x.group(1).upper(), name)

def snake2camelback(name):
    return re.sub(r'_([a-z])', lambda x: x.group(1).upper(), name)

def camel2snake(name):
    return name[0].lower() + re.sub(r'(?!^)[A-Z]', lambda x: '_' + x.group(0).lower(), name[1:])

def camelback2snake(name):
    return re.sub(r'[A-Z]', lambda x: '_' + x.group(0).lower(), name)

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
