#!/bin/bash
if [ ! -f "/usr/bin/go" ]; then
    echo "Downloading linux-386 Golang"
    curl -L -O https://golang.org/dl/go1.15.5.linux-386.tar.gz
    tar -xf go1.15.5.linux-386.tar.gz
fi
