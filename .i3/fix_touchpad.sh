#!/bin/bash

ID=$(xinput list | grep Synaptics\ TouchPad | cut -d= -f2 | awk '{print $1}')
TAP_FEATURE=$(xinput list-props $ID | grep "Tapping Enabled (" | cut -d'(' -f2 | cut -d')' -f1)
SCROLL_FEATURE=$(xinput list-props $ID | grep "Natural Scrolling Enabled (" | cut -d'(' -f2 | cut -d')' -f1)

xinput set-prop $ID $TAP_FEATURE 1
xinput set-prop $ID $SCROLL_FEATURE 0

exit 0
