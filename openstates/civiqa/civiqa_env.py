import os
import io
from dotenv import load_dotenv

import google.cloud.logging
import google.cloud.secretmanager_v1 as secretmanager

def load():
    
    project_id = os.environ["GOOGLE_CLOUD_PROJECT"]
    if "GOOGLE_APPLICATION_CREDENTIALS" not in os.environ:
        # Pull secrets from Secret Manager
        client = secretmanager.SecretManagerServiceClient()
        settings_name = os.environ.get("SETTINGS_NAME")
        name = f"projects/{project_id}/secrets/{settings_name}/versions/latest"
        payload = client.access_secret_version(name=name).payload.data.decode("UTF-8")
        load_dotenv(stream=io.StringIO(payload))

    client = google.cloud.logging.Client()
    client.setup_logging()