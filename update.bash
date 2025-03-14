#!/bin/bash

echo -e "\e[32m >>\e[m update script \e[32m<< \e[m"

#https://stackoverflow.com/a/15454284
[[ "$VIRTUAL_ENV"  == "" ]]; INENV=$?

if [ "$INENV" != "1" ]
then
	echo -e "\e[31m!> ERROR: NOT IN VENV <!\e[m"
	echo ''
	#        __-1----.----2----.----3----.----4----.----5"
	echo -e "\tThis script is intended to be run from"
	echo -e "\twithin a python virtual environment (venv)"
	echo -e "\tand not as a plain script."
	echo ''
	#        __-1----.----2----.----3--      --.----4--    --.----5"
	echo -e "\tPlease run the included \e[35msetup.bash\e[m script"
	#        __-1----.----2----.----3----.----4----.----5"
	echo -e "\tif you havent yet, then run one of ..."
	echo ''
	#       0----     .----1----.----2----.----    3----.----4----.----5"---.----6
	echo -e "    \e[35msource .venv/bin/activate\e[m        in (ba/z)sh   #! "
	echo -e "    \e[35msource .venv/bin/activate.fish\e[m   in fish       ><>"
	echo -e "    \e[35msource .venv/bin/activate.ps1\e[m    in powershell >_ "
	echo -e "    \e[35msource .venv/bin/activate.csh\e[m    in csh         c "
	exit
fi


echo -e "\e[32m :\e[m pulling ..."
git pull
echo -e "\e[32m :\e[m getting requirements ..."
pip install -r requirements.txt
echo -e "\e[32m :\e[m ensuring pip is up-to-date ..."
pip install --upgrade pip

echo -e "\e[32m >>\e[m update script done \e[32m<< \e[m"
