from ..models import District, simple_numbered_districts

"""
Legacy Districts is how we represent districts that have been retired due to redistricting
which occurs every 10 years
"""

legacy_districts = {
    "id": simple_numbered_districts(
        "ocd-division/country:us/state:id",
        "lower",
        35,
        num_seats=2,
    ),
    "nd": [
        District("4", "lower", "ocd-division/country:us/state:nd/sldl:4", 2),
        District("9", "lower", "ocd-division/country:us/state:nd/sldl:9", 2),
    ],
    "ma": [
        # These Districts were Retired in 2022
        District(
            "Worcester, Hampden, Hampshire and Middlesex",
            "upper",
            "ocd-division/country:us/state:ma/sldu:worcester_hampden_hampshire_and_middlesex",
        ),
        District(
            "Berkshire, Hampshire, Franklin and Hampden",
            "upper",
            "ocd-division/country:us/state:ma/sldu:berkshire_hampshire_franklin_and_hampden",
        ),
        District(
            "Worcester and Norfolk",
            "upper",
            "ocd-division/country:us/state:ma/sldu:worcester_and_norfolk",
        ),
        District(
            "Second Suffolk and Middlesex",
            "upper",
            "ocd-division/country:us/state:ma/sldu:2nd_suffolk_and_middlesex",
        ),
        District(
            "Second Plymouth and Bristol",
            "upper",
            "ocd-division/country:us/state:ma/sldu:2nd_plymouth_and_bristol",
        ),
        District(
            "Second Middlesex and Norfolk",
            "upper",
            "ocd-division/country:us/state:ma/sldu:2nd_middlesex_and_norfolk",
        ),
        District(
            "Second Hampden and Hampshire",
            "upper",
            "ocd-division/country:us/state:ma/sldu:2nd_hampden_and_hampshire",
        ),
        District(
            "Plymouth and Norfolk",
            "upper",
            "ocd-division/country:us/state:ma/sldu:plymouth_and_norfolk",
        ),
        District(
            "Norfolk, Bristol and Plymouth",
            "upper",
            "ocd-division/country:us/state:ma/sldu:norfolk_bristol_and_plymouth",
        ),
        District(
            "Norfolk, Bristol and Middlesex",
            "upper",
            "ocd-division/country:us/state:ma/sldu:norfolk_bristol_and_middlesex",
        ),
        District(
            "First Suffolk and Middlesex",
            "upper",
            "ocd-division/country:us/state:ma/sldu:1st_suffolk_and_middlesex",
        ),
        District(
            "First Plymouth and Bristol",
            "upper",
            "ocd-division/country:us/state:ma/sldu:1st_plymouth_and_bristol",
        ),
        District(
            "First Middlesex and Norfolk",
            "upper",
            "ocd-division/country:us/state:ma/sldu:1st_middlesex_and_norfolk",
        ),
        District(
            "First Hampden and Hampshire",
            "upper",
            "ocd-division/country:us/state:ma/sldu:1st_hampden_and_hampshire",
        ),
        District(
            "4th Berkshire",
            "lower",
            "ocd-division/country:us/state:ma/sldl:4th_berkshire",
        ),
    ],
    "md": [
        District("2C", "lower", "ocd-division/country:us/state:md/sldl:2c"),
        District("30", "lower", "ocd-division/country:us/state:md/sldl:30"),
        District("42", "lower", "ocd-division/country:us/state:md/sldl:42"),
        District("44", "lower", "ocd-division/country:us/state:md/sldl:44"),
        District("47", "lower", "ocd-division/country:us/state:md/sldl:47"),
        District("4A", "lower", "ocd-division/country:us/state:md/sldl:4a"),
        District("4B", "lower", "ocd-division/country:us/state:md/sldl:4b"),
        District("5A", "lower", "ocd-division/country:us/state:md/sldl:5a"),
        District("5B", "lower", "ocd-division/country:us/state:md/sldl:5b"),
        District("7", "lower", "ocd-division/country:us/state:md/sldl:7", 3),
        District("3A", "lower", "ocd-division/country:us/state:md/sldl:3a", 2),
        District("3B", "lower", "ocd-division/country:us/state:md/sldl:3b"),
        District("11", "lower", "ocd-division/country:us/state:md/sldl:11", 3),
        District("12", "lower", "ocd-division/country:us/state:md/sldl:12", 3),
        District("23A", "lower", "ocd-division/country:us/state:md/sldl:23a"),
        District("23B", "lower", "ocd-division/country:us/state:md/sldl:23b", 2),
        District("31A", "lower", "ocd-division/country:us/state:md/sldl:31a"),
        District("31B", "lower", "ocd-division/country:us/state:md/sldl:31b", 2),
        District("33", "lower", "ocd-division/country:us/state:md/sldl:33", 3),
        District("43", "lower", "ocd-division/country:us/state:md/sldl:43", 3),
    ],
    "nh": [
        District(
            "Strafford 22",
            "lower",
            "ocd-division/country:us/state:nh/sldl:strafford_22",
        ),
        District(
            "Strafford 23",
            "lower",
            "ocd-division/country:us/state:nh/sldl:strafford_23",
        ),
        District(
            "Strafford 24",
            "lower",
            "ocd-division/country:us/state:nh/sldl:strafford_24",
        ),
        District(
            "Strafford 25",
            "lower",
            "ocd-division/country:us/state:nh/sldl:strafford_25",
        ),
        District(
            "Sullivan 9", "lower", "ocd-division/country:us/state:nh/sldl:sullivan_9"
        ),
        District(
            "Sullivan 10", "lower", "ocd-division/country:us/state:nh/sldl:sullivan_10"
        ),
        District(
            "Sullivan 11", "lower", "ocd-division/country:us/state:nh/sldl:sullivan_11"
        ),
        District(
            "Belknap 9", "lower", "ocd-division/country:us/state:nh/sldl:belknap_9"
        ),
    ],
    "nv": [
        District(
            "Capital Senatorial District",
            "upper",
            "ocd-division/country:us/state:nv/sldu:capital",
        ),
        District(
            "Central Nevada Senatorial District",
            "upper",
            "ocd-division/country:us/state:nv/sldu:central_nevada",
        ),
        District(
            "Clark County, No. 1",
            "upper",
            "ocd-division/country:us/state:nv/sldu:clark_county_1",
        ),
        District(
            "Clark County, No. 2",
            "upper",
            "ocd-division/country:us/state:nv/sldu:clark_county_2",
        ),
        District(
            "Clark County, No. 3",
            "upper",
            "ocd-division/country:us/state:nv/sldu:clark_county_3",
        ),
        District(
            "Clark County, No. 4",
            "upper",
            "ocd-division/country:us/state:nv/sldu:clark_county_4",
        ),
        District(
            "Clark County, No. 5",
            "upper",
            "ocd-division/country:us/state:nv/sldu:clark_county_5",
        ),
        District(
            "Clark County, No. 6",
            "upper",
            "ocd-division/country:us/state:nv/sldu:clark_county_6",
        ),
        District(
            "Clark County, No. 7",
            "upper",
            "ocd-division/country:us/state:nv/sldu:clark_county_7",
        ),
        District(
            "Clark County, No. 8",
            "upper",
            "ocd-division/country:us/state:nv/sldu:clark_county_8",
        ),
        District(
            "Clark County, No. 9",
            "upper",
            "ocd-division/country:us/state:nv/sldu:clark_county_9",
        ),
        District(
            "Clark County, No. 10",
            "upper",
            "ocd-division/country:us/state:nv/sldu:clark_county_10",
        ),
        District(
            "Clark County, No. 11",
            "upper",
            "ocd-division/country:us/state:nv/sldu:clark_county_11",
        ),
        District(
            "Clark County, No. 12",
            "upper",
            "ocd-division/country:us/state:nv/sldu:clark_county_12",
        ),
        District(
            "Rural Nevada Senatorial District",
            "upper",
            "ocd-division/country:us/state:nv/sldu:rural_nevada",
        ),
        District(
            "Washoe County, No. 1",
            "upper",
            "ocd-division/country:us/state:nv/sldu:washoe_county_1",
        ),
        District(
            "Washoe County, No. 2",
            "upper",
            "ocd-division/country:us/state:nv/sldu:washoe_county_2",
        ),
        District(
            "Washoe County, No. 3",
            "upper",
            "ocd-division/country:us/state:nv/sldu:washoe_county_3",
        ),
        District(
            "Washoe County, No. 4",
            "upper",
            "ocd-division/country:us/state:nv/sldu:washoe_county_4",
        ),
    ],
    "pr": [
        District("I", "upper", division_id=None),
        District("II", "upper", division_id=None),
        District("III", "upper", division_id=None),
        District("IV", "upper", division_id=None),
        District("V", "upper", division_id=None),
        District("VI", "upper", division_id=None),
        District("VII", "upper", division_id=None),
        District("VIII", "upper", division_id=None),
    ],
    "vt": [
        District(
            "Addison-Rutland-1",
            "lower",
            "ocd-division/country:us/state:vt/sldl:addison-rutland-1",
        ),
        District(
            "Bennington-Rutland-1",
            "lower",
            "ocd-division/country:us/state:vt/sldl:bennington-rutland-1",
        ),
        District(
            "Chittenden-1-1",
            "lower",
            "ocd-division/country:us/state:vt/sldl:chittenden-1-1",
        ),
        District(
            "Chittenden-1-2",
            "lower",
            "ocd-division/country:us/state:vt/sldl:chittenden-1-2",
        ),
        District(
            "Chittenden-3-1",
            "lower",
            "ocd-division/country:us/state:vt/sldl:chittenden-3-1",
        ),
        District(
            "Chittenden-3-2",
            "lower",
            "ocd-division/country:us/state:vt/sldl:chittenden-3-2",
        ),
        District(
            "Chittenden-3-3",
            "lower",
            "ocd-division/country:us/state:vt/sldl:chittenden-3-3",
        ),
        District(
            "Chittenden-3-4",
            "lower",
            "ocd-division/country:us/state:vt/sldl:chittenden-3-4",
        ),
        District(
            "Chittenden-3-5",
            "lower",
            "ocd-division/country:us/state:vt/sldl:chittenden-3-5",
        ),
        District(
            "Chittenden-3-6",
            "lower",
            "ocd-division/country:us/state:vt/sldl:chittenden-3-6",
        ),
        District(
            "Chittenden-3-7",
            "lower",
            "ocd-division/country:us/state:vt/sldl:chittenden-3-7",
        ),
        District(
            "Chittenden-3-8",
            "lower",
            "ocd-division/country:us/state:vt/sldl:chittenden-3-8",
        ),
        District(
            "Chittenden-3-9",
            "lower",
            "ocd-division/country:us/state:vt/sldl:chittenden-3-9",
        ),
        District(
            "Chittenden-3-10",
            "lower",
            "ocd-division/country:us/state:vt/sldl:chittenden-3-10",
        ),
        District(
            "Chittenden-4",
            "lower",
            "ocd-division/country:us/state:vt/sldl:chittenden-4",
        ),
        District(
            "Chittenden-8",
            "lower",
            "ocd-division/country:us/state:vt/sldl:chittenden-8",
        ),
        District(
            "Chittenden-9",
            "lower",
            "ocd-division/country:us/state:vt/sldl:chittenden-9",
        ),
        District(
            "Franklin-3", "lower", "ocd-division/country:us/state:vt/sldl:franklin-3"
        ),
        District(
            "Grand Isle-Chittenden-1",
            "lower",
            "ocd-division/country:us/state:vt/sldl:grand_isle-chittenden-1",
        ),
        District(
            "Lamoille-4", "lower", "ocd-division/country:us/state:vt/sldl:lamoille-4"
        ),
        District(
            "Lamoille-Washington-1",
            "lower",
            "ocd-division/country:us/state:vt/sldl:lamoille-washington-1",
        ),
        District(
            "Orange-Addison-1",
            "lower",
            "ocd-division/country:us/state:vt/sldl:orange-addison-1",
        ),
        District(
            "Orleans-Caledonia-1",
            "lower",
            "ocd-division/country:us/state:vt/sldl:orange-caledonia-1",
        ),
        District(
            "Rutland-1-1", "lower", "ocd-division/country:us/state:vt/sldl:rutland-1-1"
        ),
        District(
            "Rutland-1-2", "lower", "ocd-division/country:us/state:vt/sldl:rutland-1-2"
        ),
        District(
            "Rutland-7", "lower", "ocd-division/country:us/state:vt/sldl:rutland-7"
        ),
        District(
            "Rutland-8", "lower", "ocd-division/country:us/state:vt/sldl:rutland-8"
        ),
        District(
            "Washington-3-1",
            "lower",
            "ocd-division/country:us/state:vt/sldl:washington-3-1",
        ),
        District(
            "Washington-3-2",
            "lower",
            "ocd-division/country:us/state:vt/sldl:washington-3-2",
        ),
        District(
            "Washington-3-3",
            "lower",
            "ocd-division/country:us/state:vt/sldl:washington-3-3",
        ),
        District(
            "Washington-Chittenden-1",
            "lower",
            "ocd-division/country:us/state:vt/sldl:washington-chittenden-1",
        ),
        District(
            "Windham-3-1", "lower", "ocd-division/country:us/state:vt/sldl:windham-3-1"
        ),
        District(
            "Windham-3-2", "lower", "ocd-division/country:us/state:vt/sldl:windham-3-2"
        ),
        District(
            "Windham-3-3", "lower", "ocd-division/country:us/state:vt/sldl:windham-3-3"
        ),
        District(
            "Windham-Bennington-1",
            "lower",
            "ocd-division/country:us/state:vt/sldl:windham-bennington-1",
        ),
        District(
            "Windham-Bennington-Windsor-1",
            "lower",
            "ocd-division/country:us/state:vt/sldl:windham-bennington-windsor-1",
        ),
        District(
            "Windsor-1-1", "lower", "ocd-division/country:us/state:vt/sldl:windsor-1-1"
        ),
        District(
            "Windsor-1-2", "lower", "ocd-division/country:us/state:vt/sldl:windsor-1-2"
        ),
        District(
            "Windsor-3", "lower", "ocd-division/country:us/state:vt/sldl:windsor-3"
        ),
        District(
            "Windsor-4", "lower", "ocd-division/country:us/state:vt/sldl:windsor-4"
        ),
        District(
            "Windsor-6-1", "lower", "ocd-division/country:us/state:vt/sldl:windsor-6-1"
        ),
        District(
            "Windsor-6-2", "lower", "ocd-division/country:us/state:vt/sldl:windsor-6-2"
        ),
        # These Districts were Retired in 2022
        District(
            "Bennington-2-1",
            "lower",
            "ocd-division/country:us/state:vt/sldl:bennington-2-1",
            2,
        ),
        District(
            "Bennington-2-2",
            "lower",
            "ocd-division/country:us/state:vt/sldl:bennington-2-2",
            2,
        ),
        District(
            "Caledonia-4",
            "lower",
            "ocd-division/country:us/state:vt/sldl:caledonia-4",
            2,
        ),
        District(
            "Chittenden-4-1",
            "lower",
            "ocd-division/country:us/state:vt/sldl:chittenden-4-1",
        ),
        District(
            "Chittenden-4-2",
            "lower",
            "ocd-division/country:us/state:vt/sldl:chittenden-4-2",
        ),
        District(
            "Chittenden-5-1",
            "lower",
            "ocd-division/country:us/state:vt/sldl:chittenden-5-1",
        ),
        District(
            "Chittenden-5-2",
            "lower",
            "ocd-division/country:us/state:vt/sldl:chittenden-5-2",
        ),
        District(
            "Chittenden-6-1",
            "lower",
            "ocd-division/country:us/state:vt/sldl:chittenden-6-1",
            2,
        ),
        District(
            "Chittenden-6-2",
            "lower",
            "ocd-division/country:us/state:vt/sldl:chittenden-6-2",
        ),
        District(
            "Chittenden-6-3",
            "lower",
            "ocd-division/country:us/state:vt/sldl:chittenden-6-3",
            2,
        ),
        District(
            "Chittenden-6-4",
            "lower",
            "ocd-division/country:us/state:vt/sldl:chittenden-6-4",
            2,
        ),
        District(
            "Chittenden-6-5",
            "lower",
            "ocd-division/country:us/state:vt/sldl:chittenden-6-5",
            2,
        ),
        District(
            "Chittenden-6-6",
            "lower",
            "ocd-division/country:us/state:vt/sldl:chittenden-6-6",
        ),
        District(
            "Chittenden-6-7",
            "lower",
            "ocd-division/country:us/state:vt/sldl:chittenden-6-7",
            2,
        ),
        District(
            "Chittenden-7-1",
            "lower",
            "ocd-division/country:us/state:vt/sldl:chittenden-7-1",
        ),
        District(
            "Chittenden-7-2",
            "lower",
            "ocd-division/country:us/state:vt/sldl:chittenden-7-2",
        ),
        District(
            "Chittenden-7-3",
            "lower",
            "ocd-division/country:us/state:vt/sldl:chittenden-7-3",
        ),
        District(
            "Chittenden-7-4",
            "lower",
            "ocd-division/country:us/state:vt/sldl:chittenden-7-4",
        ),
        District(
            "Chittenden-8-1",
            "lower",
            "ocd-division/country:us/state:vt/sldl:chittenden-8-1",
            2,
        ),
        District(
            "Chittenden-8-2",
            "lower",
            "ocd-division/country:us/state:vt/sldl:chittenden-8-2",
            2,
        ),
        District(
            "Chittenden-8-3",
            "lower",
            "ocd-division/country:us/state:vt/sldl:chittenden-8-3",
        ),
        District(
            "Chittenden-9-1",
            "lower",
            "ocd-division/country:us/state:vt/sldl:chittenden-9-1",
            2,
        ),
        District(
            "Chittenden-9-2",
            "lower",
            "ocd-division/country:us/state:vt/sldl:chittenden-9-2",
            2,
        ),
        District(
            "Essex-Caledonia-Orleans",
            "lower",
            "ocd-division/country:us/state:vt/sldl:essex-caledonia-orleans",
        ),
        District(
            "Franklin-3-1",
            "lower",
            "ocd-division/country:us/state:vt/sldl:franklin-3-1",
            2,
        ),
        District(
            "Franklin-3-2",
            "lower",
            "ocd-division/country:us/state:vt/sldl:franklin-3-2",
        ),
        District(
            "Orleans-Caledonia",
            "lower",
            "ocd-division/country:us/state:vt/sldl:orleans-caledonia",
            2,
        ),
        District(
            "Rutland-5-1", "lower", "ocd-division/country:us/state:vt/sldl:rutland-5-1"
        ),
        District(
            "Rutland-5-2", "lower", "ocd-division/country:us/state:vt/sldl:rutland-5-2"
        ),
        District(
            "Rutland-5-3", "lower", "ocd-division/country:us/state:vt/sldl:rutland-5-3"
        ),
        District(
            "Rutland-5-4", "lower", "ocd-division/country:us/state:vt/sldl:rutland-5-4"
        ),
        District(
            "Rutland-Windsor-1",
            "lower",
            "ocd-division/country:us/state:vt/sldl:rutland-windsor-1",
        ),
        District(
            "Rutland-Windsor-2",
            "lower",
            "ocd-division/country:us/state:vt/sldl:rutland-windsor-2",
        ),
        District(
            "Washington-7",
            "lower",
            "ocd-division/country:us/state:vt/sldl:washington-7",
            2,
        ),
        District(
            "Windham-2-1", "lower", "ocd-division/country:us/state:vt/sldl:windham-2-1"
        ),
        District(
            "Windham-2-2", "lower", "ocd-division/country:us/state:vt/sldl:windham-2-2"
        ),
        District(
            "Windham-2-3", "lower", "ocd-division/country:us/state:vt/sldl:windham-2-3"
        ),
        District(
            "Windham-Bennington",
            "lower",
            "ocd-division/country:us/state:vt/sldl:windham-bennington",
        ),
        District(
            "Windham-Bennington-Windsor",
            "lower",
            "ocd-division/country:us/state:vt/sldl:windham-bennington-windsor",
        ),
        District(
            "Windsor-3-1", "lower", "ocd-division/country:us/state:vt/sldl:windsor-3-1"
        ),
        District(
            "Windsor-3-2",
            "lower",
            "ocd-division/country:us/state:vt/sldl:windsor-3-2",
            2,
        ),
        District(
            "Windsor-4-1", "lower", "ocd-division/country:us/state:vt/sldl:windsor-4-1"
        ),
        District(
            "Windsor-4-2",
            "lower",
            "ocd-division/country:us/state:vt/sldl:windsor-4-2",
            2,
        ),
        District(
            "Windsor-Rutland",
            "lower",
            "ocd-division/country:us/state:vt/sldl:windsor-rutland",
        ),
        District(
            "Chittenden", "upper", "ocd-division/country:us/state:vt/sldu:chittenden", 6
        ),
        District(
            "Essex-Orleans",
            "upper",
            "ocd-division/country:us/state:vt/sldu:essex-orleans",
            2,
        ),
    ],
    "us": [
        District(
            "CA-53", "lower", division_id="ocd-division/country:us/state:ca/cd:53"
        ),
        District(
            "IL-18", "lower", division_id="ocd-division/country:us/state:il/cd:18"
        ),
        District(
            "IL-20", "lower", division_id="ocd-division/country:us/state:il/cd:20"
        ),
        District(
            "MA-10", "lower", division_id="ocd-division/country:us/state:ma/cd:10"
        ),
        District(
            "MI-14", "lower", division_id="ocd-division/country:us/state:mi/cd:14"
        ),
        District("MO-9", "lower", division_id="ocd-division/country:us/state:mo/cd:9"),
        District(
            "NJ-13", "lower", division_id="ocd-division/country:us/state:nj/cd:13"
        ),
        District(
            "NY-29", "lower", division_id="ocd-division/country:us/state:ny/cd:29"
        ),
        District(
            "NY-27", "lower", division_id="ocd-division/country:us/state:ny/cd:27"
        ),
        District(
            "OH-16", "lower", division_id="ocd-division/country:us/state:oh/cd:16"
        ),
        District(
            "OH-17", "lower", division_id="ocd-division/country:us/state:oh/cd:17"
        ),
        District(
            "OH-18", "lower", division_id="ocd-division/country:us/state:oh/cd:18"
        ),
        District("OK-6", "lower", division_id="ocd-division/country:us/state:ok/cd:6"),
        District(
            "PA-18", "lower", division_id="ocd-division/country:us/state:pa/cd:18"
        ),
        District("WV-3", "lower", division_id="ocd-division/country:us/state:wv/cd:3"),
        District(
            "MT-AL", "lower", division_id="ocd-division/country:us/state:mt/cd:at-large"
        ),
    ],
}
