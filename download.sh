#!/bin/sh

mkdir -p data
if [ -d "data/sadie-d1" ]; then
    echo "data/sadie-d1 already exists, skipping download"
else
    mkdir -p data/sadie-d1
    wget https://www.york.ac.uk/sadie-project/Resources/SADIEIIDatabase/D1/D1_HRIR_WAV.zip
    unzip D1_HRIR_WAV.zip -d data/sadie-d1
    rm D1_HRIR_WAV.zip
fi
