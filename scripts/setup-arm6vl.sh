#!/bin/bash
if [ ! -f "/usr/bin/go" ]; then
    echo "Downloading arm6vl Golang"
    curl -L -O https://golang.org/dl/go1.15.5.linux-armv6l.tar.gz
    tar -xf go1.15.5.linux-armv6l.tar.gz
fi