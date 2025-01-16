""" Time Frequency Plots """

import matplotlib.pyplot as plt
from cycler import cycler

from ..utils import find_folders as find_folders
from ..utils import io as io
from . import tfr_preprocessing as tfr_preprocessing


PICK_CHANNELS = {
    "Ring_neighbours": ["01", "12", "23"],
    "Ring_sandwich": ["02", "13"],
    "Segm": ["1A1B", "1A1C", "1B1C", "2A2B", "2A2C", "2B2C", "1A2A", "1B2B", "1C2C"],
}

CHANNEL_GROUPS = {
    "Ring": ["01", "12", "23", "02", "13", "03"],
    "SegmInter": ["1A2A", "1B2B", "1C2C"],
    "SegmIntra": [
        "1A1B",
        "1A1C",
        "1B1C",
        "2A2B",
        "2A2C",
        "2B2C",
    ],
}

CONDITION_FILENAME = {
    "m0s0": "MedOFF-StimOFF",
    "m0s1": "MedOFF-StimON",
    "m1s0": "MedON-StimOFF",
    "m1s1": "MedON-StimON",
}

ALL_CHANNELS = [
    "01",
    "12",
    "23",
    "02",
    "13",
    "03",
    "1A1B",
    "1A1C",
    "1B1C",
    "2A2B",
    "2A2C",
    "2B2C",
    "1A2A",
    "1B2B",
    "1C2C",
]


def plot_time_frequency(
    sub: str, session: str, condition: str, hemisphere: str, filtered: str
):
    """
    Plot Time frequency plots either filtered "band_pass" or "unfiltered"


    1) load data from main_class.PerceiveData using the input values.

    2) band-pass filter by a Butterworth Filter of fifth order (5-95 Hz).

    3) Plot Time Frequency plot for each Channel of one session.

    """
    # load psd
    beta_profile = tfr_preprocessing.main_tfr(
        sub=sub, session=session, condition=condition, hemisphere=hemisphere
    )

    power_details = beta_profile[1]

    for group in CHANNEL_GROUPS.keys():

        channels = CHANNEL_GROUPS[group]
        n_channels = len(channels)  # Number of channels to plot

        # Dynamic figure size: width is constant, height scales with channels
        fig_width = 8  # Width of the figure
        fig_height_per_channel = 3  # Allocate 3 units of height per channel
        fig_height = n_channels * fig_height_per_channel

        fig, axes = plt.subplots(n_channels, 1, figsize=(fig_width, fig_height))

        # Ensure axes is always iterable
        if n_channels == 1:
            axes = [axes]

        plt.setp(axes, xlabel="Time [sec]", ylabel="Frequency [Hz]")
        fig.suptitle(
            f"Subject {sub}, Session {session}, {hemisphere} Hemisphere, {group} Group, {filtered}"
        )

        fig.tight_layout()
        fig.subplots_adjust(left=0.15, top=0.95)

        for i, ch in enumerate(channels):

            # get power details and frequencies for each channel
            ch_lfp_data = power_details.loc[power_details.channel == ch]

            time_series = (
                ch_lfp_data.filtered_lfp.values[0]
                if filtered == "band_pass"
                else ch_lfp_data.unfiltered_lfp.values[0]
            )

            # plot the time frequency plot
            axes[i].specgram(
                time_series,
                Fs=250,
                cmap=plt.get_cmap("viridis", 512),
                # cmap="viridis",
                vmin=-25,
                vmax=10,
            )
            axes[i].grid(False)
            axes[i].set_title(f"Channel {ch}", fontsize=15)
            axes[i].set_aspect("auto")  # Dynamic scaling

        # save figure
        io.save_fig_jpeg(
            sub=sub,
            filename=f"Time_Frequency_sub-{sub}_hem-{hemisphere}_ses-{session}_cond-{condition}_group-{group}_{filtered}",
            figure=fig,
        )
