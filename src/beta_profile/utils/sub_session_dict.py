""" Dictionary of all included subjects and their sessions """

sub_sessions_dict = {
    "017": ["Fu11m"],
    "019": ["Fu12m"],  # 020 hat 3389??
    "021": ["Fu12m"],
    "023": ["Fu13m"],
    "024": ["Fu11m"],
    "025": ["Fu12m"],
    "026": ["Fu12m"],
    "028": ["Fu12m"],
    "029": ["Fu16m"],
    "030": ["Fu12m"],
    "031": ["Fu03m"],  # Düsseldorf
    "032": ["Fu03m"],  # Düsseldorf
    "033": ["Fu12m"],
    "036": ["Fu12m"],
    "038": ["Fu03m"],
    "039": ["Fu13m"],
    "040": ["Fu12m"],
    "041": ["Fu17m"],
    "042": ["Fu13m"],
    "043": ["Fu13m"],
    "044": ["Fu13m"],
    "045": ["Fu12m"],
    "047": ["Fu12m"],
    "048": ["Fu12m"],
    "049": ["Fu12m"],
    "050": ["Fu10m"],
    "051": ["Fu12m"],
    "052": ["Fu13m"],
    "055": ["Fu18m"],
    "056": ["Fu13m"],
    "059": ["Fu23m"],
    "060": ["Fu13m"],
    "061": ["Fu12m"],
    "062": ["Fu12m"],
    # "063": ["Fu12m"],  # 063 fehlt
    "064": ["Fu03m"],
    "065": ["Fu03m"],
    "066": ["Fu12m"],
    "067": ["Fu13m"],
    "068": ["Fu12m"],
    "069": ["Fu12m"],
    "070": ["Fu12m"],
    "071": ["Fu03m"],
    "072": ["Fu12m"],
    # "073": ["Fu12m"], # 073 fehlt
    "075": ["Fu14m"],
    "076": ["Fu03m"],
    "077": ["Fu12m"],
    "078": ["Fu03m"],
    "079": ["Fu03m"],
    "080": ["Fu12m"],
    "081": ["Fu12m"],
    "083": ["Fu12m"],
    "084": ["Fu11m"],
    "085": ["Fu12m"],
    # "086": ["Fu12m"], # nur 0M
    "087": ["Fu12m"],
    "088": ["Fu03m"],
    "089": ["Fu11m"],
    "090": ["Fu03m"],
    "091": ["Fu03m"],
    "093": ["Fu03m"],
    "094": ["Fu03m"],
    "095": ["Fu03m"],
    "096": ["Fu15m"],
    # "097": ["Fu12m"], # 097 fehlt
    # "098": ["Fu12m"], # 098 fehlt
    "099": ["Fu03m"],
    "101": ["Fu03m"],
    # "102": ["Fu02m"], #fehlt
    "105": ["Fu02m"],
    "106": ["Fu03m"],
    "108": ["Fu03m"],
    # "110": ["Fu12m"], #fehlt
    # "112": ["Fu12m"], #fehlt
    "114": ["Fu03m"],
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
