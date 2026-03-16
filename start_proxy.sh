#!/bin/bash
processDumpID=$(ps aux | grep -c '[m]itmdump')
processWebID=$(ps aux | grep -c '[m]itmweb')
echo 'Запущенных mitmdump =' ${processDumpID}
echo 'Запущенных mitmweb =' ${processWebID}
processID=$((processDumpID+$processWebID))
if [ "$processID" -eq 0 ]
then {
  echo "Run proxy"
  mitmweb -s proxy_handler.py --set anticache=true --set ssl_insecure=true
  exit 1
}
else {
echo "Proxy is already running..."
}
exit
fi