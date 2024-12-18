import pathlib

import cartopy.crs as ccrs
import cartopy.feature as cfeature
import matplotlib.pyplot as plt
from mpl_toolkits import axes_grid1

from ncoda_util import reader

TEMPERATURE_FILE = pathlib.Path(
    "tests/manual/in_data/example/seatmp_pre_000000_005000_1o2161x1051_2023090700_00000000_analfld"
)
LON_FILE = pathlib.Path(
    "tests/manual/in_data/static/grdlon_sfc_000000_000000_1o2161x1051_datafld"
)
LAT_FILE = pathlib.Path(
    "tests/manual/in_data/static/grdlat_sfc_000000_000000_1o2161x1051_datafld"
)

LEVEL = 0
PLOT_TITLE = "Sea Surface Temperature (°C)"
DPI = 800


def main():
    temperature_data = reader.read_data(TEMPERATURE_FILE)
    lons = reader.read_coord(LON_FILE)
    lats = reader.read_coord(LAT_FILE)

    data_2d = temperature_data[:, :, LEVEL]

    projection = ccrs.Mercator(central_longitude=180.0)
    fig, ax = plt.subplots(subplot_kw={"projection": projection})

    mesh = ax.pcolormesh(lons, lats, data_2d, transform=ccrs.PlateCarree(), cmap="jet")

    ax.margins(0)
    ax.add_feature(cfeature.OCEAN)
    ax.add_feature(cfeature.LAND, edgecolor="black")
    ax.add_feature(cfeature.LAKES, edgecolor="black")
    ax.add_feature(cfeature.RIVERS)
    states = cfeature.NaturalEarthFeature(
        category="cultural",
        scale="50m",
        facecolor="none",
        name="admin_1_states_provinces_lines",
    )
    ax.add_feature(states, edgecolor="black")
    ax.add_feature(cfeature.BORDERS)

    # colorbar
    divider = axes_grid1.make_axes_locatable(ax)
    cax = divider.append_axes("right", size="5%", pad=0.1, axes_class=plt.Axes)
    cbar = plt.colorbar(mesh, cax=cax)

    cbar.set_label(PLOT_TITLE)

    ax.coastlines(resolution="110m")
    gl = ax.gridlines(draw_labels=True)

    # labels
    gl.top_labels = True
    gl.bottom_labels = True
    gl.left_labels = True
    gl.right_labels = False

    fig.suptitle(PLOT_TITLE)
    plt.savefig("tests/manual/plots/ncoda_sst_plot.png", dpi=DPI)


if __name__ == "__main__":
    main()
