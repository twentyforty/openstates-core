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
            result &= Q(name__iexact=name) | Q(scraped_names__value=name)

        return result
