"""
functions in this module should take a single object and update it in place

optionally, they can take a save parameter, that should default to False
but can be set to True to force a save if changes were made
(this allows for usage from CLI)
"""
from ._types import Model


def update_bill_fields(bill: Model, *, save: bool = False) -> None:
    first_action_date = None
    latest_action_date = None
    latest_action_description = ""
    latest_passage_date = None

    # iterate over according to order
    # first action date will use first by order (<)
    # latest will use latest by order (>=)
    actions = bill.actions.order_by("date", "order")
    if actions:
        first_action = actions.first()
        latest_action = actions.last()
        passage_action = actions.filter(classification__in="passage").last()
        first_action_date = first_action.date
        latest_action_date = latest_action.date
        latest_action_description = latest_action.description

        if passage_action:
            latest_passage_date = passage_action.date

    if (
        bill.first_action_date != first_action_date
        or bill.latest_action_date != latest_action_date
        or bill.latest_passage_date != latest_passage_date
        or bill.latest_action_description != latest_action_description
    ):
        bill.first_action_date = first_action_date
        bill.latest_passage_date = latest_passage_date
        bill.latest_action_date = latest_action_date
        bill.latest_action_description = latest_action_description
        bill.save()
