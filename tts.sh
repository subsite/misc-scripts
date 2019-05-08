#!/bin/sh

# Read file aloud using Pico TTS and vlc
# apt install libttspico-utils vlc

if [ $# -lt 1 ]; then
	echo "USAGE: tts.sh /path/to/textfile"
	exit
fi

TEMPFILE="/tmp/ttsoutput.wav"
TEXTFILE=$1

#pico2wave -w=$TEMPFILE "$(cat $TEXTFILE)"
mimic -f ${1} -o $TEMPFILE -voice slt

vlc $TEMPFILE
