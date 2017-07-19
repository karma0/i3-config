#!/bin/bash

WS_LAYOUT_FILE="~/.i3/terms.json"
TERM="lilyterm"
TERM_PARAMS="-name"

i3-msg append_layout "$WS_LAYOUT_FILE"

for window in $(seq 9); do
  $TERM $TERM_PARAMS "W$window" &
done

