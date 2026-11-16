#!/bin/sh
# Assemble le site publiable dans public/
set -e
cd "$(dirname "$0")"
rm -rf public && mkdir -p public
cp -r img public/img
cp index.html public/index.html
echo "public/ prêt : $(du -sh public | cut -f1)"
