#!/bin/bash
if [ ! -f "/usr/bin/go" ]; then
    curl -L -O https://golang.org/dl/go1.15.5.linux-armv6l.tar.gz
    tar -xf go1.15.5.linux-armv6l.tar.gz
    mv go /usr/local
    ln -s /usr/local/go/bin/go /usr/bin/go
fi