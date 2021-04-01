#!/bin/bash
if [ ! -f "/usr/local/bin/go" ]; then
    echo "Downloading darwin-amd64 Golang"
    curl -L -O https://golang.org/dl/go1.15.5.darwin-amd64.tar.gz
    tar -xf go1.15.5.darwin-amd64.tar.gz
fi
