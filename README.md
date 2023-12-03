# eodal_basetiff_template
A template repository for running `eodal_basetiffs`. You can use this template to run `eodal_basetiffs` for a custom area of interest, change the platform (default: Sentinel-2) and the temporal increment (default: 7 days).

In addition, an animated GIF will be created from the `rgb`, `fcir` and `ndvi` product, and a map of the area of interest (AOI) and the cloud cover over time will be plotted.

## Usage

### Using docker compose
The docker `compose.yaml` file pulls the [published docker image](https://github.com/orgs/terensis/packages/container/package/) and runs the docker container. This is the **recommended way** to use this repository.

For this to work, you must:
- Create an AOI directory and copy the AOI-geopackage file to it `mkdir aoi`
- Create an output directory for the host machine `mkdir host_output`

Adopt the content of `compose.yaml` if necessary:

```yaml
version: '3'
services:
  app:
    image: ghcr.io/terensis/eodal_basetiffs:latest  # image to pull
    volumes:
      - ./host_output:/app/container_output         # directory on the host where outputs are written to (./host_output)
      - ./aoi:/app/aoi                              # directory on the host with the AOI file (./aoi)
    command:
      [
        "-a",
        "aoi/aoi.gpkg",                             # AOI file on the host. Directory must match directory specified in volumes
        "-o",
        "container_output",                         # Container internal output directory. Is bind to ./host_output in the volumes
        "-c",
        "2056",                                     # spatial reference system in EPSG notation (here: Swiss LV95)
        "-t",
        "7",                                        # temporal increment in days (here: 7 days)
        "-p",
        "sentinel-2",                               # remote sensing platform to query (here: Sentinel-2)
        "-r",
        "True"                                      # run till complete - i.e., download all available scenes (here: True)?
      ]
    container_name: eodal_basetiffs_run             # name of the container. Can be changed.
volumes:
  host_output:
  aoi:
```

Then, you can run the docker compose file:
```bash
sudo docker compose up
```

The outputs will be stored in the output directory defined in the `compose.yaml` (`host_output` in the example above). 

### Using source code repository
There are only three steps required to get `eodal_basetiffs` running.

1. On Github, click on "Use this template" on the upper right to generate a new repository from this template.
2. Clone the new repository.
3. Enter the cloned repository. Specify your area of interest (AOI) by placing a geopackage file named `aoi.gpkg` in the [aoi folder](/aoi).
4. Execute the `eodal_basetiffs.sh` shell script by running `sh eodal_basetiffs.sh` in the (Linux) terminal. This will execute the full workflow automatically.

By **default** this will query and fetch the `Sentinel-2` imagery for the AOI starting on `January 1st, 2017` and will run with an increment of `7 days` until all scenes available `till present` have been fetched. The data is projected to web mercator (EPSG:3857).

By **default**, the satellite data products output by `eodal_basetiffs` will be stored by acquisition date in the `data` subdirectory created in the root of this repository. Plots (maps and animations) of these will be stored in `plots`.