from dataclasses import dataclass

import apos


@dataclass
class TestOneEvent:
    pass


@dataclass
class TestTwoEvent:
    pass


def main():

    def test_event_handler(event):
        assert isinstance(event, TestOneEvent)
        apos.messenger.publish_event(TestTwoEvent())

    apos.messenger.subscribe_event(TestOneEvent, [test_event_handler])
    apos.messenger.publish_event(TestOneEvent())
    print(apos.messenger.get_published_events())


if __name__ == "__main__":
    main()
