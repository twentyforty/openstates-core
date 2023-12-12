import os
import logging
from google.cloud.logging.handlers import CloudLoggingHandler
from google.cloud.logging import Client

# Google Cloud logging severity and Python levels mapping
py_label_to_level = {"NOTICE": 25, "ALERT": 70, "EMERGENCY": 80}
py_level_to_label = {v: k for k, v in py_label_to_level.items()}
py_level_to_severity = {25: 300, 70: 700, 80: 800}

#
def google_cloud_client(credentials=None):
    """
    Instantiates Google Cloud Logging client.
    credentials - value of the environment variable GOOGLE_APPLICATION_CREDENTIALS
    """
    if credentials:
        os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = credentials
    try:
        return Client()
        # return Client.from_service_account_json(google_service_key_path)
    except Exception as e:
        print(f"Error instantiating a Google Cloud client: {e}")
        return None


#
class JsonFieldsFileHandler(logging.FileHandler):
    """
    Takes care of json_fields by merging data with the log message
    """

    def emit(self, record):
        json_fields = getattr(record, "json_fields", {})
        msg = getattr(record, "msg", "")

        if json_fields:
            record.json_fields = None
            record.msg = str(msg) + " " + str(json_fields)

        super().emit(record)

        # restore the record for other handlers
        if json_fields:
            record.json_fields = json_fields
            record.msg = msg


#
class CloudLoggingHandlerX(CloudLoggingHandler):
    """
    Adjusts logging level before passing it to GCP
    """

    def emit(self, record):
        level = record.levelno
        if record.levelno in py_level_to_severity:
            record.levelno = py_level_to_severity[record.levelno]

        super().emit(record)
        record.levelno = level


#
def logging_config(logging_settings):
    # Add custom log levels
    for level, levelName in py_level_to_label.items():
        logging.addLevelName(level, levelName)

    # Register a custom logger
    logging.setLoggerClass(LoggerWithExtra)

    # call Python library config function
    # LOGGING_CONFIG = "logging.config.dictConfig"
    logging.config.dictConfig(logging_settings)


#
class LoggerWithExtra(logging.Logger):
    """
    Allows logging with extra fields treated as JSON payload.
    Adds notice method to log entries with severity between INFO and WARNING.
    Adds functions to log with alert and emergency severities.
    Example:
        logger.info('A message with data', x=1, y=2)
    """

    def critical(self, msg, *args, **kwargs):
        super().critical(msg, *args, extra={"json_fields": kwargs}, stacklevel=2)

    def debug(self, msg, *args, **kwargs):
        super().debug(msg, *args, extra={"json_fields": kwargs}, stacklevel=2)

    def error(self, msg, *args, **kwargs):
        super().error(msg, *args, extra={"json_fields": kwargs}, stacklevel=2)

    def exception(self, msg, *args, **kwargs):
        super().exception(msg, *args, extra={"json_fields": kwargs}, stacklevel=2)

    def fatal(self, msg, *args, **kwargs):
        super().fatal(msg, *args, extra={"json_fields": kwargs}, stacklevel=2)

    def info(self, msg, *args, **kwargs):
        super().info(msg, *args, extra={"json_fields": kwargs}, stacklevel=2)

    def notice(self, msg, *args, **kwargs):
        super().log(
            py_label_to_level["NOTICE"],
            msg,
            *args,
            extra={"json_fields": kwargs},
            stacklevel=2,
        )

    def warning(self, msg, *args, **kwargs):
        super().warning(msg, *args, extra={"json_fields": kwargs}, stacklevel=2)

    def log(self, level, msg, *args, **kwargs):
        super().log(level, msg, *args, extra={"json_fields": kwargs}, stacklevel=2)

    def alert(self, msg, *args, **kwargs):
        super().log(
            py_label_to_level["ALERT"],
            msg,
            *args,
            extra={"json_fields": kwargs},
            stacklevel=2,
        )

    def emergency(self, msg, *args, **kwargs):
        super().log(
            py_label_to_level["EMERGENCY"],
            msg,
            *args,
            extra={"json_fields": kwargs},
            stacklevel=2,
        )
