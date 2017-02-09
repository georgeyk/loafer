from loafer.message_translators import StringMessageTranslator


def test_translate():
    translator = StringMessageTranslator()
    message = translator.translate(1)
    assert message == {'content': '1', 'metadata': {}}

    message = translator.translate('test')
    assert message == {'content': 'test', 'metadata': {}}

    message = translator.translate(None)
    assert message == {'content': 'None', 'metadata': {}}
