#!/bin/bash

echo -e "\e[32m|>\e[m TASK: Create venv"
echo -e "\e[32m :\e[m Creating venv at \e[35m.venv\e[0m ..."
python3 -m venv .venv
echo -e "\e[32m :\e[m Activating venv ..."
source .venv/bin/activate
echo -e "\e[32m<|\e[m TASK COMPLETE"

echo -e "\e[32m|>\e[m TASK: Run updates"
./tools/update.bash
echo -e "\e[32m<|\e[m TASK COMPLETE"


echo -e "\e[32m|>\e[m TASK: Create links"
echo -e "\e[32m :\e[m Linking new file \e[35mapp\e[m to \e[35mapp.py\e[m ..."
ln -s app.py app
echo -e "\e[32m :\e[m Linking new file \e[35m/home/protected/run-site.bash\e[m to \e[35mrun.bash\e[m ..."
ln -s run.bash /home/protected/run-site.bash
echo -e "\e[32m<|\e[m TASK COMPLETE"
