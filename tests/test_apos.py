import pytest

import apos


def test_version():
    assert apos.__version__ == '0.2.1'


def test_publish_event():
    messenger = apos.Apos()

    class TestOneEvent:
        pass

    class TestTwoEvent:
        pass

    def test_event_handler(event):
        assert isinstance(event, TestOneEvent)
        messenger.publish_event(TestTwoEvent())

    messenger.subscribe_event(TestOneEvent, [test_event_handler])
    messenger.publish_event(TestOneEvent())
    assert len(messenger.get_published_events()) == 2
    assert isinstance(messenger.get_published_events()[0], TestOneEvent)
    assert isinstance(messenger.get_published_events()[1], TestTwoEvent)


def test_command_and_event():
    messenger = apos.Apos()

    class TestCommand:
        pass

    class TestEvent:
        pass

    def command_handler(command):
        assert isinstance(command, TestCommand)
        messenger.publish_event(TestEvent())

    messenger.subscribe_command(TestCommand, command_handler)
    messenger.publish_command(TestCommand())
    assert len(messenger.get_published_events()) == 1
    assert isinstance(messenger.get_published_events()[0], TestEvent)


def test_query():
    messenger = apos.Apos()

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
        messenger = apos.Apos()
        messenger.publish_command(TestMessage())

    with pytest.raises(apos.MissingHandler):
        messenger = apos.Apos()
        messenger.publish_query(TestMessage())


def test_overwriting_handler():
    messenger = apos.Apos()

    class TestMessage:
        pass

    def test_handler():
        pass

    with pytest.raises(apos.OverwritingHandler):
        messenger = apos.Apos()
        messenger.subscribe_command(TestMessage, test_handler)
        messenger.subscribe_command(TestMessage, test_handler)

    with pytest.raises(apos.OverwritingHandler):
        messenger = apos.Apos()
        messenger.subscribe_query(TestMessage, test_handler)
        messenger.subscribe_query(TestMessage, test_handler)


def test_sessions():
    messenger = apos.Apos()

    class TestCommand:
        pass

    class TestEvent:
        pass

    def command_handler(command):
        messenger.publish_event(TestEvent())

    messenger.subscribe_command(TestCommand, command_handler)

    with messenger.session() as messenger_session_1:
        messenger_session_1.publish_command(TestCommand())
        assert len(messenger_session_1.get_published_events()) == 1
        assert isinstance(
            messenger_session_1.get_published_events()[0], TestEvent)

    with messenger.session() as messenger_session_2:
        messenger_session_2.publish_command(TestCommand())
        assert len(messenger_session_2.get_published_events()) == 1
        assert isinstance(
            messenger_session_2.get_published_events()[0], TestEvent)

    assert len(messenger.get_published_events()) == 0
