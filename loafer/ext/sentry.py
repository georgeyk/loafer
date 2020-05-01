# TODO: it should be async
# https://github.com/getsentry/raven-aiohttp


def sentry_handler(capture_exception, delete_message=False):

    def send_to_sentry(exc_info, message):
        scope_kwargs = {"message": message}
        capture_exception(exc_info, **scope_kwargs)

        return delete_message

    return send_to_sentry
