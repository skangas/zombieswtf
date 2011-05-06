#!/bin/bash

# For each subdirectory, rename all files to 0000.png, 0001.png, and so on.

# Use when you are in a directory with 000, 045, 090 and so on with images

for directory in `ls -d */` 
do
    cd $directory 
    counter=0
    for file in `ls` 
    do
        mv $file `printf "%04d.png" "$counter"` -v
        let counter=$[ $counter + 1 ]
    done
    cd .. 
done
