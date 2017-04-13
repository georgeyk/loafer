# TODO: it should be async
# https://github.com/getsentry/raven-aiohttp


def sentry_handler(client, delete_message=False):

    def send_to_sentry(exc_info, message):
        client.captureException(
            exc_info,
            extra={'message': message},
        )
        return delete_message

    return send_to_sentry
