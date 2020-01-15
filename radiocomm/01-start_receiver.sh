#!/bin/bash

rsync -a mps@192.168.0.10:~/dev/projects/facki/radiocomm/src/ ./src && \
echo "Sync complete. Executing receiver..."

sleep 1

python ./src/1_sniffer.py && \

if [[ $? -ne 0 ]] ; then
  echo "Error in receiver script. Aborting..."
  exit 0;
fi

echo "Receiver was successful. Storing graph."

timestamp=$( date +%s )
rsync -a ../generated/ mps@192.168.0.10:~/dev/projects/facki/radiocomm/generated
# rsync -a ./generated/ mps@192.168.0.10:~/dev/projects/facki/pi-transmitter/generated/export-"$timestamp".csv
#scp ./signal-log.txt mps@192.168.0.10:~/dev/projects/pi-transmitter/results/signal-log-"$timestamp".txt
