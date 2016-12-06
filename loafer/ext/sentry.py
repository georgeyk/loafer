# TODO: it should be async
# https://github.com/getsentry/raven-aiohttp


def sentry_handler(client):

    def send_to_sentry(exc_type, exc, message):
        client.captureException(
            extra={'message': message},
        )
        # The message that originated the error will be acknowledged
        return True

    return send_to_sentry
