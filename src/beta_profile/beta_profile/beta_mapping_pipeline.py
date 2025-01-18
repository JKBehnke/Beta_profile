""" Code to run the beta mapping pipeline. """

import mne
import numpy as np
import pandas as pd
import scipy
import os
import warnings
import matplotlib.pyplot as plt

from ..utils import find_folders as find_folders
from ..utils import io as io

from ..beta_profile import time_series_ecg_artifact as time_series
from ..beta_profile import power_spectra_plots as power_spectra
from ..beta_profile import tfr_plots as tfr_plots
from ..beta_profile import calculate_features

HEMISPHERES = ["Right", "Left"]
FREQ_BANDS = ["beta", "high_beta", "low_beta"]

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


####### 0. Get the Excel sheet with artifacts info #######
def get_artifacts_excel():
    """
    Load the excel file "artifacts_present.xlsx" from the data folder in Beta_mapping
    """

    # find the path to the results folder
    path = find_folders.get_local_path(folder="data")

    # load the file
    filename = "artifacts_peak_details.xlsx"
    filepath = os.path.join(path, filename)

    # load the file
    ecg_artifact_df = pd.read_excel(
        filepath, keep_default_na=True, sheet_name="artifacts"
    )
    print("Excel file loaded: ", filename, "\nloaded from: ", path)

    return ecg_artifact_df


def save_updated_artifacts_excel(updated_df):
    """
    Save the updated excel file with the new row added.

    Input:
        - artifacts_df: pd.DataFrame -> dataframe with the ecg artifacts
        - new_row: dict -> {"subject": str, "hemisphere": str, "session": str, "condition": str, "channel_group": str, "ecg_artifact": str, "movement_artifact": str}
    """

    # find the path to the results folder
    path = find_folders.get_local_path(folder="data")

    # load the file
    filename = "artifacts_peak_details.xlsx"
    filepath = os.path.join(path, filename)

    updated_df.to_excel(filepath, index=False, sheet_name="artifacts")
    print("Excel file updated: ", filename, "\nloaded from: ", path)

    return updated_df


def get_input_y_n(message: str) -> str:
    """Get `y` or `n` user input."""
    try:
        while True:
            user_input = input(f"{message} (y/n)? ")
            if user_input.lower() in ["y", "n"]:
                break
            print(
                f"Input must be `y` or `n`. Got: {user_input}."
                " Please provide a valid input."
            )
        return user_input
    except KeyboardInterrupt:
        print("Operation cancelled by the user (Ctrl+C).")
        return "canceled"


def get_comment(message: str) -> str:
    """Get comment from user."""
    while True:
        user_input = input(f"{message} ")
        if user_input:
            break
        print("Please type 'n' for no comments.")
    return user_input


####### 1. Load data and plot: unfiltered time series, Power spectra and Time frequency plots - save in raw folder (including calculated features: beta profile) #######
def plot_and_clean_raw_data(sub: str, hemisphere: str, session: str, condition: str):
    """
    Input:
    - sub: str -> "017"
    - hemisphere: str -> "Right"
    - session: str -> "Fu12m"
    - condition: str -> "m0s0"

    Plot raw data: unfiltered time series, Power spectra and Time frequency plots
    - save in raw folder
    - including calculated features: beta profile
    """

    # Suppress all warnings
    warnings.filterwarnings("ignore")

    artifacts_peak_details = get_artifacts_excel()
    ecg_artifact_input = {}
    movement_artifact_input = {}
    beta_peak_input = {}
    double_beta_peak_input = {}

    ### MAKE SURE TO SHOW THE PLOTS IN THE NOTEBOOK (plt.show(block=False)) ###
    for group in CHANNEL_GROUPS.keys():
        plot_raw_time_series = time_series.plot_ieeg_data(
            sub=sub,
            session=session,
            condition=condition,
            hemisphere=hemisphere,
            group=group,
            sub_folder="raw",
        )

    time_frequency = tfr_plots.plot_time_frequency(
        sub=sub,
        session=session,
        condition="m0s0",
        hemisphere=hemisphere,
        filtered="unfiltered",
        sub_folder="raw",
    )

    # are there ecg artifacts?
    input_ecg_artifact_Ring = get_input_y_n(
        "Are there ECG artifacts in the Ring channels?"
    )
    input_ecg_artifact_SegmInter = get_input_y_n(
        "Are there ECG artifacts in the SegmInter channels?"
    )
    input_ecg_artifact_SegmIntra = get_input_y_n(
        "Are there ECG artifacts in the SegmIntra channels?"
    )

    ecg_artifact_input = {
        "Ring": input_ecg_artifact_Ring,
        "SegmInter": input_ecg_artifact_SegmInter,
        "SegmIntra": input_ecg_artifact_SegmIntra,
    }

    # are there movement artifacts?
    input_movement_artifact_Ring = get_input_y_n(
        "Are there movement artifacts in the Ring channels?"
    )
    input_movement_artifact_SegmInter = get_input_y_n(
        "Are there movement artifacts in the SegmInter channels?"
    )
    input_movement_artifact_SegmIntra = get_input_y_n(
        "Are there movement artifacts in the SegmIntra channels?"
    )

    movement_artifact_input = {
        "Ring": input_movement_artifact_Ring,
        "SegmInter": input_movement_artifact_SegmInter,
        "SegmIntra": input_movement_artifact_SegmIntra,
    }

    power_spectra_plot = power_spectra.plot_power_spectra(
        sub=sub,
        session=session,
        condition=condition,
        hemisphere=hemisphere,
        sub_folder="raw",
    )

    # is beta peak present?
    input_beta_peak_Ring = get_input_y_n("Is beta peak present in Ring channels?")
    input_beta_peak_SegmInter = get_input_y_n(
        "Is beta peak present in SegmInter channels?"
    )
    input_beta_peak_SegmIntra = get_input_y_n(
        "Is beta peak present in SegmIntra channels?"
    )

    beta_peak_input = {
        "Ring": input_beta_peak_Ring,
        "SegmInter": input_beta_peak_SegmInter,
        "SegmIntra": input_beta_peak_SegmIntra,
    }

    # is double beta peak present?
    input_double_beta_peak_Ring = get_input_y_n(
        "Is double beta peak present in Ring channels?"
    )
    input_double_beta_peak_SegmInter = get_input_y_n(
        "Is double beta peak present in SegmInter channels?"
    )
    input_double_beta_peak_SegmIntra = get_input_y_n(
        "Is double beta peak present in SegmIntra channels?"
    )

    double_beta_peak_input = {
        "Ring": input_double_beta_peak_Ring,
        "SegmInter": input_double_beta_peak_SegmInter,
        "SegmIntra": input_double_beta_peak_SegmIntra,
    }

    # any comments?
    comments = get_comment("Any comments? ")

    # save new row in the excel file
    for group in CHANNEL_GROUPS.keys():
        new_row = {
            "subject": sub,
            "hemisphere": hemisphere,
            "session": session,
            "condition": condition,
            "channel_group": group,
            "ecg_artifact": ecg_artifact_input[group],
            "movement_artifact": movement_artifact_input[group],
            "beta_peak_present": beta_peak_input[group],
            "double_beta_peak": double_beta_peak_input[group],
            "comment": comments,
        }
        new_row = pd.DataFrame([new_row], index=[0])
        artifacts_peak_details = pd.concat(
            [artifacts_peak_details, new_row], ignore_index=True
        )

    # save the updated excel file
    save_updated_artifacts_excel(artifacts_peak_details)

    # write tfr and psd data to pickle file
    lfp_data = io.save_tfr_and_psd_to_pickle(
        sub=sub,
        session=session,
        condition=condition,
        hemisphere=hemisphere,
        sub_folder="raw",
    )

    for fq_band in FREQ_BANDS:

        beta_file = calculate_features.write_beta_profile(
            sub=sub,
            session=session,
            condition=condition,
            beta_range=fq_band,
            sub_folder="raw",
        )

    ####### Do you wish to perform ECG cleaning? ########
    ecg_cleaning_performed = get_input_y_n("Do you wish to perform ECG cleaning?")

    ####### For unclean data, first run the ECG cleaning script and save run the plotting pipeline again for the clean data #######
    if ecg_cleaning_performed == "y":

        # run the ECG cleaning script
        ecg_artifact_df, clean_time_series_df = time_series.ecg_cleaning(
            sub=sub, hem=hemisphere, session=session, condition=condition
        )

        # save the clean data and new clean plots in the clean folder
        for group in CHANNEL_GROUPS.keys():
            plot_raw_time_series = time_series.plot_ieeg_data(
                sub=sub,
                session=session,
                condition=condition,
                hemisphere=hemisphere,
                group=group,
                sub_folder="clean",
                cleaned_data=clean_time_series_df,
            )

        time_frequency = tfr_plots.plot_time_frequency(
            sub=sub,
            session=session,
            condition="m0s0",
            hemisphere=hemisphere,
            filtered="unfiltered",
            sub_folder="clean",
            cleaned_data=clean_time_series_df,
        )

        power_spectra_plot = power_spectra.plot_power_spectra(
            sub=sub,
            session=session,
            condition=condition,
            hemisphere=hemisphere,
            sub_folder="clean",
            cleaned_data=clean_time_series_df,
        )

        # write tfr and psd data to pickle file
        lfp_data = io.save_tfr_and_psd_to_pickle(
            sub=sub,
            session=session,
            condition=condition,
            hemisphere=hemisphere,
            sub_folder="clean",
            cleaned_data=clean_time_series_df,
        )

        for fq_band in FREQ_BANDS:

            beta_file = calculate_features.write_beta_profile(
                sub=sub,
                session=session,
                condition=condition,
                beta_range=fq_band,
                sub_folder="clean",
                cleaned_data=clean_time_series_df,
            )

    ####### If all data is clean, save all files in the clean folder #######
    elif ecg_cleaning_performed == "n":
        print("Data is clean.")

        # save all original data in the clean folder
        for group in CHANNEL_GROUPS.keys():
            plot_raw_time_series = time_series.plot_ieeg_data(
                sub=sub,
                session=session,
                condition=condition,
                hemisphere=hemisphere,
                group=group,
                sub_folder="clean",
            )

        time_frequency = tfr_plots.plot_time_frequency(
            sub=sub,
            session=session,
            condition="m0s0",
            hemisphere=hemisphere,
            filtered="unfiltered",
            sub_folder="clean",
        )

        power_spectra_plot = power_spectra.plot_power_spectra(
            sub=sub,
            session=session,
            condition=condition,
            hemisphere=hemisphere,
            sub_folder="clean",
        )

        # write tfr and psd data to pickle file
        lfp_data = io.save_tfr_and_psd_to_pickle(
            sub=sub,
            session=session,
            condition=condition,
            hemisphere=hemisphere,
            sub_folder="clean",
        )

        for fq_band in FREQ_BANDS:

            beta_file = calculate_features.write_beta_profile(
                sub=sub,
                session=session,
                condition=condition,
                beta_range=fq_band,
                sub_folder="clean",
            )

    # close all plots in Jupyter Notebook
    plt.clf()
    plt.close("all")
