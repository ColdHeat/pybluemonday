#!/bin/sh
if [ ! -f "/usr/bin/go" ]; then
    echo "Downloading linux-amd64 Golang"
    if [ -x /usr/bin/curl ]; then
        curl -L -O https://golang.org/dl/go1.15.5.linux-amd64.tar.gz
    else
        wget -v https://golang.org/dl/go1.15.5.linux-amd64.tar.gz
    fi
    tar -xf go1.15.5.linux-amd64.tar.gz
    if [ -x /lib/libc.musl-* ]; then
        apk add --no-cache libc6-compat
    fi
fi
