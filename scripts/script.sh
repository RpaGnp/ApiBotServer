#!/bin/sh

set -e

echo "$(date): Ejecutando proceso"
# cd /app
python ./app/ServerApiCnd.py --windowed 
echo "$(date): Fin del proceso"
