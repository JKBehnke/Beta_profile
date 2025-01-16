""" Loads and saves data"""

import os
import re
import pandas as pd
from mne.io import read_raw_fieldtrip

# PyPerceive Imports
from PerceiveImport.classes import main_class
from ..beta_profile import tfr_preprocessing as tfr

from ..utils import find_folders as find_folders

LFP_GROUPS = {
    "Right": ["RingR", "SegmIntraR", "SegmInterR"],
    "Left": ["RingL", "SegmIntraL", "SegmInterL"],
}

RUNS = ["run-1", "run-2", "run-3", "run-4"]


def load_sub_path(sub: str):
    """
    Loading the path to the diectory:
        - Percept_Data_structured/beta_data/sub-XXX

    Input:
        - sub: "024"
    """

    sub_path = find_folders.get_onedrive_path(folder="beta_mapping_project")
    sub_path = os.path.join(sub_path, f"sub-{sub}")

    return sub_path


def check_or_create_sub_path(sub: str):
    """
    Checks if the sub-XXX folder exists and creates it if it doesn't
    """

    sub_path = load_sub_path(sub=sub)

    if not os.path.exists(sub_path):
        os.makedirs(sub_path)

    return sub_path


############### using NeuroCure Dataset to load data ####################
def find_sessions_per_sub(condition: str, modality: str):
    """
    This code will search through the Neurocure dataset (v3) and provide a dataframe with all available sessions in
    a specific condition ("MedOff" or "MedOn") per subject.
    """

    sessions_list = []
    sub_session_dict = {}

    modality_dict = {"survey": "LMTD", "indefinite_streaming": "IS"}

    # check if input condition is in ["MedOFF", "MedOn"]
    if condition not in ["MedOff", "MedOn"]:
        raise ValueError("condition must be either 'MedOff' or 'MedOn'")

    neuro_cure_path = find_folders.get_onedrive_path(folder="neuro_cure")

    for sub in os.listdir(neuro_cure_path):
        # check which sessions exist:
        session_pattern = r"Fu\d{2}m"
        available_sessions = []

        subject_path = os.path.join(neuro_cure_path, sub)  # e.g. sub-017
        if os.path.isdir(subject_path) and sub.startswith("sub-"):

            # check if condition exists
            for ses_folder in os.listdir(subject_path):
                if ses_folder.endswith(condition):
                    # search for all available sessions in the correct condition
                    match = re.search(session_pattern, ses_folder)
                    if match:
                        available_sessions.append(match.group())

                    session_path = os.path.join(subject_path, ses_folder, "ieeg")

                    # check if modality exists
                    modality_files = [
                        file
                        for file in os.listdir(session_path)
                        if modality_dict[modality] in file and file.endswith(".mat")
                    ]
                    modality_exists = bool(modality_files)

                    sessions_list.append(
                        {
                            "subject": sub,
                            "session_folder": ses_folder,
                            "session_path": session_path,
                            "modality_exists": modality_exists,
                            "modality_files": modality_files,
                        }
                    )

                    sub_session_dict[sub] = available_sessions

    session_path_dataframe = pd.DataFrame(sessions_list)

    # order the dictionary by subject numbers
    sub_session_dict = dict(sorted(sub_session_dict.items()))

    return session_path_dataframe, sub_session_dict


def load_neuro_cure_object(
    sub: str, session: str, condition: str, modality: str, hemisphere: str = None
):
    """
    Load specifically data from one subject, session, condition, modality and hemisphere

    Provides all files for both hemispheres.

    For surveys: 3 channel groups per hemisphere: RingR, SegmIntraR, SegmInterR
    For indefinite_streaming: Ring channel group only

    If there are more than run-1, only the highest run is kept.
    """

    modality_dict = {"survey": "LMTD", "indefinite_streaming": "IS"}
    # Validate modality input
    if modality not in modality_dict:
        raise ValueError(
            "Invalid modality. Must be 'survey' or 'indefinite_streaming'."
        )

    if condition == "m0s0":
        condition = "MedOff"
    elif condition == "m1s0":
        condition = "MedOn"

    file_paths = []
    lfp_group_data = {}
    indef_streaming_data = {}
    run_info = {}

    neuro_cure_path = find_folders.get_onedrive_path(folder="neuro_cure", sub=sub)
    if not os.path.exists(neuro_cure_path):
        raise FileNotFoundError(f"Subject folder not found: {neuro_cure_path}")

    session_found = False  # Flag to check if the session exists

    for ses_folder in os.listdir(neuro_cure_path):

        if session in ses_folder and ses_folder.endswith(condition):
            session_found = True  # Session found
            session_path = os.path.join(neuro_cure_path, ses_folder, "ieeg")

            # check if modality exists
            modality_files = [
                file
                for file in os.listdir(session_path)
                if modality_dict[modality] in file and file.endswith(".mat")
            ]

            if modality_files:
                for file in modality_files:
                    file_paths.append(os.path.join(session_path, file))

    # Error if session wasn't found
    if not session_found:
        raise FileNotFoundError(
            f"Session '{session}' with condition '{condition}' not found for subject {sub}."
        )

    ### load the data
    if modality == "survey":
        for lfp_group in LFP_GROUPS[hemisphere]:
            for f in file_paths:

                for run in RUNS:  # always just keep hightest run (probably the best)
                    if run in f:
                        if lfp_group in f:
                            data = read_raw_fieldtrip(f, info={}, data_name="data")
                            lfp_group_data[lfp_group] = data
                            run_info[lfp_group] = run

    if modality == "indefinite_streaming":
        for f in file_paths:
            if "Ring" in f:

                # check if there are more than 1 run
                for run in RUNS:
                    if run in f:
                        data = read_raw_fieldtrip(f, info={}, data_name="data")
                        indef_streaming_data[run] = data

    return {
        "file_paths": file_paths,
        "lfp_group_data": lfp_group_data,
        "indef_streaming_data": indef_streaming_data,
    }


############### using PyPerceive to load data ####################


def load_py_perceive_object(sub: str, session: str, condition: str, hemisphere: str):
    """
    Loading the MNE object of the BrainSense Survey of the given input through PyPerceive

    """
    return main_class.PerceiveData(
        sub=sub,
        incl_modalities=["survey"],
        incl_session=[session],
        incl_condition=[condition],
        incl_task=["rest"],
        incl_contact=LFP_GROUPS[hemisphere],
    )


def extract_data_from_py_perceive(
    sub: str,
    session: str,
    condition: str,
    hemisphere: str,
):
    """
    This function first checks if the data exists and then extracts the LFP of interest from the PyPerceive MNE object
    """

    lfp_group_data = {}

    # load the MNE object
    mainclass_object = load_py_perceive_object(
        sub=sub, session=session, condition=condition, hemisphere=hemisphere
    )

    for lfp_group in LFP_GROUPS[hemisphere]:

        # check if attributes exist
        if getattr(mainclass_object.survey, session) is None:
            print(f"session {session} doesn't exist for sub-{sub}")

        else:
            lfp_data = getattr(mainclass_object.survey, session)

        if getattr(lfp_data, condition) is None:
            print(
                f"condition {condition} doesn't exist for sub-{sub}, session {session}"
            )

        else:
            lfp_data = getattr(lfp_data, condition)
            lfp_data = getattr(lfp_data.rest, lfp_group)
            lfp_data = (
                lfp_data.run1.data
            )  # gets the mne loaded data from the perceive .mat BSSu, m0s0 file

            # save in a dictionary with keys "RingR", "SegmIntraR", "SegmInterR"
            lfp_group_data[lfp_group] = lfp_data

    return lfp_group_data


def save_fig_jpeg(sub: str, filename: str, figure=None):
    """
    Input:
        - path: str
        - filename: str
        - figure: must be a plt figure

    """
    path = check_or_create_sub_path(sub=sub)

    figure.savefig(
        os.path.join(path, f"{filename}.jpg"),
        bbox_inches="tight",
        format="jpeg",
        dpi=300,
    )

    print(f"Figure {filename}.jpg", f"\nwere written in: {path}.")


def save_df_as_excel(sub: str, filename: str, file: pd.DataFrame, sheet_name: str):
    """ """

    path = check_or_create_sub_path(sub=sub)
    filepath = os.path.join(path, f"{filename}.xlsx")

    file.to_excel(filepath, sheet_name=sheet_name, index=False)


def save_df_to_excel_sheets(sub: str, filename: str, file: dict):
    """ """
    sheet_names = ["Right_Ring", "Right_Segm", "Left_Ring", "Left_Segm"]

    path = check_or_create_sub_path(sub=sub)
    filepath = os.path.join(path, f"{filename}.xlsx")

    # write each dataframe to separate Excel sheet
    with pd.ExcelWriter(filepath) as writer:

        for sheet in sheet_names:
            file[sheet].to_excel(writer, sheet_name=sheet, index=False)


def save_tfr_and_psd_to_pickle(sub: str, session: str, condition: str, hemisphere: str):
    """
    Saves the TFR and PSD data as pickle files

    - peak details: channel, f_range, power_in_f_range, peak_CF, peak_power, peak_4Hz_power
    - time series and power details: channel, unfiltered_lfp, filtered_lfp, frequencies, filtered_psd
    """

    # sub path
    sub_path = check_or_create_sub_path(sub=sub)

    # load the data
    beta_profile = tfr.main_tfr(
        sub=sub, session=session, condition=condition, hemisphere=hemisphere
    )

    # save the data as pickle files
    beta_profile[0].to_pickle(
        os.path.join(
            sub_path,
            f"peak_details_sub-{sub}_hem-{hemisphere}_ses-{session}_cond-{condition}.pkl",
        )
    )

    beta_profile[1].to_pickle(
        os.path.join(
            sub_path,
            f"time_series_and_power_details_sub-{sub}_hem-{hemisphere}_ses-{session}_cond-{condition}.pkl",
        )
    )

    print(f"Data saved in {sub_path}")
    return beta_profile[0], beta_profile[1]
