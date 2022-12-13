siecle_millenaire = r"^s((\.|i[eè]cles?)?|mill[eé]naires?)$"

patterns_fr_CENTURY = [
    {
        "label": "CENTURY",
        "pattern": [
            {"OP": "*", "ENT_TYPE": "DATEPREFIX"},
            {"ENT_TYPE": "ORDINAL"},
            {"LOWER": {"REGEX": siecle_millenaire}},
            {"OP": "*", "ENT_TYPE": "DATESUFFIX"}
        ]
    },
    {
        "label": "CENTURY",
        "pattern": [
            {"OP": "*", "ENT_TYPE": "DATEPREFIX"},
            {"ENT_TYPE": "ORDINAL"},
            {"OP": "?", "LOWER": {"REGEX": siecle_millenaire}},
            {"OP": "*", "ENT_TYPE": "DATESUFFIX"},
            {"ENT_TYPE": "DATESEPARATOR"},
            {"OP": "*", "ENT_TYPE": "DATEPREFIX"},
            {"ENT_TYPE": "ORDINAL"},
            {"LOWER": {"REGEX": siecle_millenaire}},
            {"OP": "*", "ENT_TYPE": "DATESUFFIX"}
        ]
    },
    {
        "label": "CENTURY",
        "pattern": [
            {"OP": "*", "ENT_TYPE": "DATEPREFIX"},
            {"ENT_TYPE": "ORDINAL"},
            {"LOWER": {"REGEX": siecle_millenaire}},
            {"OP": "*", "ENT_TYPE": "DATESUFFIX"},
            {"ENT_TYPE": "DATESEPARATOR"},
            {"OP": "*", "ENT_TYPE": "DATEPREFIX"},
            {"ENT_TYPE": "ORDINAL"},
            {"OP": "?", "LOWER": {"REGEX": siecle_millenaire}},
            {"OP": "*", "ENT_TYPE": "DATESUFFIX"}
        ]
    }
]
