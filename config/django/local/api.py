from config.env import env
from config.django.base import *


# File Uploads

STORAGES = {
    "default": {
        "BACKEND": "django.core.files.storage.FileSystemStorage",
        "OPTIONS": {
            "location": MEDIA_ROOT,
            "base_url": MEDIA_URL,
            "allow_overwrite": True,
        },
    },
}
