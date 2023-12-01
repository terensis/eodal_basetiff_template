"""
This script generates plots (maps) of a data product and an animation
(gif) from a (time) series of maps. It also plots the area of interest
on a map for fast visual inspection and the cloud cover of an area of
interest over time.

The part works natively on the output of the `eodal_basetiffs` package.

Copyright (C) 2023 Lukas Valentin Graf (lukas.graf@terensis.io)

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""

from __future__ import annotations

import argparse

import contextily as ctx
import geopandas as gpd
import imageio
import matplotlib.pyplot as plt
import pandas as pd
import warnings

from eodal.core.raster import RasterCollection
from matplotlib_scalebar.scalebar import ScaleBar
from pathlib import Path

warnings.filterwarnings("ignore")

# Allow dynamic input of AOI path
parser = argparse.ArgumentParser()
parser.add_argument(
    "-a",
    "--area-of-interest",
    type=str,
    help="path to the GeoPackage or Shapefile with the area of interest",
)
parser.add_argument(
    "-o",
    "--output-parent-dir",
    type=str,
    help="path to the directory where the plots should be stored",
)

# parse CLI arguments
args = parser.parse_args()


def generate_plots(
    data_dir: Path, product_name: str, plot_dir: Path, vector_feature: Path
) -> None:
    """
    Generate plots (maps) of a data product.

    :param data_dir:
        directory with data products
    :param product_name:
        name of the data product to plot
    :param plot_dir:
        directory for storing the plots
    :param vector_feature:
        area of interest to plot to ensure all plots cover the same extent
    """
    # loop through scenes
    for scene_dir in data_dir.glob("*"):
        if not scene_dir.is_dir:
            continue
        try:
            fpath_product = next(scene_dir.glob(f"*{product}.tif"))
        except StopIteration:
            continue
        rc = RasterCollection.from_multi_band_raster(
            fpath_product, vector_features=vector_feature
        )

        # make sure the data covers at least 90% of the area of the AOI
        aoi = gpd.read_file(vector_feature)
        area_aoi = aoi.area.iloc[0]
        area_rc = rc[rc.band_names[0]].bounds.area
        if area_rc / area_aoi < 0.9:
            continue

        # determine how to plot the product depending on the number
        # of bands
        f, ax = plt.subplots()
        if len(rc) == 1:
            rc.plot_band(
                rc.band_names[0], colormap="viridis",
                colorbar_label=product_name, ax=ax
            )
        elif len(rc) == 3:
            rc.plot_multiple_bands(band_selection=rc.band_names, ax=ax)
        ax.set_title(scene_dir.name)
        # add a scalebar
        scalebar = ScaleBar(dx=1)
        ax.add_artist(scalebar)

        # save the figure
        f.savefig(plot_dir.joinpath(
            f"{scene_dir.name}_{product_name}.png"), dpi=150)
        plt.close(f)


def make_gif(plot_dir: Path, product_name: str) -> None:
    """
    Generate an animation (gif) from a (time) series of maps.

    :param plot_dir:
        directory containing the plots (*.png) with the maps of
        the product generated using `~generate_plots`
    :param product_name:
        name of the product to plot
    """
    # get a list of pngs and sort them by their sensing date
    file_paths = [x for x in plot_dir.glob(f"*_{product_name}.png")]
    file_paths = sorted(file_paths)

    # create a file path for the animation
    fpath_animation = plot_dir.joinpath(f"{product_name}.gif")

    # create a gif
    with imageio.get_writer(fpath_animation, mode="I", duration=4) as writer:
        for filename in file_paths:
            image = imageio.imread(filename)
            writer.append_data(image)


def plot_aoi(fpath_aoi: Path, plot_dir: Path) -> None:
    """
    Plot the area of interest on a map for fast visual inspection.

    :param fpath_aoi:
        path to the area of interest
    :param plot_dir:
        directory for storing the plot
    """
    gdf = gpd.read_file(fpath_aoi)

    f, ax = plt.subplots()
    gdf.boundary.plot(ax=ax)

    # add a basemap from OpenStreetMap
    ctx.add_basemap(
        ax, crs=gdf.crs.to_string(), source=ctx.providers.OpenStreetMap.Mapnik
    )
    ax.set_axis_off()

    f.savefig(plot_dir.joinpath("aoi.png"), dpi=150)
    plt.close(f)


def plot_cloud_cover(data_dir: Path, plot_dir: Path) -> None:
    """
    Plot the cloud cover of an area of interest over time.

    :param data_dir:
        directory with data products
    :param plot_dir:
        directory for storing the plots
    """
    file_paths = [x for x in data_dir.glob("*/*cloudy_pixel_percentage.txt")]
    file_dates = [pd.to_datetime(x.parent.name) for x in file_paths]
    df = pd.DataFrame(
        data={
            "date": file_dates,
            "cloud_cover": [float(x.read_text()) for x in file_paths],
        }
    )
    df.sort_values(by="date", inplace=True)

    # plot time series
    f, ax = plt.subplots()
    ax.scatter(df.date, df.cloud_cover)
    ax.set_xlabel("Date")
    ax.set_ylabel("Cloud cover (%)")

    f.savefig(plot_dir.joinpath("cloud_cover.png"), dpi=150)
    plt.close(f)

    # plot histogram
    f, ax = plt.subplots()
    ax.hist(df.cloud_cover, bins=20)
    ax.set_xlabel("Cloud cover (%)")
    ax.set_ylabel("Frequency")
    ax.set_title(f"N = {df.shape[0]}")

    f.savefig(plot_dir.joinpath("cloud_cover_hist.png"), dpi=150)


if __name__ == "__main__":
    parent_dir = Path(args.output_parent_dir)
    data_dir = parent_dir
    products = ["fcir", "rgb", "ndvi"]
    plot_dir = Path(parent_dir.joinpath("Plots"))
    plot_dir.mkdir(exist_ok=True)

    vector_feature = Path(args.area_of_interest)

    plot_aoi(fpath_aoi=vector_feature, plot_dir=plot_dir)

    plot_cloud_cover(data_dir=data_dir, plot_dir=plot_dir)

    for product in products:
        generate_plots(
            data_dir=data_dir,
            product_name=product,
            plot_dir=plot_dir,
            vector_feature=vector_feature,
        )
        make_gif(plot_dir=plot_dir, product_name=product)
