from django.db.models import Q
from ._types import _JsonDict
from .base import BaseImporter
from ..data.models import Organization


class OrganizationImporter(BaseImporter):
    _type = "organization"
    model_class = Organization

    def limit_spec(self, spec: _JsonDict) -> _JsonDict:
        if spec.get("classification") != "party":
            spec["jurisdiction_id"] = self.jurisdiction_id

        result = Q(**spec)
        name = spec.pop("name", None)
        if name:
            result &= (
                Q(name__iexact=name)
                | (
                    Q(
                        sponsorships_scraped_names__value__iexact=name,
                        sponsorships_scraped_names__approved=True,
                    )
                )
                | Q(other_names__name__iexact=name)
            )

        return result
