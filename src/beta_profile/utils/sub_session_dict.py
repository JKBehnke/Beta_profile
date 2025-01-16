""" Dictionary of all included subjects and their sessions """

sub_sessions_dict = {
    "017": ["Fu11m"],
    "019": ["Fu12m"],
    "021": ["Fu12m"],
    "023": ["Fu13m"],
    "024": ["Fu12m"],
    "025": ["Fu12m"],
    "026": ["Fu12m"],
    "028": ["Fu12m"],
    "029": ["Fu16m"],
    "030": ["Fu12m"],
    "031": ["Fu03m"],
    "032": ["Fu03m"],
    "033": ["Fu12m"],
    "036": ["Fu12m"],
    "038": ["Fu03m"],
    "039": ["Fu13m"],
    "040": ["Fu12m"],
    "041": ["Fu12m"],  # fehlt
    "042": ["Fu13m"],
    "043": ["Fu13m"],
    "044": ["Fu13m"],
    "045": ["Fu12m"],
    "047": ["Fu12m"],
    "048": ["Fu12m"],  # nur 0M
    "049": ["Fu12m"],  # nur 0M
    "050": ["Fu10m"],
    "051": ["Fu12m"],  # nur 0M
    "052": ["Fu12m"],  # nur 0M
    "055": ["Fu12m"],  # nur 0M
    "056": ["Fu12m"],  # fehlt
    "059": ["Fu06m"],
    "060": ["Fu03m"],  # 12M fehlt
    "061": ["Fu12m"],  # nur 0M
    "062": ["Fu03m"],  # 12M fehlt
    "063": ["Fu12m"],  # fehlt
    "064": ["Fu12m"],
    "065": ["Fu12m"],
    "066": ["Fu12m"],
    "067": ["Fu12m"],
    "068": ["Fu12m"],
    "069": ["Fu12m"],
    "070": ["Fu12m"],
    "071": ["Fu12m"],
    "072": ["Fu12m"],
    "073": ["Fu12m"],
    "075": ["Fu12m"],
    "076": ["Fu12m"],
    "077": ["Fu12m"],
    "078": ["Fu12m"],
    "079": ["Fu12m"],
    "080": ["Fu12m"],
    "081": ["Fu12m"],
    "083": ["Fu12m"],
    "084": ["Fu12m"],
    "085": ["Fu12m"],
    "086": ["Fu12m"],
    "087": ["Fu12m"],
    "088": ["Fu12m"],
    "089": ["Fu12m"],
    "090": ["Fu12m"],
    "091": ["Fu12m"],
    "093": ["Fu12m"],
    "094": ["Fu12m"],
    "095": ["Fu12m"],
    "096": ["Fu12m"],
    "097": ["Fu12m"],
    "098": ["Fu12m"],
    "099": ["Fu12m"],
    "101": ["Fu12m"],
    "102": ["Fu12m"],
    "105": ["Fu12m"],
    "106": ["Fu12m"],
    "108": ["Fu12m"],
    "110": ["Fu12m"],
    "112": ["Fu12m"],
}


def get_sub_sessions(sub: str):
    """
    Get the available session from a subject
    """

    return sub_sessions_dict[sub]


def get_all_included_subjects():
    """
    Get all included subjects
    """

    return list(sub_sessions_dict.keys())
