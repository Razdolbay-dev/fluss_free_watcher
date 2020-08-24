#!/bin/sh

CFGDIR=/etc/astra
LUA=/etc/astra/dumpstream.lua
INITD=/etc/init.d/astra
BINFILE=/usr/bin/astra

if [ $(id -u) != "0" ]; then
    echo "Please, launch script with root permission"
    exit 1
fi

mkdir -p /etc/astra

echo "downloading..."

wget -q -O $INITD http://cesbo.com/download/astra/scripts/init-d.sh
chmod +x $INITD

wget -q -O $BINFILE https://cesbo.com/download/astra/4.4.182/free/x86_64/astra
chmod +x $BINFILE

wget -q -O $LUA https://cesbo.com/download/astra/scripts/dumpstream.lua
chmod +x $LUA

echo 'Вроде все'
echo "installed $($BINFILE -v)"
