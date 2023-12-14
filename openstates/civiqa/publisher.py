import json
import os

from google.api_core.exceptions import NotFound
from google.cloud.pubsub import PublisherClient

from openstates.data.models.jurisdiction import LegislativeSession

project_id = os.environ["GOOGLE_CLOUD_PROJECT"]
publisher_client = PublisherClient()


OS_UPDATE_FINISHED = "os-update-finished"
OS_UPDATE_REQUESTED = "os-update-requested"


def publish_os_update_request(legislative_session: LegislativeSession, scrapers=["bills"]):
    jurisdiction_id = legislative_session.jurisdiction_id
    session_identifier = legislative_session.identifier
    active_only = False
    jurisdiction_id, scrapers, session_identifier, active_only
    _publish(OS_UPDATE_REQUESTED, {
        "jurisdiction_id": jurisdiction_id,
        "scrapers": scrapers,
        "session_identifier": session_identifier,
        "active_only": active_only,
    })


def publish_os_update_finished(run_plan):
    _publish(OS_UPDATE_FINISHED, {"run_plan_id": run_plan.id})


def _publish(topic, args: dict):
    topic_id = _to_topic_id(topic)
    topic_path = publisher_client.topic_path(project_id, topic_id)

    try:
        data = json.dumps(args).encode("utf-8")
        future = publisher_client.publish(topic_path, data)
        print(f"Published message ID: {future.result()}")

    except NotFound:
        print(f"{topic_id} not found.")


def _to_topic_id(topic: str, environment=None):
    return "%s-%s" % (topic, environment or os.environ["ENVIRONMENT"])
