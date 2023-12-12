import json
import os

from data.models import RunPlan
from google.api_core.exceptions import NotFound
from google.cloud.pubsub import PublisherClient

project_id = os.environ.get("GOOGLE_CLOUD_PROJECT")
publisher_client = PublisherClient()


OS_UPDATE_FINISHED = "os-update-finished"
    
def publish_os_update_finished(run_plan: RunPlan):
    _publish(OS_UPDATE_FINISHED, {"run_plan_id": run_plan.id})


def _publish(topic_id, args: dict):
    topic_path = publisher_client.topic_path(project_id, topic_id)

    try:
        data = json.dumps(args).encode("utf-8")
        future = publisher_client.publish(topic_path, data)
        print(f"Published message ID: {future.result()}")

    except NotFound:
        print(f"{topic_id} not found.")
