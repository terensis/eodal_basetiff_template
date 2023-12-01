# eodal_basetiff_template
A template repository for running `eodal_basetiffs`. You can use this template to run `eodal_basetiffs` for a custom area of interest, change the platform (default: Sentinel-2) and the temporal increment (default: 7 days).

In addition, an animated GIF will be created from the `rgb`, `fcir` and `ndvi` product, and a map of the area of interest (AOI) and the cloud cover over time will be plotted.

## Usage
There are only three steps required to get `eodal_basetiffs` running.

1. On Github, click on "Use this template" on the upper right to generate a new repository from this template.
2. Clone the new repository.
3. Enter the cloned repository. Specify your area of interest (AOI) by placing a geopackage file named `aoi.gpkg` in the [aoi folder](/aoi).
4. Execute the `eodal_basetiffs.sh` shell script by running `sh eodal_basetiffs.sh` in the (Linux) terminal. This will execute the full workflow automatically.

By **default** this will query and fetch the `Sentinel-2` imagery for the AOI starting on `January 1st, 2017` and will run with an increment of `7 days` until all scenes available `till present` have been fetched. The data is projected to web mercator (EPSG:3857).

## Output

By **default**, the satellite data products output by `eodal_basetiffs` will be stored by acquisition date in the `data` subdirectory created in the root of this repository. Plots (maps and animations) of these will be stored in `plots`.


## Setup dockerfile
First, build the dockerfile into a docker image: 
```bash
sudo docker build -t your-image-name .
```
In this command, your-image-name should be replaced with the name you want to give to your Docker image, and the . specifies that Docker should look for the Dockerfile in the current directory.

You can check for your available images by: 
```bash
sudo docker images
```

Unused images can be deleted by:
```bash
sudo docker rmi your-image-name -f
```

Then, you can run the created docker image:
```bash
sudo docker run --rm --name your-container-name your-image-name 

```
Don't forget to set the CLI arguments for the `.sh` script
```bash
sudo docker run --rm --name your-container-name your-image-name  -a -t ...
```

### Run dockerfile with volumes
```bash
sudo docker run -v /host_output:/app/container_output --rm --name your-container-name your-image-name  -a -t
```

We have to use [bind mounts](https://docs.docker.com/storage/bind-mounts/) for the output to be written to the host's filesystem. The `$(pwd)` sub-command expands to the current working directory on Linux or macOS hosts.
```bash
sudo docker run --mount type=bind,source="$(pwd)"/host_output,target=/container/container_output --rm --name your-container-name your-image-name -a path/to/aoi/file.gpkg -o /container/container_output -t 7 -p sentinel-2
```

