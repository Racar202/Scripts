#!/bin/bash

echo -n "Folder's name: "
read folder

if [ -d "$folder" ]; then
  echo -e "\e[31mDirectory already exists.\e[0m"
else
  mkdir -p "$folder"
  cd "$folder"
fi
