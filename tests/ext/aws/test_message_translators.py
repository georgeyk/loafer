import json

import pytest

from loafer.ext.aws.message_translators import SNSMessageTranslator, SQSMessageTranslator

# sqs


@pytest.fixture
def sqs_translator():
    return SQSMessageTranslator()


def test_translate_sqs(sqs_translator):
    original = {'Body': json.dumps('some-content')}
    content = sqs_translator.translate(original)
    assert 'content' in content
    assert content['content'] == 'some-content'

    original = {'Body': json.dumps({'key': 'value'})}
    content = sqs_translator.translate(original)
    assert content['content'] == {'key': 'value'}


def test_sqs_metadata_extract(sqs_translator):
    original = {'Body': json.dumps('some-content'), 'whatever': 'whatever'}
    content = sqs_translator.translate(original)
    metadata = content['metadata']
    assert metadata
    assert 'whatever' in metadata
    assert metadata['whatever'] == 'whatever'


@pytest.fixture(params=[{'invalid': 'format'}, 'invalid format',
                        42, {}, [], (), ''])
def parametrize_invalid_messages(request):
    return request.param


def test_translate_sqs_handles_invalid_format(sqs_translator, parametrize_invalid_messages):
    content = sqs_translator.translate(parametrize_invalid_messages)
    assert content['content'] is None


def test_translate_sqs_handles_json_error(sqs_translator):
    original = {'Body': 'invalid: json'}
    content = sqs_translator.translate(original)
    assert content['content'] is None

# sns


@pytest.fixture
def sns_translator():
    return SNSMessageTranslator()


def test_translate_sns(sns_translator):
    message_content = 'here I am'
    message = json.dumps({'Message': json.dumps(message_content)})
    original = {'Body': message}
    content = sns_translator.translate(original)
    assert content['content'] == message_content

    message_content = {'here': 'I am'}
    message = json.dumps({'Message': json.dumps(message_content)})
    original = {'Body': message}
    content = sns_translator.translate(original)
    assert content['content'] == message_content


def test_sns_metadata_extract(sns_translator):
    message_content = 'here I am'
    message = json.dumps({'Message': json.dumps(message_content), 'foo': 'nested'})
    original = {'Body': message, 'bar': 'not nested'}
    content = sns_translator.translate(original)
    metadata = content['metadata']
    assert metadata
    assert 'foo' in metadata
    assert metadata['foo'] == 'nested'
    assert 'bar' in metadata
    assert metadata['bar'] == 'not nested'


def test_translate_sns_handles_invalid_content(sns_translator, parametrize_invalid_messages):
    message = json.dumps({'Message': parametrize_invalid_messages})
    original = {'Body': message}
    content = sns_translator.translate(original)
    assert content['content'] is None


def test_translate_sns_handles_invalid_format(sns_translator, parametrize_invalid_messages):
    content = sns_translator.translate(parametrize_invalid_messages)
    assert content['content'] is None
