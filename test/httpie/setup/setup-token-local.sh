#!/bin/bash

echo "使用 source this-file 来在当前终端环境中导入SUT_B、TOKEN等变量"

export SUT_S=http
export SUT_H=localhost
export SUT_P=5000
export SUT_B=${SUT_S}://${SUT_H}:${SUT_P}

export TOKEN=$(http -b POST ${SUT_B}/tokens/ username==origin passwd==Aa.123456 | jq -r '.encoded')


