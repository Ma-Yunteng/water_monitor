#! /usr/bin/env bash

avconv -f video4linux2 -r 7 -s 640x480 -i /dev/video0 video0.avi
