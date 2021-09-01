import pytest

import apos


def test_version():
    assert apos.__version__ == '0.1.2'


def test_publish_event():
    messenger = apos.Messenger()

    class TestOneEvent:
        pass

    class TestTwoEvent:
        pass

    def test_event_handler(event):
        assert isinstance(event, TestOneEvent)
        messenger.publish_event(TestTwoEvent())

    messenger.subscribe_event(TestOneEvent, test_event_handler)
    messenger.publish_event(TestOneEvent())
    assert len(messenger.get_published_events()) == 2
    assert isinstance(messenger.get_published_events()[0], TestOneEvent)
    assert isinstance(messenger.get_published_events()[1], TestTwoEvent)


def test_command_and_event():
    messenger = apos.Messenger()

    class TestCommand:
        pass

    class TestEvent:
        pass

    def test_command_handler(command):
        assert isinstance(command, TestCommand)
        messenger.publish_event(TestEvent())

    messenger.subscribe_command(TestCommand, test_command_handler)
    messenger.publish_command(TestCommand())
    assert len(messenger.get_published_events()) == 1
    assert isinstance(messenger.get_published_events()[0], TestEvent)


def test_query():
    messenger = apos.Messenger()

    class TestQuery:
        pass

    class TestResponse:
        pass

    def test_query_handler(query):
        assert isinstance(query, TestQuery)
        return TestResponse()

    messenger.subscribe_query(TestQuery, test_query_handler)
    response = messenger.publish_query(TestQuery())
    assert isinstance(response, TestResponse)


def test_missing_handler():

    class TestMessage:
        pass

    with pytest.raises(apos.MissingHandler):
        messenger = apos.Messenger()
        messenger.publish_command(TestMessage())

    with pytest.raises(apos.MissingHandler):
        messenger = apos.Messenger()
        messenger.publish_query(TestMessage())


def test_overwriting_handler():
    messenger = apos.Messenger()

    class TestMessage:
        pass

    def test_handler():
        pass

    with pytest.raises(apos.OverwritingHandler):
        messenger = apos.Messenger()
        messenger.subscribe_command(TestMessage, test_handler)
        messenger.subscribe_command(TestMessage, test_handler)

    with pytest.raises(apos.OverwritingHandler):
        messenger = apos.Messenger()
        messenger.subscribe_query(TestMessage, test_handler)
        messenger.subscribe_query(TestMessage, test_handler)
