#!/bin/bash


if [ -z "$*" ]; then
  i3-msg -t get_workspaces | tr ',' '\n' | grep "name" | sed 's/"name":"\(.*\)"/\1/g' | sort -n
else
  if [ -n "$*" ]; then
    i3-msg workspace "$*" >/dev/null
  fi
fi

