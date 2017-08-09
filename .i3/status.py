#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os

from status_dock.bar import Bar


CONFIG_FILE = f"{os.environ['HOME']}/.i3/status.conf.json"


if __name__ == "__main__":
    import sys
    try:
        layout = sys.argv[1]
    except IndexError:
        raise ValueError("Please supply the layout as the only argument.")

    b = Bar(CONFIG_FILE, layout)
    b.run()

