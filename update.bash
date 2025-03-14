#!/bin/bash

echo -e "\e[32m >>\e[m update script \e[32m<< \e[m"

echo -e "\e[32m :\e[m pulling ..."
git pull
echo -e "\e[32m :\e[m getting requirements ..."
pip install -r requirements.txt
echo -e "\e[32m :\e[m ensuring pip is up-to-date ..."
pip install --upgrade pip

echo -e "\e[32m >>\e[m update script done \e[32m<< \e[m"
