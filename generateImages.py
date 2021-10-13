import config

import pandas as pd
import datetime
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import matplotlib.ticker as ticker
import os
import logging
from PIL import Image
import warnings

warnings.filterwarnings("ignore")


def generateGraph(filename, defaultPath=True):
    """
    Velocity            - FPS
    Vacuum              - Inches WC
    Discharge Pressure  - PSI
    Pump Speed          - RPM
    Depth               - Feet
    """

    if defaultPath:
        csv_file = config.csv_path + "/" + filename
    else:
        csv_file = filename

    df = pd.read_csv(
        csv_file,
        skipinitialspace=True,
        parse_dates=["msg_start_time", "msg_end_time"],
    )

    for col in [
        "vert_correction",
        "ch_latitude",
        "ch_longitude",
        "ch_depth",
        "ch_heading",
        "slurry_velocity",
        "slurry_density",
        "pump_rpm",
        "vacuum",
        "outlet_psi",
        "offset",
        "rot",
    ]:
        df[col] = pd.to_numeric(df[col], errors="coerce")

    time = [
        datetime.datetime.strptime(time, "%Y-%m-%d %H:%M:%S") for time in df["msg_time"]
    ]

    plt.rcParams["figure.figsize"] = [23, 5]

    # VELOCITY
    fig_Ve, ax_Ve = plt.subplots()
    ax_Ve.plot(time, df["slurry_velocity"])
    ax_Ve.set(
        xlabel="time",
        ylabel="Velocity - FPS",
        title="Velocity - FPS",
    )
    ax_Ve.grid()
    fig_Ve.autofmt_xdate()
    ax_Ve.fmt_xdata = mdates.DateFormatter("%Y-%m-%d %H:%M:%S")
    ax_Ve.xaxis.set_major_formatter(mdates.DateFormatter("%H:%M:%S"))
    ax_Ve.xaxis.set_major_locator(ticker.MaxNLocator(25))
    ax_Ve.xaxis.set_minor_locator(ticker.AutoMinorLocator())
    ax_Ve.yaxis.set_minor_locator(ticker.AutoMinorLocator())

    # VACUUM
    fig_Va, ax_Va = plt.subplots()
    ax_Va.plot(time, df["vacuum"])
    ax_Va.set(
        xlabel="time",
        ylabel="Vacuum - Inches WC",
        title="Vacuum - Inches WC",
    )
    ax_Va.grid()
    fig_Va.autofmt_xdate()
    ax_Va.fmt_xdata = mdates.DateFormatter("%Y-%m-%d %H:%M:%S")
    ax_Va.xaxis.set_major_formatter(mdates.DateFormatter("%H:%M:%S"))
    ax_Va.xaxis.set_major_locator(ticker.MaxNLocator(25))
    ax_Va.xaxis.set_minor_locator(ticker.AutoMinorLocator())
    ax_Va.yaxis.set_minor_locator(ticker.AutoMinorLocator())

    # Discharge Pressure
    fig_Dp, ax_Dp = plt.subplots()
    ax_Dp.plot(time, df["outlet_psi"])
    ax_Dp.set(
        xlabel="time",
        ylabel="Discharge Pressure - PSI",
        title="Discharge Pressure - PSI",
    )
    ax_Dp.grid()
    fig_Dp.autofmt_xdate()
    ax_Dp.fmt_xdata = mdates.DateFormatter("%Y-%m-%d %H:%M:%S")
    ax_Dp.xaxis.set_major_formatter(mdates.DateFormatter("%H:%M:%S"))
    ax_Dp.xaxis.set_major_locator(ticker.MaxNLocator(25))
    ax_Dp.xaxis.set_minor_locator(ticker.AutoMinorLocator())
    ax_Dp.yaxis.set_minor_locator(ticker.AutoMinorLocator())

    # Pump Speed
    fig_Ps, ax_Ps = plt.subplots()
    ax_Ps.plot(time, df["pump_rpm"])
    ax_Ps.set(
        xlabel="time",
        ylabel="Pump Speed - RPM",
        title="Pump Speed - RPM",
    )
    ax_Ps.grid()
    fig_Ps.autofmt_xdate()
    ax_Ps.fmt_xdata = mdates.DateFormatter("%Y-%m-%d %H:%M:%S")
    ax_Ps.xaxis.set_major_formatter(mdates.DateFormatter("%H:%M:%S"))
    ax_Ps.xaxis.set_major_locator(ticker.MaxNLocator(25))
    ax_Ps.xaxis.set_minor_locator(ticker.AutoMinorLocator())
    ax_Ps.yaxis.set_minor_locator(ticker.AutoMinorLocator())

    # Depth
    fig_De, ax_De = plt.subplots()
    ax_De.plot(time, df["ch_depth"])
    ax_De.set(
        xlabel="time",
        ylabel="Depth - Feet",
        title="Depth - Feet",
    )
    ax_De.grid()
    fig_De.autofmt_xdate()
    ax_De.fmt_xdata = mdates.DateFormatter("%Y-%m-%d %H:%M:%S")
    ax_De.xaxis.set_major_formatter(mdates.DateFormatter("%H:%M:%S"))
    ax_De.xaxis.set_major_locator(ticker.MaxNLocator(25))
    ax_De.xaxis.set_minor_locator(ticker.AutoMinorLocator())
    ax_De.yaxis.set_minor_locator(ticker.AutoMinorLocator())

    if not os.path.exists(config.image_path):
        os.makedirs(config.image_path)
        logging.debug("Making directory " + config.image_path)

    if not os.path.exists(f"{config.image_path}/subImages"):
        os.makedirs(f"{config.image_path}/subImages")
        logging.debug("Making directory " + f"{config.image_path}/subImages")

    fig_Ve.savefig(
        f"{config.image_path}/subImages/Velocity_{filename.strip('.csv')}.png"
    )
    fig_Va.savefig(f"{config.image_path}/subImages/Vacuum_{filename.strip('.csv')}.png")
    fig_Dp.savefig(
        f"{config.image_path}/subImages/Discharge_Pressure_{filename.strip('.csv')}.png"
    )
    fig_Ps.savefig(
        f"{config.image_path}/subImages/Pump_Speed_{filename.strip('.csv')}.png"
    )
    fig_De.savefig(f"{config.image_path}/subImages/Depth_{filename.strip('.csv')}.png")

    velocity = Image.open(
        f"{config.image_path}/subImages/Velocity_{filename.strip('.csv')}.png"
    )
    vacuum = Image.open(
        f"{config.image_path}/subImages/Vacuum_{filename.strip('.csv')}.png"
    )
    discharge = Image.open(
        f"{config.image_path}/subImages/Discharge_Pressure_{filename.strip('.csv')}.png"
    )
    pump_speed = Image.open(
        f"{config.image_path}/subImages/Pump_Speed_{filename.strip('.csv')}.png"
    )
    depth = Image.open(
        f"{config.image_path}/subImages/Depth_{filename.strip('.csv')}.png"
    )

    velocity_size = velocity.size
    combined = Image.new(
        "RGB", (velocity_size[0], 5 * velocity_size[1]), (250, 250, 250)
    )
    combined.paste(velocity, (0, 0))
    combined.paste(vacuum, (0, velocity_size[1]))
    combined.paste(discharge, (0, 2 * velocity_size[1]))
    combined.paste(pump_speed, (0, 3 * velocity_size[1]))
    combined.paste(depth, (0, 4 * velocity_size[1]))
    combined.save(
        f"{config.image_path}/Smoke_Chart_{filename.strip('.csv')}.png", "PNG"
    )


if __name__ == "__main__":
    filename = "2021-10-13.csv"
    generateGraph(filename, True)
