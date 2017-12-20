#!/usr/bin/env bash

http -v GET ${SUT_B}/users token==${TOKEN}

http -b GET ${SUT_B}/users token==${TOKEN} | jq -r '._meta.total'