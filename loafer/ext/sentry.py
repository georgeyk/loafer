# TODO: it should be async


def sentry_handler(sdk_or_hub, delete_message=False):

    def send_to_sentry(exc_info, message):
        with sdk_or_hub.push_scope() as scope:
            scope.set_extra("message", message)
            sdk_or_hub.capture_exception(exc_info)
        return delete_message

    return send_to_sentry
