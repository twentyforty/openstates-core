from ..models import State, Chamber, District, simple_numbered_districts

NJ = State(
    name="New Jersey",
    abbr="NJ",
    capital="Trenton",
    capital_tz="America/New_York",
    fips="34",
    unicameral=False,
    legislature_name="New jersey Legislature",
    lower=Chamber(
        chamber_type="lower",
        name="Assembly",
        num_seats=80,
        title="Assembly Member",
        districts=[
            District("1", 2),
            District("2", 2),
            District("3", 2),
            District("4", 2),
            District("5", 2),
            District("6", 2),
            District("7", 2),
            District("8", 2),
            District("9", 2),
            District("10", 2),
            District("11", 2),
            District("12", 2),
            District("13", 2),
            District("14", 2),
            District("15", 2),
            District("16", 2),
            District("17", 2),
            District("18", 2),
            District("19", 2),
            District("20", 2),
            District("21", 2),
            District("22", 2),
            District("23", 2),
            District("24", 2),
            District("25", 2),
            District("26", 2),
            District("27", 2),
            District("28", 2),
            District("29", 2),
            District("30", 2),
            District("31", 2),
            District("32", 2),
            District("33", 2),
            District("34", 2),
            District("35", 2),
            District("36", 2),
            District("37", 2),
            District("38", 2),
            District("39", 2),
            District("40", 2),
        ],
    ),
    upper=Chamber(
        chamber_type="upper",
        name="Senate",
        num_seats=40,
        title="Senator",
        districts=simple_numbered_districts(40),
    ),
)
