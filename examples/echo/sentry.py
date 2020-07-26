import os
import sys

import sentry_sdk

from loafer.ext.sentry import sentry_handler

sentry_sdk.init(os.environ.get("SENTRY_SDK_URL", None))
handler = sentry_handler(sentry_sdk)

try:
    raise ValueError("test")
except:  # noqa
    handler(sys.exc_info(), "ping-message")
