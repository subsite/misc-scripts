#!/bin/sh

# Read file aloud using Pico TTS and vlc
# apt install libttspico-utils vlc

if [ $# -lt 1 ]; then
	echo "USAGE: tts.sh /path/to/textfile"
	exit
fi

TEMPFILE="/tmp/ttsoutput.wav"
TEXTFILE="$(cat $1)"

pico2wave -w=$TEMPFILE "${TEXTFILE}"
vlc $TEMPFILE
