#!/bin/bash
for p in {1..20}; do
    wget http://ctf.thehackerconclave.es:20002/images/$p.jpg
done