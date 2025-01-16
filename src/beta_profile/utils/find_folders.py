""" Find folders """

import os
import sys

import numpy as np


def get_local_path(folder: str, sub: str = None):
    """
    find_project_folder is a function to find the folder "Beta_mapping" on your local computer

    Input:
        - folder: str
            'Research': path to Research folder
            'Beta_mapping': path to Project folder
            'GroupResults': path to results folder, without going in subject level
            'results': subject folder of results
            'GroupFigures': path to figures folder, without going in subject level
            'figures': figure folder of results

        - sub: str, e.g. "029"


    """

    folder_options = [
        "Project",
        "GroupResults",
        "results",
        "GroupFigures",
        "figures",
        "data",
    ]

    # Error checking, if folder input is in folder options
    # if folder.lower() not in folder_options:
    # raise ValueError(
    #     f'given folder: {folder} is incorrect, '
    #     f'should be {folder_options}')

    # from your cwd get the path and stop at 'Users'
    jennifer_user_path = os.getcwd()
    while jennifer_user_path[-14:] != "jenniferbehnke":
        jennifer_user_path = os.path.dirname(jennifer_user_path)

    project_path = os.path.join(
        jennifer_user_path, "Dropbox", "work", "ResearchProjects", "Beta_mapping"
    )

    # add the folder to the path and from there open the folders depending on input folder
    if folder == "Project":
        return project_path

    elif folder == "GroupResults":
        return os.path.join(project_path, "results")

    elif folder == "results":
        return os.path.join(project_path, "results", f"sub-{sub}")

    elif folder == "GroupFigures":
        return os.path.join(project_path, "figures")

    elif folder == "figures":
        return os.path.join(project_path, "figures", f"sub-{sub}")

    elif folder == "data":
        return os.path.join(project_path, "data")


# def get_onedrive_path(folder: str = 'onedrive',
#                       sub: str = None):
#     """
#     Device and OS independent function to find
#     the synced-OneDrive folder where data is stored
#     Folder has to be in ['onedrive', 'Percept_Data_structured', 'sourcedata']
#     """

#     folder_options = ['onedrive', 'sourcedata', 'beta_data']

#     # Error checking, if folder input is in folder options
#     if folder.lower() not in folder_options:
#         raise ValueError(f'given folder: {folder} is incorrect, ' f'should be {folder_options}')

#     # from your cwd get the path and stop at 'Users'
#     path = os.getcwd()

#     while os.path.dirname(path)[-5:] != 'Users':
#         path = os.path.dirname(path)  # path is now leading to Users/username

#     # get the onedrive folder containing "onedrive" and "charit" and add it to the path
#     onedrive_f = [f for f in os.listdir(path) if np.logical_and('onedrive' in f.lower(), 'charit' in f.lower())]

#     path = os.path.join(path, onedrive_f[0])  # path is now leading to Onedrive folder

#     # add the folder DATA-Test to the path and from there open the folders depending on input folder
#     datapath = os.path.join(path, 'Percept_Data_structured')
#     if folder == 'onedrive':
#         return datapath

#     elif folder == 'sourcedata':
#         return os.path.join(datapath, 'sourcedata')

#     elif folder == 'beta_data':
#         return os.path.join(datapath, 'beta_data')


# def get_onedrive_path_mac(folder: str = 'onedrive', sub: str = None):
#     """
#     Device and OS independent function to find
#     the synced-OneDrive folder where data is stored
#     Folder has to be in ['onedrive', 'Percept_Data_structured', 'sourcedata']
#     """

#     folder_options = ['onedrive', 'sourcedata', 'beta_data']

#     # Error checking, if folder input is in folder options
#     if folder.lower() not in folder_options:
#         raise ValueError(f'given folder: {folder} is incorrect, ' f'should be {folder_options}')

#     # from your cwd get the path and stop at 'Users'
#     path = os.getcwd()

#     while os.path.dirname(path)[-5:] != 'Users':
#         path = os.path.dirname(path)  # path is now leading to Users/username

#     # get the onedrive folder containing "charit" and add it to the path

#     path = os.path.join(path, 'Charité - Universitätsmedizin Berlin')

#     # onedrive_f = [
#     #     f for f in os.listdir(path) if np.logical_and(
#     #         'onedrive' in f.lower(),
#     #         'shared' in f.lower())
#     #         ]
#     # print(onedrive_f)

#     # path = os.path.join(path, onedrive_f[0]) # path is now leading to Onedrive folder

#     # add the folder DATA-Test to the path and from there open the folders depending on input folder
#     datapath = os.path.join(path, 'AG Bewegungsstörungen - Percept - Percept_Data_structured')
#     if folder == 'onedrive':
#         return datapath

#     elif folder == 'sourcedata':
#         return os.path.join(datapath, 'sourcedata')

#     elif folder == 'beta_data':
#         return os.path.join(datapath, 'beta_data')


def get_onedrive_path(folder: str = "onedrive", sub: str = None):
    """
    Device and OS independent function to find
    the synced-OneDrive folder where data is stored
    Folder has to be in ['onedrive', 'Percept_Data_structured', 'sourcedata']
    """

    folder_options = [
        "onedrive",
        "sourcedata",
        "beta_data_v2",
        "neuro_cure",
        "beta_mapping_project",
    ]

    # Error checking, if folder input is in folder options
    if folder.lower() not in folder_options:
        raise ValueError(
            f"given folder: {folder} is incorrect, " f"should be {folder_options}"
        )

    # from your cwd get the path and stop at 'Users'
    path = os.getcwd()

    for _ in range(20):
        if os.path.dirname(path)[-5:] != "Users":
            path = os.path.dirname(path)  # path is now leading to Users/username
    assert path != os.getcwd(), '"Users" path not found'

    ####### in a specific case, if the Percept_Data_structured folder is in a specific directory #######
    if np.logical_and(
        "Charité - Universitätsmedizin Berlin" in os.listdir(path),
        os.path.exists(
            os.path.join(
                path,
                "Charité - Universitätsmedizin Berlin",
                "AG Bewegungsstörungen - Percept - " "Percept_Data_structured",
            )
        ),
    ):

        # add the folder DATA-Test to the path and from there open the folders depending on input folder
        datapath = os.path.join(
            path,
            "Charité - Universitätsmedizin Berlin",
            "AG Bewegungsstörungen - Percept - Percept_Data_structured",
        )
        if folder == "onedrive":
            return datapath

        elif folder == "sourcedata":
            return os.path.join(datapath, "sourcedata")

        elif folder == "beta_data_v2":
            return os.path.join(datapath, "beta_data_v2")

        elif folder == "beta_mapping_project":
            return os.path.join(datapath, "beta_mapping_project")

        elif folder == "neuro_cure":
            path = os.path.join(datapath, "NeuroCure", "rawdata_v3")
            if sub:
                path = os.path.join(path, f"sub-{sub}")
            return path

    ####### this should be the general case #######
    else:
        # get the onedrive folder containing "onedrive" and "charit" and add it to the path
        onedrive_f = [
            f
            for f in os.listdir(path)
            if np.logical_and("onedrive" in f.lower(), "charit" in f.lower())
        ]
        path = os.path.join(
            path, onedrive_f[0]
        )  # path is now leading to Onedrive folder

        # add the folder name
        path = os.path.join(path, "Percept_Data_structured")
        if folder == "sourcedata":
            path = os.path.join(path, "sourcedata")
            if sub:
                path = os.path.join(path, f"sub-{sub}")

        if folder == "beta_data_v2":
            path = os.path.join(path, "beta_data_v2")
            if sub:
                path = os.path.join(path, f"sub-{sub}")

        if folder == "beta_mapping_project":
            path = os.path.join(path, "beta_mapping_project")
            if sub:
                path = os.path.join(path, f"sub-{sub}")

        if folder == "neuro_cure":
            path = os.path.join(path, "NeuroCure", "rawdata_v3")
            if sub:
                path = os.path.join(path, f"sub-{sub}")

        assert os.path.exists(path), f"wanted path ({path}) not found"

        return path


def chdir_repository(repository: str):
    """
    repository: "Py_Perceive", "Beta_profile"

    """

    #######################     USE THIS DIRECTORY FOR IMPORTING PYPERCEIVE REPO  #######################

    # create a path to the BetaSenSightLongterm folder
    # and a path to the code folder within the BetaSenSightLongterm Repo
    jennifer_user_path = os.getcwd()
    while jennifer_user_path[-14:] != "jenniferbehnke":
        jennifer_user_path = os.path.dirname(jennifer_user_path)

    repo_dict = {
        "Py_Perceive": os.path.join(
            jennifer_user_path, "code", "PyPerceive_project", "PyPerceive", "code"
        ),
        "Beta_profile": os.path.join(
            jennifer_user_path, "code", "Beta_profile_project", "Beta_profile"
        ),
    }

    # directory to PyPerceive code folder
    project_path = repo_dict[repository]
    sys.path.append(project_path)

    # # change directory to PyPerceive code path within BetaSenSightLongterm Repo
    os.chdir(project_path)

    return os.getcwd()
