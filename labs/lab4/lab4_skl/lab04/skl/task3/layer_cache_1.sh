#!/bin/bash

echo "        size,          ops,         time,      op/time"

for ((i=1024; i <= 80960; i = i + 1024)) do
    ./task3 64 $i $((10000000000 / $i))
done
