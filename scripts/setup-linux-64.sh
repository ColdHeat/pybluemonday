#!/bin/bash
if [ ! -f "/usr/bin/go" ]; then
    echo "Downloading linux-amd64 Golang"
    curl -L -O https://golang.org/dl/go1.15.5.linux-amd64.tar.gz
    tar -xf go1.15.5.linux-amd64.tar.gz
fi
