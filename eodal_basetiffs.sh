#!/bin/bash

# create virtual python3.11 environment if it does not exist
if [ ! -d ".venv" ]; then
    virtualenv -q -p /usr/bin/python3.11 .venv
fi

# activate virtual environment
source .venv/bin/activate
pip install --upgrade pip

# install eodal_basetiffs from Github and other dependencies for visualization
pip install contextily
pip install imageio
pip install matplotlib-scalebar
pip uninstall eodal_basetiffs -y
pip install git+https://github.com/terensis/eodal_basetiffs_GPL3@1.2


# initialize variable defaults for command line arguments
aoi=""
output=""
tempincrement=""
targetcrs=3857
product=""
run_till_complete="False"

# parse command line arguments
while getopts a:o:t:c:p:r: flag
do
    case "${flag}" in
        a) aoi=${OPTARG};;
        o) output=${OPTARG};;
        t) tempincrement=${OPTARG};;
        c) targetcrs=${OPTARG};;
        p) product=${OPTARG};;
        r) run_till_complete=${OPTARG};;
    esac
done

# execute python script using the command line interface
eodal_basetiffs -a "$aoi" -o "$output" -t "$tempincrement" -c "$targetcrs" -p "$product" -r "$run_till_complete"

# visualize the results
python visualize.py -a "$aoi" -o "$output"
