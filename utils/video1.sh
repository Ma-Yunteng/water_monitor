#! /usr/bin/env bash

avconv -f video4linux2 -r 7 -s 640x480 -i /dev/video1 video1.avi
