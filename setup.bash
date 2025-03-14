#!/bin/bash

python3 -m venv .venv
source .venv/bin/activate

./update.bash

ln -s app.py app
ln -s run.bash /home/protected/run-site.bash
