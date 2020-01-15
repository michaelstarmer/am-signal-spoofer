#!/bin/bash

rsync -a mps@192.168.0.10:~/dev/projects/facki/radiocomm/src/ /services/facki/radiocomm/src && \
echo "Sync complete. Transmitting signal..."

python ./src/3_transmit-signal.py && \

if [[ $? -ne 0 ]] ; then
  echo "Error in transmitter script. Aborting..."
  exit 0;
fi

echo "Signal transmittet successfully/"

timestamp=$( date +%s )
#rsync -a ../generated/ mps@192.168.0.10:~/dev/projects/facki/radiocomm/generated
# rsync -a ./generated/ mps@192.168.0.10:~/dev/projects/facki/pi-transmitter/generated/export-"$timestamp".csv
#scp ./signal-log.txt mps@192.168.0.10:~/dev/projects/pi-transmitter/results/signal-log-"$timestamp".txt
