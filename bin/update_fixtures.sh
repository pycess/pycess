#!/bin/sh

here="$(dirname "$0")"

$here/../manage.py dumpdata --format json --indent 4 process \
    > $here/../process/fixtures/murksmeldung.json