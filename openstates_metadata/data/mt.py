from ..models import State, Chamber, simple_numbered_districts

MT = State(
    name="Montana",
    abbr="MT",
    capital="Helena",
    capital_tz="America/Denver",
    fips="30",
    unicameral=False,
    legislature_name="Montana Legislature",
    lower=Chamber(
        chamber_type="lower",
        name="House",
        num_seats=100,
        title="Representative",
        districts=simple_numbered_districts(100),
    ),
    upper=Chamber(
        chamber_type="upper",
        name="Senate",
        num_seats=50,
        title="Senator",
        districts=simple_numbered_districts(50),
    ),
)
