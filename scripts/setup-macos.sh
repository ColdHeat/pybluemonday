#!/bin/sh
if [ ! -f "/usr/local/bin/go" ]; then
    echo "Downloading darwin-amd64 Golang"
    if [ -x /usr/bin/curl ]; then
        curl -L -O https://golang.org/dl/go1.15.5.darwin-amd64.tar.gz
    else
        wget -v https://golang.org/dl/go1.15.5.darwin-amd64.tar.gz
    fi
    tar -xf go1.15.5.darwin-amd64.tar.gz
fi
