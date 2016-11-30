import pytest

from examples.message_translator import IntMessageTranslator


@pytest.fixture
def translator():
    return IntMessageTranslator()


def test_translate(translator):
    for i in ['0', '-1', '1', '1000']:
        translated = translator.translate(i)
        assert 'content' in translated
        assert translated['content'] == int(i)


def test_translate_error(translator):
    for i in ['a', '[]', '{}', '()']:
        translated = translator.translate(i)
        assert 'content' in translated
        assert translated['content'] is None
