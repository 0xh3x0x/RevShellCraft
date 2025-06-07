#!/bin/bash

#Installer of the RevShellCraft tool, run this script as root

#defines colors
GREEN='\033[0;32m'
RED='\033[0;31m'

if [ "$(id -u)" -eq 0 ];then
  echo -e "${GREEN}[🐧] Running script as root: ${RED}OK"
  sudo cp ./revshellcraft.py /usr/bin/revshellcraft
  sudo chmod +x /usr/bin/revshellcraft
  echo -e "${GREEN}[💾] the RevShellCraft has been installed successfully!"
  echo -e "[💜] run tool by ${RED}revshellcraft"
else
  echo -e "${RED}[-] run this script as root"
  exit 0
fi 
