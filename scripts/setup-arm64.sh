#!/bin/bash
if [ ! -f "/usr/bin/go" ]; then
    echo "Downloading arm64 Golang"
    curl -vvv -L -O https://golang.org/dl/go1.15.5.linux-arm64.tar.gz
    tar -xf go1.15.5.linux-arm64.tar.gz
fi