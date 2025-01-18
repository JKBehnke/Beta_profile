""" ECG artifact cleaning """

import matplotlib.pyplot as plt
import os
import pandas as pd
import numpy as np
import pickle
from sklearn.decomposition import FastICA
import warnings
import mne

from ..utils import io as io
from ..utils import find_folders as find_folders
from . import tfr_preprocessing as tfr_preprocessing


HEMISPHERES = ["Right", "Left"]


PICK_CHANNELS = {
    "Ring": ["01", "12", "23", "02", "13"],
    "SegmInter": ["1A2A", "1B2B", "1C2C"],
    "SegmIntra": ["1A1B", "1A1C", "1B1C", "2A2B", "2A2C", "2B2C"],
}

CH_GROUPS = ["Ring", "SegmInter", "SegmIntra"]
LFP_GROUPS = {
    "Right": ["RingR", "SegmIntraR", "SegmInterR"],
    "Left": ["RingL", "SegmIntraL", "SegmInterL"],
}

CHANNELNAMES_MAPPING = {
    "LFP_Stn_0_3_": "03",
    "LFP_Stn_1_3_": "13",
    "LFP_Stn_0_2_": "02",
    "LFP_Stn_1_2_": "12",
    "LFP_Stn_0_1_": "01",
    "LFP_Stn_2_3_": "23",
    "LFP_Stn_1_A_1_B_": "1A1B",
    "LFP_Stn_1_A_1_C_": "1A1C",
    "LFP_Stn_1_B_1_C_": "1B1C",
    "LFP_Stn_2_A_2_B_": "2A2B",
    "LFP_Stn_2_A_2_C_": "2A2C",
    "LFP_Stn_2_B_2_C_": "2B2C",
    "LFP_Stn_1_A_2_A_": "1A2A",
    "LFP_Stn_1_B_2_B_": "1B2B",
    "LFP_Stn_1_C_2_C_": "1C2C",
}


def plot_ieeg_data(
    sub: str,
    hemisphere: str,
    condition: str,
    session: str,
    group: str,
    sub_folder: str = None,
    cleaned_data: pd.DataFrame = None,
):
    """
    Function to plot the iEEG data. This function can be used when you have already extracted the data into a 2D array.

    Input:
        - ieeg_data: np.array -> 2D array shape: (n_channels, n_samples)
        - sub_folder: e.g."ecg_cleaning", "clean", "raw" -> if "yes" the data will be saved into a ecg folder in the subject folder,
                        otherwise it will be saved in the subject folder directly
    """

    try:
        plt.style.use("seaborn-whitegrid")
    except OSError as e:
        if "'seaborn-whitegrid' is not a valid package style" not in str(e):
            raise e
        plt.style.use("seaborn-v0_8-whitegrid")

    # load psd
    beta_profile = tfr_preprocessing.main_tfr(
        sub=sub, session=session, condition=condition, hemisphere=hemisphere
    )

    clean_mark = ""

    if cleaned_data is not None:
        beta_profile = tfr_preprocessing.main_tfr_clean_data(cleaned_data=cleaned_data)
        clean_mark = "_cleaned"

    power_details = beta_profile[1]

    # for group in CH_GROUPS:

    channels = PICK_CHANNELS[group]
    fig_size = (40, 30)

    fig, axes = plt.subplots(
        len(channels), 1, figsize=fig_size
    )  # subplot(rows, columns, panel number), figsize(width,height)
    plt.subplots_adjust(wspace=0, hspace=0)
    fig.suptitle(
        f"Unfiltered time series sub-{sub}, {hemisphere} hemisphere, {session} session, {condition}, {group}",
        ha="center",
        fontsize=40,
    )

    fs = 250  # sampling frequency

    for i, ch in enumerate(channels):

        ch_unfiltered_lfp = power_details.loc[power_details.channel == ch]
        signal_data = ch_unfiltered_lfp.unfiltered_lfp.values[0]

        time_vector = np.arange(len(signal_data)) / fs

        #################### PLOT THE CHOSEN PSD DEPENDING ON NORMALIZATION INPUT ####################

        axes[i].set_title(f"Channel {ch}", fontsize=30)
        axes[i].plot(time_vector, signal_data, label=f"{ch}", color="k", linewidth=0.5)

    for ax in axes:
        ax.set_xlabel("Time [sec]", fontsize=30)
        ax.set_ylabel("Amplitude", fontsize=30)
        ax.tick_params(axis="both", which="major", labelsize=30)

    for ax in axes.flat[:-1]:
        ax.set(xlabel="")

    fig.tight_layout()
    plt.subplots_adjust(wspace=0, hspace=0)
    plt.show(block=False)

    # save figure
    filename = f"unfiltered_time_series_sub-{sub}_hem-{hemisphere}_ses-{session}_cond-{condition}_group-{group}{clean_mark}"

    # if sub_folder is given, save the figure in the sub_folder
    if sub_folder:
        # find the path to the results folder
        io.save_fig_jpeg(sub=sub, filename=filename, figure=fig, sub_folder=sub_folder)

    else:
        io.save_fig_jpeg(sub=sub, filename=filename, figure=fig)

    return {"data": power_details, "channels": channels}


## plot cleaned data
def plot_ieeg_data_cleaned(
    sub: str,
    hemisphere: str,
    session: str,
    condition: str,
    group: str,
    channels: list,
    ieeg_data: np.array,
    fig_title: str,
):
    """
    - ieeg_data: np.array -> 2D array shape: (n_channels, n_samples)
    - figure_title: str ->
    """

    try:
        plt.style.use("seaborn-whitegrid")
    except OSError as e:
        if "'seaborn-whitegrid' is not a valid package style" not in str(e):
            raise e
        plt.style.use("seaborn-v0_8-whitegrid")

    # find the path to the results folder
    sub_path = io.check_or_create_sub_path(sub)
    sub_ecg_path = os.path.join(sub_path, "ecg_cleaning")
    # check if exists, otherwise create folder
    if not os.path.exists(sub_ecg_path):
        os.makedirs(sub_ecg_path)

    fig_size = (40, 30)

    fig, axes = plt.subplots(
        len(channels), 1, figsize=fig_size
    )  # subplot(rows, columns, panel number), figsize(width,height)
    plt.subplots_adjust(wspace=0, hspace=0)
    fig.suptitle(
        f"{fig_title} time series sub-{sub}, {hemisphere} hemisphere, {session} session, {condition}, {group}",
        ha="center",
        fontsize=40,
    )

    fs = 250  # sampling frequency

    for i, ch in enumerate(channels):

        signal_data = ieeg_data[i, :]

        time_vector = np.arange(len(signal_data)) / fs

        #################### PLOT THE CHOSEN PSD DEPENDING ON NORMALIZATION INPUT ####################

        axes[i].set_title(f"Channel {ch}", fontsize=30)
        axes[i].plot(time_vector, signal_data, label=f"{ch}", color="k", linewidth=0.5)

    for ax in axes:
        ax.set_xlabel("Time [sec]", fontsize=30)
        ax.set_ylabel("Amplitude", fontsize=30)
        ax.tick_params(axis="both", which="major", labelsize=30)

    for ax in axes.flat[:-1]:
        ax.set(xlabel="")

    fig.tight_layout()
    plt.subplots_adjust(wspace=0, hspace=0)
    plt.show(block=False)

    # save figure
    filename = f"{fig_title}_time_series_sub-{sub}_hem-{hemisphere}_ses-{session}_cond-{condition}_group-{group}"

    fig.savefig(
        os.path.join(
            sub_ecg_path,
            filename + ".jpg",
        ),
        bbox_inches="tight",
    )
    # io.save_fig_jpeg(sub=sub, filename=filename, figure=fig)

    return {"data": ieeg_data, "channels": channels}


################## General functions for ECG artifact cleaning ##################
def get_ecg_artifact_excel():
    """
    Load the excel file "ecg_artifacts.xlsx" from the data folder > ecg_cleaning folder
    """

    # find the path to the results folder
    path = find_folders.get_local_path(folder="data")

    # go into ecg cleaning folder
    path = os.path.join(path, "ecg_cleaning")

    # load the file
    filename = "ecg_artifacts.xlsx"
    filepath = os.path.join(path, filename)

    # load the file
    ecg_artifact_df = pd.read_excel(
        filepath, keep_default_na=True, sheet_name="ecg_artifacts"
    )
    print("Excel file loaded: ", filename, "\nloaded from: ", path)

    return ecg_artifact_df


def save_updated_excel(updated_df):
    """
    Save the updated excel file with the new row added.

    Input:
        - ecg_artifact_df: pd.DataFrame -> dataframe with the ecg artifacts
        - new_row: dict -> {"subject": str, "session": str, "channel_group": str, "ecg_component": int, "cleaned": str, "comment": str}
    """

    # find the path to the results folder
    path = find_folders.get_local_path(folder="data")

    # go into ecg cleaning folder
    path = os.path.join(path, "ecg_cleaning")

    # load the file
    filename = "ecg_artifacts.xlsx"
    filepath = os.path.join(path, filename)

    updated_df.to_excel(filepath, index=False, sheet_name="ecg_artifacts")
    print("Excel file updated: ", filename, "\nloaded from: ", path)

    return updated_df


def get_input_y_n(message: str) -> str:
    """Get `y` or `n` user input."""
    while True:
        user_input = input(f"{message} (y/n)? ")
        if user_input.lower() in ["y", "n"]:
            break
        print(
            f"Input must be `y` or `n`. Got: {user_input}."
            " Please provide a valid input."
        )
    return user_input


def get_input_ecg_component(message: str) -> str:
    """Get integer of ecg component user input."""
    while True:
        user_input = input(f"{message} (integer)? 0 if none.")
        if int(user_input) in {0, 1, 2, 3, 4, 5, 6}:
            break
        print(
            f"Input must be an integer from 0 to 6. Got: {user_input}."
            " Please provide a valid input."
        )
    return int(user_input)


def fit_ica_on_channel_group(data):
    """
    Function to fit ICA on the raw data of one channel group.

    Input: mne_object.get_data() -> 2D array shape: (n_channels, n_samples)

    """

    # first transpose the data to fit the input of FastICA
    data_to_fit = data.T

    # initialize ICA
    n_components = data.shape[
        0
    ]  # number of channels (only so many components can be estimated)

    ica = FastICA(n_components=n_components, random_state=97)  # why 97?

    # fit ICA model (fit) and transform the data into the independent components (transform)
    ica_components = ica.fit_transform(data_to_fit)

    return ica_components, n_components, ica


def plot_ica_components(data):
    """
    Function to plot the independent components of the ICA.

    Input: mne_object.get_data() -> 2D array shape: (n_channels, n_samples)

    """
    try:
        plt.style.use("seaborn-v0_8-whitegrid")
    except OSError as e:
        print("Seaborn style not found. Using default style.")
        plt.style.use("default")

    # fit the ICA model and get components
    ica_components, n_components, ica = fit_ica_on_channel_group(data)

    if n_components == 6:
        fig_size = (30, 10)

    elif n_components == 3:
        fig_size = (30, 5)

    time_points = np.arange(data.shape[1])  # Assuming your data is sampled uniformly
    fig, axes = plt.subplots(
        n_components, 1, figsize=fig_size, sharex=True, sharey=True
    )

    for i in range(n_components):
        axes[i].plot(
            time_points, ica_components[:, i], label=f"Component {i + 1}", linewidth=0.3
        )
        axes[i].set_title(f"Component {i + 1}", fontsize=15)
        axes[i].set_ylabel(f"Amplitude")

    axes[n_components - 1].set_xlabel("Time points")
    plt.tight_layout()
    plt.show()

    return {
        "fig_ecg_components": fig,
        "ica_components": ica_components,
        "n_components": n_components,
        "ica": ica,
    }


def remove_ecg_artifact_from_signals(
    data: np.array, ecg_component_index: int, ica_components: np.array, ica
):
    """
    Function to remove ECG artifact from the signals.

    Input:
        - ecg_component: int -> number of the independent component that represents the ECG artifact
        - data: np.array -> 2D array shape: (n_channels, n_samples)
        - ica_components: np.array -> 2D array shape: (n_samples, n_components)
        - ica: FastICA object

    Output:
        - cleaned_ieeg_data: np.array -> 2D array shape: (n_channels, n_samples)
    """

    # get the ecg component
    ecg_component = ica_components[:, ecg_component_index]

    # remove the ecg component from the data
    cleaned_ieeg_data = data.T - np.outer(
        ecg_component, ica.mixing_[:, ecg_component_index]
    )  # both shape (times x channels)

    # explained: ica.mixing_[:, ecg_component_index]: Retrieves the mixing coefficients corresponding to the ECG component. The ica.mixing_ matrix describes how the independent components are combined to form the observed data.
    # np.outer(ecg_component, ica.mixing_[:, ecg_component_index]): This is the outer product of the ECG component and the mixing coefficients. This gives the contribution of the ECG component to each channel at each time point.
    # This results in a matrix where each element is the product of the corresponding elements of ecg_component and the mixing coefficients.
    # - n.outer() subtracts the ECGF artifact contribution from the transposed data

    # Now, cleaned_ieeg_data contains the EEG data with the ECG artifact removed
    # Note: Depending on the scaling of the components, you might need to adjust the amplitude of the subtracted signal to achieve the desired artifact removal.
    # You may also need to experiment with the sign of the subtracted signal.
    # If the artifact is not completely removed, you can try multiplying the ECG component by a scaling factor before subtraction.

    return cleaned_ieeg_data.T


############################ SCRIPT TO CLEAN ALL ECG ARTIFACTS FROM THE DATA ############################


def ecg_cleaning(
    sub: str,
    hem: str,
    session: str,
    condition: str,
):
    """
    Input:
        - sub: str -> "017"
        - session: str -> "Fu12m"
        - condition: str -> "m0s0"

    Function to clean the ECG artifacts from the iEEG data of a subject.

    This function will iterate over all sessions and channel groups of a subject and clean the ECG artifacts from the iEEG data.
    It will check which session exist for a subject
    It will also check if the subject has a perceive error in any of the sessions. In case of a perceive error, the data will be loaded from the JSON file.
    Make sure to have the Report json in the data folder > source_json

    - Step 1: load and plot the raw time series
    - Step 2: fit ICA on the raw data and plot the components
    - Step 3: remove the ECG artifact from the signals
    - Step 4: plot the cleaned signals
    - Step 5: save the results
        in an Excel file ("ecg_artifacts.xlsx") in the data folder > ecg_cleaning folder
        and the cleaned signals in a pickle file ("cleaned_time_series.pickle") in the subjects results folder


    """

    # Suppress all warnings
    warnings.filterwarnings("ignore")

    # load the excel file with the ecg artifacts
    ecg_artifact_df = get_ecg_artifact_excel()

    # find the path to the results folder
    sub_path = io.check_or_create_sub_path(sub)
    sub_ecg_path = os.path.join(sub_path, "ecg_cleaning")
    # check if exists, otherwise create folder
    if not os.path.exists(sub_ecg_path):
        os.makedirs(sub_ecg_path)

    # dictionary to store the results
    clean_time_series_dict = {}

    # iterate over channel groups
    mne_object_data = io.load_neuro_cure_object(
        sub, session, condition, modality="survey", hemisphere=hem
    )
    for group in LFP_GROUPS[hem]:  # RingR, SegmIntraR, SegmInterR
        group_data = mne_object_data["lfp_group_data"][group]
        data = group_data.get_data()

        # rename channels
        for old_name in group_data.info.ch_names:
            for key, value in CHANNELNAMES_MAPPING.items():
                if key in old_name:
                    new_name = value
                    group_data.rename_channels({old_name: new_name})

        # get new channel names
        channels = group_data.info.ch_names

        ch_group = group[:-1]  # Ring, SegmIntra, SegmInter

        # Step 1: load and plot the raw time series ############################################
        # plot_ieeg_data(sub: str, hemisphere: str, condition: str, session: str, group: str):
        plot_raw = plot_ieeg_data(
            sub=sub,
            hemisphere=hem,
            condition=condition,
            session=session,
            group=ch_group,
            sub_folder="ecg_cleaning",
        )

        # extract the data and channels and hemisphere
        # data_as_df = plot_raw["data"]  # in 2D array shape: (n_channels, n_samples)
        # channels = plot_raw["channels"]

        # check if data contains ECG artifact
        input_y_or_n_artifact = get_input_y_n(
            "ECG artifacts found"
        )  # interrups run and asks for input

        if input_y_or_n_artifact == "n":

            # save new row in the excel file
            new_row = {
                "subject": sub,
                "hemisphere": hem,
                "session": session,
                "condition": condition,
                "channel_group": ch_group,
                "ecg_artifact": input_y_or_n_artifact,
                "ecg_component_first_run": 0,
                "ecg_component_second_run": 0,
                "cleaned": "n",
                "ieeg_saved": "original",
            }
            new_row = pd.DataFrame([new_row], index=[0])
            ecg_artifact_df = pd.concat([ecg_artifact_df, new_row], ignore_index=True)

            # keep the original data and continue
            clean_time_series_dict[f"{sub}_{hem}_{session}_{condition}_{ch_group}"] = [
                sub,
                hem,
                session,
                condition,
                ch_group,
                "no",
                data,
                channels,
            ]

            continue

        # Step 2: fit ICA on the raw data and plot the components ############################################
        plot_ica = plot_ica_components(
            data
        )  # transorm data to correct format: 2D array shape: (n_channels, n_samples)

        # save figure:
        plot_ica["fig_ecg_components"].savefig(
            os.path.join(
                sub_ecg_path,
                f"ica_components_sub-{sub}_{session}_{condition}_{group}.svg",
            ),
            bbox_inches="tight",
            format="svg",
        )
        plot_ica["fig_ecg_components"].savefig(
            os.path.join(
                sub_ecg_path,
                f"ica_components_sub-{sub}_{session}_{condition}_{group}.png",
            ),
            bbox_inches="tight",
        )

        # extract features from plot_ica
        ica_components = plot_ica["ica_components"]
        ica = plot_ica["ica"]

        # select the ECG component
        first_input_ecg_component = get_input_ecg_component(
            "Which component is the ECG artifact? (if none is obvious type 0 and save original)"
        )  # interrups run and asks for input
        if first_input_ecg_component in {1, 2, 3, 4, 5, 6}:
            first_ecg_component = first_input_ecg_component - 1  # index starts at 0

        elif first_input_ecg_component == 0:

            # save new row in the excel file
            new_row = {
                "subject": sub,
                "hemisphere": hem,
                "session": session,
                "condition": condition,
                "channel_group": ch_group,
                "ecg_artifact": "n",
                "ecg_component_first_run": first_input_ecg_component,
                "ecg_component_second_run": 0,
                "cleaned": "n",
                "ieeg_saved": "original",
            }
            new_row = pd.DataFrame([new_row], index=[0])
            ecg_artifact_df = pd.concat([ecg_artifact_df, new_row], ignore_index=True)

            # keep the original data and continue
            clean_time_series_dict[f"{sub}_{hem}_{session}_{condition}_{ch_group}"] = [
                sub,
                hem,
                session,
                condition,
                ch_group,
                "no",
                data,
                channels,
            ]

            continue

        else:
            print("Invalid input. Please provide a valid input.")
            break

        # Step 3: remove the ECG artifact from the signals ############################################
        cleaned_ieeg_data = remove_ecg_artifact_from_signals(
            data, first_ecg_component, ica_components, ica
        )

        # Step 4: plot the cleaned signals ############################################
        plot_cleaned = plot_ieeg_data_cleaned(
            sub=sub,
            hemisphere=hem,
            session=session,
            condition=condition,
            group=ch_group,
            channels=channels,
            ieeg_data=cleaned_ieeg_data,
            fig_title="cleaned",
        )

        # check if data now clean
        input_y_or_n_clean = get_input_y_n(
            "Data cleaned?"
        )  # interrups run and asks for input
        ieeg_saved = "cleaned"
        second_input_ecg_component = 0

        if input_y_or_n_clean == "n":
            second_input_y_or_n = get_input_y_n(
                "Try again?"
            )  # interrups run and asks for input

            # try a second time #############################################
            if second_input_y_or_n == "y":
                second_plot_ica = plot_ica_components(cleaned_ieeg_data)

                # save figure:
                second_plot_ica["fig_ecg_components"].savefig(
                    os.path.join(
                        sub_ecg_path,
                        f"second_run_ica_components_sub-{sub}_{session}_{condition}_{group}.png",
                    ),
                    bbox_inches="tight",
                )

                # extract features from plot_ica
                second_ica_components = second_plot_ica["ica_components"]
                second_ica = second_plot_ica["ica"]

                second_input_ecg_component = get_input_ecg_component(
                    "Which component is the ECG artifact?"
                )  # interrups run and asks for input
                if second_input_ecg_component in {1, 2, 3, 4, 5, 6}:
                    second_ecg_component = (
                        second_input_ecg_component - 1
                    )  # index starts at 0
                    # remove another component from the cleaned signals ############################################
                    cleaned_ieeg_data = remove_ecg_artifact_from_signals(
                        cleaned_ieeg_data,
                        second_ecg_component,
                        second_ica_components,
                        second_ica,
                    )

                    # Step 4: plot the cleaned signals ############################################
                    plot_cleaned = plot_ieeg_data_cleaned(
                        sub=sub,
                        hemisphere=hem,
                        session=session,
                        condition=condition,
                        group=ch_group,
                        channels=channels,
                        ieeg_data=cleaned_ieeg_data,
                        fig_title="second_run_cleaned",
                    )

            elif second_input_y_or_n == "n":
                second_input_ecg_component = 0

        # check if data now clean
        input_keep_original = get_input_y_n(
            "Do you want to keep the original? (type y if you want to keep original)"
        )  # interrups run and asks for input

        # if still not clean ask to keep original
        if input_keep_original == "y":
            cleaned_ieeg_data = data
            first_input_ecg_component = 0
            second_input_ecg_component = 0
            ieeg_saved = "original"

        elif input_keep_original == "n":
            ieeg_saved = "cleaned"

        # save new row in the excel file
        new_row = {
            "subject": sub,
            "hemisphere": hem,
            "session": session,
            "condition": condition,
            "channel_group": ch_group,
            "ecg_artifact": input_y_or_n_artifact,
            "ecg_component_first_run": first_input_ecg_component,
            "ecg_component_second_run": second_input_ecg_component,
            "cleaned": input_y_or_n_clean,
            "ieeg_saved": ieeg_saved,
        }
        new_row = pd.DataFrame([new_row], index=[0])
        ecg_artifact_df = pd.concat([ecg_artifact_df, new_row], ignore_index=True)

        clean_time_series_dict[f"{sub}_{hem}_{session}_{condition}_{ch_group}"] = [
            sub,
            hem,
            session,
            condition,
            ch_group,
            "yes",
            cleaned_ieeg_data,
            channels,
        ]

    # save the updated excel file
    save_updated_excel(ecg_artifact_df)

    # dataframe to store the results
    clean_time_series_df = pd.DataFrame(clean_time_series_dict)
    clean_time_series_df.rename(
        index={
            0: "subject",
            1: "hemisphere",
            2: "session",
            3: "condition",
            4: "channel_group",
            5: "ecg_artifact",
            6: "cleaned_time_series",
            7: "channels",
        },
        inplace=True,
    )
    clean_time_series_df = clean_time_series_df.transpose()

    # save the results as pickle
    results_filepath = os.path.join(
        sub_ecg_path, f"cleaned_time_series_survey_{condition}.pickle"
    )
    with open(results_filepath, "wb") as file:
        pickle.dump(clean_time_series_df, file)

    return ecg_artifact_df, clean_time_series_df
