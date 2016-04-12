# -*- coding: utf-8 -*-
# vi:si:et:sw=4:sts=4:ts=4

from loafer.message_translator import StringMessageTranslator


def test_translate():
    translator = StringMessageTranslator()
    message = translator.translate(1)
    assert message == '1'

    message = translator.translate('test')
    assert message == 'test'

    message = translator.translate(None)
    assert message == 'None'
