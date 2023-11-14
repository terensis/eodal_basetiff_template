# eodal_basetiff_template
A template repository for running `eodal_basetiffs`. You can use this template to run `eodal_basetiffs` for a custom area of interest, change the platform (default: Sentinel-2) and the temporal increment (default: 7 days).

In addition, an animated GIF will be created from the `rgb`, `fcir` and `ndvi` product, and a map of the area of interest (AOI) and the cloud cover over time will be plotted.

## Usage
There are only three steps required to get `eodal_basetiffs` running.

1. On Github, click on "use template" on the upper right to generate a new repository from this template.
2. Specify your area of interest (AOI) by placing a geopackage file named `aoi.gpkg` in the [aoi folder](/aoi).
3. Execute the `eodal_basetiffs.sh` shell script by running `sh eodal_basetiffs.sh` in the (Linux) terminal.

By **default** this will query and fetch the `Sentinel-2` imagery for the AOI starting on `January 1st, 2017` and will run with an increment of `7 days` until all scenes available `till present` have been fetched. The data is projected to web mercator (EPSG:3857).

## Output

By **default**, the satellite data products output by `eodal_basetiffs` will be stored by acquisition date in the `data` subdirectory created in the root of this repository. Plots (maps and animations) of these will be stored in `plots`.
