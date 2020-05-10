import asyncio
import os

from loafer.ext.aws.routes import SQSRoute
from loafer.managers import LoaferManager


async def echo_message_handler(message, *args):
    print(f"message is {message}")
    print(f"args is {args}")

    await asyncio.sleep(0.5)
    return True


async def error_handler(exc_type, message):
    print(f"exception {exc_type} received")
    return False


endpoint_url = os.environ.get("AWS_ENDPOINT_URL", "http://localhost:4100")

routes = (
    SQSRoute(
        "echo__loafer__notification",
        {"endpoint_url": endpoint_url},
        handler=echo_message_handler,
        error_handler=error_handler,
    ),
)

manager = LoaferManager(routes=routes)
manager.run(debug=True)
