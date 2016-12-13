
class ProviderError(Exception):
    pass


class ConfigurationError(Exception):
    pass


class LoaferException(Exception):
    pass


class IgnoreMessage(LoaferException):
    pass


class RejectMessage(LoaferException):
    pass


# Alias

DeleteMessage = RejectMessage
