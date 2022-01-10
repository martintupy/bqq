#!/bin/sh

cd "$(dirname "${BASH_SOURCE[0]}")/.."

python3 -m build

VERSION=$(cat setup.cfg | grep "version =" | cut -d = -f 2 | xargs)

docker build . \
  --build-arg version=$VERSION \
  --tag bqq:latest \
  --tag bqq:$VERSION