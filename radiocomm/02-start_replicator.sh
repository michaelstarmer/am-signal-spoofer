#!/bin/bash

rsync -a mps@192.168.0.10:~/dev/projects/facki/radiocomm/src/ ./src && \
echo "Sync complete. Executing receiver..."

python ./src/2_replicate-signal.py && \

if [[ $? -ne 0 ]] ; then
  echo "Error in receiver script. Aborting..."
  exit 0;
fi

echo "Success. Signature saved to generated/"

timestamp=$( date +%s )
rsync -a ../generated/ mps@192.168.0.10:~/dev/projects/facki/radiocomm/generated
rsync -a ../workspace/ mps@192.168.0.10:~/dev/projects/facki/radiocomm/workspace

# rsync -a ./generated/ mps@192.168.0.10:~/dev/projects/facki/pi-transmitter/generated/export-"$timestamp".csv
#scp ./signal-log.txt mps@192.168.0.10:~/dev/projects/pi-transmitter/results/signal-log-"$timestamp".txt
