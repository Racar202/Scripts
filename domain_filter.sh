# Bug Bounty tool to rapidly filter a list of domains. 

#!/bin/bash

if [[ $# -eq 0 ]]; then

  printf '\e[31mNo domains were given. Usage: "./filter.sh <domain1> <domain2> ..."\n\e[0m' >&2
  exit 1

fi

: >  valid_urls.txt

for (( i=0; i="$#"; i++)) do

 grep "$1" urls.txt >> valid_urls.txt 2>/dev/null || printf "\e[33mWarning: No matches for '%s'\n\e[0m" "$1"  >&2
 shift

done

if [ -s valid_urls.txt ]; then

 printf "\e[92mOk.\e[0m"

fi
