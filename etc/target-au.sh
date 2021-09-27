#!/bin/bash

# create a minified base64-encoded JSON string

json=$(cat <<__json__
{"name":"Target Australia",
"country": "au",
"dest":"target.com.au",
"registered": "20210901",
"expires": "20230901"}
__json__
)

echo $json | jsmin | base64
