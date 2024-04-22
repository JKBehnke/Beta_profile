""" Loads and saves data"""

import os
import numpy as np
import pandas as pd
import scipy

# PyPerceive Imports
from PerceiveImport.classes import main_class
from .. utils import find_folders as find_folders

LFP_GROUPS = {
    "Right": ["RingR", "SegmIntraR", "SegmInterR"],
    "Left": ["RingL", "SegmIntraL", "SegmInterL"]
}

def load_sub_path(sub:str):
    """
    Loading the path to the diectory:
        - ercept_Data_structured/beta_data/sub-XXX

    Input:
        - sub: "024"
    """

    sub_path = find_folders.get_onedrive_path_mac(folder="beta_data")
    sub_path = os.path.join(sub_path, f"sub-{sub}")

    return sub_path

def load_py_perceive_object(
        sub:str,
        session:str,
        condition:str,
        hemisphere:str

):
    """
    Loading the MNE object of the BrainSense Survey of the given input through PyPerceive
    
    """
    mainclass_sub = main_class.PerceiveData(
        sub = sub, 
        incl_modalities= ["survey"],
        incl_session = [session],
        incl_condition = [condition],
        incl_task = ["rest"],
        incl_contact=LFP_GROUPS[hemisphere]
        )
    
    return mainclass_sub


def extract_data_from_py_perceive(
        sub:str,
        session:str,
        condition:str,
        hemisphere:str,
):
    """
    This function first checks if the data exists and then extracts the LFP of interest from the PyPerceive MNE object
    """

    lfp_group_data = {}

    # load the MNE object
    mainclass_object = load_py_perceive_object(
        sub=sub,
        session=session,
        condition=condition,
        hemisphere=hemisphere
    )

    for lfp_group in LFP_GROUPS[hemisphere]:

        # check if attributes exist
        if getattr(mainclass_object.survey, session) is None:
            print(f"session {session} doesn't exist for sub-{sub}")
        
        else:
            lfp_data = getattr(mainclass_object.survey, session)

        
        if getattr(lfp_data, condition) is None:
            print(f"condition {condition} doesn't exist for sub-{sub}, session {session}")
        
        else:
            lfp_data = getattr(lfp_data, condition)
            lfp_data = getattr(lfp_data.rest, lfp_group)
            lfp_data = lfp_data.run1.data # gets the mne loaded data from the perceive .mat BSSu, m0s0 file 

            # save in a dictionary with keys "RingR", "SegmIntraR", "SegmInterR"
            lfp_group_data[lfp_group] = lfp_data
        
    return lfp_group_data

        



    
    
    





    

