#!/bin/bash

# create virtual environment if it does not exist
if [ ! -d ".venv" ]; then
    virtualenv -q -p /usr/bin/python .venv
fi

# activate virtual environment
source .venv/bin/activate
pip install --upgrade pip

# install eodal_basetiffs from Github and other dependencies for visualization
pip install contextily
pip install imageio
pip uninstall eodal_basetiffs -y
pip install git+https://github.com/terensis/eodal_basetiffs_GPL3


# execute python script using the command line interface
eodal_basetiffs -a aoi/aoi_cape-coast.gpkg -o data -t 7 -c 3857 -p sentinel-2 -r True

# visualize the results
python visualize.py
