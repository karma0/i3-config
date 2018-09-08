#!/bin/bash

ID=$(xinput list | grep Synaptics\ TouchPad | cut -d= -f2 | awk '{print $1}')
TAP_FEATURE=$(xinput list-props $ID | grep "Tapping Enabled (" | cut -d'(' -f2 | cut -d')' -f1)

xinput set-prop $ID $TAP_FEATURE 1

exit 0
