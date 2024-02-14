import os
import django  # type: ignore
from django import conf  # type: ignore
import dj_database_url  # type: ignore


SETTINGS_PATH = os.path.dirname(os.path.dirname(__file__))


def init_django() -> None:  # pragma: no cover
    DATABASE_URL = os.environ.get(
        "DATABASE_URL", "postgis://openstates:openstates@localhost/openstates"
    )
    DATABASES = {"default": dj_database_url.parse(DATABASE_URL)}
    application_name = "os_core"
    if "OPTIONS" not in DATABASES:
        DATABASES["default"]["OPTIONS"] = {"application_name": application_name}
    else:
        DATABASES["default"]["OPTIONS"]["application_name"] = application_name

    conf.settings.configure(
        conf.global_settings,
        SECRET_KEY="not-important",
        DEBUG=False,
        INSTALLED_APPS=(
            "django.contrib.contenttypes",
            "openstates.data",
        ),
        DATABASES=DATABASES,
        TIME_ZONE="UTC",
        MIDDLEWARE_CLASSES=(),
    )
    django.setup()
