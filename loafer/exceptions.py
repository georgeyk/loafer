# -*- coding: utf-8 -*-
# vi:si:et:sw=4:sts=4:ts=4


class ConsumerError(Exception):
    pass


class ConfigurationError(Exception):
    pass


class IgnoreMessage(Exception):
    pass


class RejectMessage(Exception):
    pass
