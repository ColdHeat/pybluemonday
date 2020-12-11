#!/bin/bash
if [ ! -f "/usr/bin/go" ]; then
    curl -vvv -L -O https://golang.org/dl/go1.15.5.linux-amd64.tar.gz
    tar -xf go1.15.5.linux-amd64.tar.gz
    mv go /usr/local
    ln -s /usr/local/go/bin/go /usr/bin/go
fi
