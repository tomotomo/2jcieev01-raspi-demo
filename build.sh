#!/bin/bash

DIR=$(cd $(dirname $0);pwd)

cd ${DIR}/bin
make baro

exit 0
