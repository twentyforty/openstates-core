from ..models import State, Chamber, simple_numbered_districts

CO = State(
    name="Colorado",
    abbr="CO",
    capital="Denver",
    capital_tz="America/Denver",
    fips="08",
    unicameral=False,
    legislature_name="Colorado General Assembly",
    lower=Chamber(
        chamber_type="lower",
        name="House",
        num_seats=65,
        title="Representative",
        districts=simple_numbered_districts(65),
    ),
    upper=Chamber(
        chamber_type="upper",
        name="Senate",
        num_seats=35,
        title="Senator",
        districts=simple_numbered_districts(35),
    ),
)
