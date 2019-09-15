#!/bin/sh

set -e

js="elm.js"

elm make --optimize --output=$js ./src/TextHandlerPage.elm
sed -i 's@http://127.0.0.1:5000@@g' elm.js


