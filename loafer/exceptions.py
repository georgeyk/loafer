
class ProviderError(Exception):
    pass


class ConfigurationError(Exception):
    pass


class LoaferException(Exception):
    pass


class KeepMessage(LoaferException):
    pass


class DeleteMessage(LoaferException):
    pass
