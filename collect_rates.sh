#!/bin/bash
# Collect Alsoug market rate every 6h via cron

curl -s -X POST "http://localhost:5000/convert" \
  -d "base=USD&target=SDG&amount=1" \
  -o /dev/null
