#!/bin/bash

REQUIRED_PKG="tmux"
PKG_OK=$(dpkg-query -W --showformat='${Status}\n' $REQUIRED_PKG|grep "install ok installed")
echo Checking for $REQUIRED_PKG: $PKG_OK
if [ "" = "$PKG_OK" ]; then
  echo "No $REQUIRED_PKG. Setting up $REQUIRED_PKG."
  sudo apt-get --yes install $REQUIRED_PKG
fi

cd "$(dirname "$0")"

session="enviro-fastapi"
tmux has-session -t $session 2>/dev/null

if [ $? != 0 ]; then
  tmux new-session -d -s $session

  window=0
  tmux rename-window -t $session:$window 'enviro'
  tmux send-keys -t $session:$window 'uvicorn app.main:app --host 0.0.0.0 --port 8080 --reload' C-m
fi

tmux attach-session -t $session