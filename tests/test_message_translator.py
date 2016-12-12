from loafer.message_translators import StringMessageTranslator


def test_translate():
    translator = StringMessageTranslator()
    message = translator.translate(1)
    assert message == {'content': '1'}

    message = translator.translate('test')
    assert message == {'content': 'test'}

    message = translator.translate(None)
    assert message == {'content': 'None'}
