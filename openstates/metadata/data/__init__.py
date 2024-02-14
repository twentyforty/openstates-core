from openstates.metadata.models import State
from . import states
from .pr import PR
from .dc import DC
from .us import US

STATES = states.STATES
TERRITORIES = states.TERRITORIES
STATES_AND_TERRITORIES = STATES + TERRITORIES + states.DISTRICTS
STATES_AND_DC_PR = STATES + [DC, PR]
INTERNATIONAL = states.INTERNATIONAL + [US]

STATES_BY_ABBR = {s.abbr: s for s in STATES_AND_TERRITORIES + INTERNATIONAL}
STATES_BY_JID: dict[str, State] = {
    s.jurisdiction_id: s for s in STATES_AND_TERRITORIES + INTERNATIONAL
}
STATES_BY_NAME = {s.name.lower(): s for s in STATES_AND_TERRITORIES + INTERNATIONAL}

NON_US_INTERNATIONAL_ABBRS = [k.abbr for k in INTERNATIONAL if k.abbr != "US"]
INTERNATIONAL_ABBRS = [k.abbr for k in INTERNATIONAL]
