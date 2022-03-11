#!/bin/sh
set -e

input="exception-list.txt"
while IFS= read -r line
do
  echo "$line"
  docker pull $line
  docker tag $line 192.168.0.3:30500/$line
  docker push 192.168.0.3:30500/$line
done < "$input"