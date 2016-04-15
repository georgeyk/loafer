# -*- coding: utf-8 -*-
# vi:si:et:sw=4:sts=4:ts=4

import json

import pytest

from loafer.aws.message_translator import SQSMessageTranslator


@pytest.fixture
def translator():
    return SQSMessageTranslator()


def test_translate(translator):
    original = {'Body': json.dumps('some-content')}
    content = translator.translate(original)
    assert 'content' in content
    assert content['content'] == 'some-content'

    original = {'Body': json.dumps({'key': 'value'})}
    content = translator.translate(original)
    assert content['content'] == {'key': 'value'}


@pytest.fixture(params=[{'invalid': 'format'}, 'invalid format',
                        42, {}, [], (), '', object()])
def parametrize_invalid_messages(request):
    return request.param


def test_translate_handles_invalid_format(translator, parametrize_invalid_messages):
    content = translator.translate(parametrize_invalid_messages)
    assert content['content'] is None


def test_translate_handles_json_error(translator):
    original = {'Body': 'invalid: json'}
    content = translator.translate(original)
    assert content['content'] is None
