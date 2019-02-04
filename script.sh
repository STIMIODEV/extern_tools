#!/bin/bash
killall JLinkRTTClient
killall JLinkExe

mkdir -p "Donnees"

heure=$(date +%Y_%m_%d_%Hh%Mmin)

if [ $# == "1" ]; then
   name="$1_"
fi

JLinkExe -device nrf52 -if swd -speed 4000 -autoconnect 1 &
sleep 1
JLinkRTTClient |ts '%H:%M:%S;' |cat > Donnees/data_$name$heure.txt &

python3 live_accelerometer.py -input Donnees/data_$name$heure.txt
