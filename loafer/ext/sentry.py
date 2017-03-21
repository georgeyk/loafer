# TODO: it should be async
# https://github.com/getsentry/raven-aiohttp


def sentry_handler(client, delete_message=False):

    def send_to_sentry(exc_type, exc, message):
        client.captureException(
            extra={'message': message},
        )
        return delete_message

    return send_to_sentry
