#!/bin/bash

runtime=90
resting_time=30

# Activate venv
# (this assumes the daemon config knows where to drop us)
source .venv/bin/activate

while true;do
	# Run waitress on the flask app
	timeout "$runtime" \
		waitress-serve --port=50505 app:app

	# Ensure all things are up-to-date
	sleep "$resting_time"
	./update.bash
	sleep "$resting_time"
done
