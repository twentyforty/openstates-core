import os
import io
from dotenv import load_dotenv

import google.cloud.logging
import google.cloud.secretmanager_v1 as secretmanager

def load_civiqa_env():
    if os.environ.get("GOOGLE_CLOUD_PROJECT", None):
        # Pull secrets from Secret Manager
        project_id = os.environ.get("GOOGLE_CLOUD_PROJECT")
        client = secretmanager.SecretManagerServiceClient()
        settings_name = os.environ.get("SETTINGS_NAME")
        name = f"projects/{project_id}/secrets/{settings_name}/versions/latest"
        payload = client.access_secret_version(name=name).payload.data.decode("UTF-8")
        load_dotenv(stream=io.StringIO(payload))

    # Instantiates a client
    client = google.cloud.logging.Client()

    # Retrieves a Cloud Logging handler based on the environment
    # you're running in and integrates the handler with the
    # Python logging module. By default this captures all logs
    # at INFO level and higher
    client.setup_logging()