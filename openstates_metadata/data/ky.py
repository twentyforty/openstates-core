from ..models import State, Chamber, simple_numbered_districts

KY = State(
    name="Kentucky",
    abbr="KY",
    capital="Frankfort",
    capital_tz="America/New_York",
    fips="21",
    unicameral=False,
    legislature_name="Kentucky General Assembly",
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
        num_seats=38,
        title="Senator",
        districts=simple_numbered_districts(38),
    ),
)
