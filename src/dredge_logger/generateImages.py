import datetime
import logging
import os
import warnings

import matplotlib.dates as mdates
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import pandas as pd
from dredge_logger.config import config
from PIL import Image

warnings.filterwarnings("ignore")

_logger = logging.getLogger(__name__)


def generateGraph(filename, defaultPath=True):
    if not config.vars["images"]["save"]:
        return []

    if defaultPath:
        csv_file = config.vars["csv_path"] + "/" + filename
    else:
        csv_file = filename

    df = pd.read_csv(csv_file, skipinitialspace=True)

    graph_vars = []
    for graph in config.vars["images"]["graphs"]:
        graph_vars.append(graph["variable"])

    for col in graph_vars:
        df[col] = pd.to_numeric(df[col], errors="coerce")

    time_var = config.vars["images"]["time"]

    graph_vars_time = graph_vars + [time_var]

    df.dropna(
        subset=graph_vars_time,
        inplace=True,
    )

    time = [datetime.datetime.strptime(time, "%Y-%m-%d %H:%M:%S") for time in df[time_var] if isinstance(time, str)]

    if not os.path.exists(config.vars["image_path"]):
        os.makedirs(config.vars["image_path"])
        _logger.debug("Making directory " + config.vars["image_path"])

    if not os.path.exists(f"{config.vars['image_path']}/subImages"):
        os.makedirs(f"{config.vars['image_path']}/subImages")
        _logger.debug("Making directory " + f"{config.vars['image_path']}/subImages")

    plt.rcParams["figure.figsize"] = [23, 5]

    for graph in config.vars["images"]["graphs"]:
        fig, ax = plt.subplots()
        ax.plot(time, df[graph["variable"]])
        ax.set(
            xlabel="time",
            ylabel=f"{graph['name']} - {graph['unit']}",
            title=f"{graph['name']} - {graph['unit']}",
        )
        ax.grid()
        fig.autofmt_xdate()
        ax.fmt_xdata = mdates.DateFormatter("%Y-%m-%d %H:%M:%S")
        ax.xaxis.set_major_formatter(mdates.DateFormatter("%H:%M:%S"))
        ax.xaxis.set_major_locator(ticker.MaxNLocator(25))
        ax.xaxis.set_minor_locator(ticker.AutoMinorLocator())
        ax.yaxis.set_minor_locator(ticker.AutoMinorLocator())

        fig.savefig(f"{config.vars['image_path']}/subImages/{graph['name']}_{filename.strip('.csv')}.png")

    images = []

    for graph in config.vars["images"]["graphs"]:
        images.append(Image.open(f"{config.vars['image_path']}/subImages/{graph['name']}_{filename.strip('.csv')}.png"))

    images = [images[i : i + 5] for i in range(0, len(images), 5)]

    img_size = images[0][0].size

    images_filenames = []

    for pos, set in enumerate(images):
        combined = Image.new("RGB", (img_size[0], 5 * img_size[1]), (250, 250, 250))
        for i in range(len(set)):
            combined.paste(set[i], (0, img_size[1] * i))
        if pos != 0:
            combined.save(f"{config.vars['image_path']}/Smoke_Chart_{filename.strip('.csv')}_{pos}.png", "PNG")
            images_filenames.append(f"{config.vars['image_path']}/Smoke_Chart_{filename.strip('.csv')}_{pos}.png")
        else:
            combined.save(f"{config.vars['image_path']}/Smoke_Chart_{filename.strip('.csv')}.png", "PNG")
            images_filenames.append(f"{config.vars['image_path']}/Smoke_Chart_{filename.strip('.csv')}.png")

    return images_filenames


if __name__ == "__main__":
    filename = "2022-01-11.csv"
    filenames = generateGraph(filename, True)
    print(filenames)
