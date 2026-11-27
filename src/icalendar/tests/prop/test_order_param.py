from icalendar import Event, vText


def test_order_default_is_none():
    """ORDER is absent by default, meaning 'comes last'."""
    contact = vText("Dev")
    assert contact.ORDER is None


def test_order_round_trips_as_int():
    """Setting ORDER stores an int and reads back the same int."""
    contact = vText("Dev")
    contact.ORDER = 1
    assert contact.ORDER == 1
    assert contact.params["ORDER"] == "1"


def test_order_parses_from_ical():
    """A CONTACT with ORDER set in a real .ics round-trips through from_ical."""
    ics = "BEGIN:VEVENT\r\nCONTACT;ORDER=2:Dev\r\nEND:VEVENT\r\n"
    event = Event.from_ical(ics)
    [contact] = event.contacts
    assert contact.ORDER == 2
