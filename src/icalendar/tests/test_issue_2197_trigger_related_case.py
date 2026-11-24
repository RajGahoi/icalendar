from datetime import datetime, timedelta, timezone

from icalendar import Alarm, Calendar


def test_trigger_related_case_insensitivity():
    """Test that TRIGGER;RELATED parameter is case-insensitive (#2197)."""
    ics_template = """BEGIN:VCALENDAR
VERSION:2.0
PRODID:-//example//EN
BEGIN:VEVENT
UID:related-case@example.com
DTSTAMP:20250101T000000Z
DTSTART:20250115T100000Z
DTEND:20250115T120000Z
BEGIN:VALARM
ACTION:DISPLAY
DESCRIPTION:Reminder
TRIGGER;RELATED={related}:-PT15M
END:VALARM
END:VEVENT
END:VCALENDAR
"""
    expected_start = datetime(2025, 1, 15, 9, 45, 0, tzinfo=timezone.utc)
    expected_end = datetime(2025, 1, 15, 11, 45, 0, tzinfo=timezone.utc)

    for related in ["START", "start", "Start"]:
        cal = Calendar.from_ical(ics_template.format(related=related))
        event = cal.events[0]
        alarm_comp = event.subcomponents[0]
        assert alarm_comp.TRIGGER_RELATED == "START"
        alarm = event.alarms.times[0]
        assert alarm.trigger == expected_start

    for related in ["END", "end", "End"]:
        cal = Calendar.from_ical(ics_template.format(related=related))
        event = cal.events[0]
        alarm_comp = event.subcomponents[0]
        assert alarm_comp.TRIGGER_RELATED == "END"
        alarm = event.alarms.times[0]
        assert alarm.trigger == expected_end


def test_trigger_related_getter_and_setter_normalization():
    """Test normalization in getter and setter of TRIGGER_RELATED."""
    alarm = Alarm()
    alarm.TRIGGER = timedelta(minutes=-15)

    assert alarm.TRIGGER_RELATED == "START"

    alarm.TRIGGER_RELATED = "end"
    assert alarm.TRIGGER_RELATED == "END"
    assert alarm["TRIGGER"].params["RELATED"] == "END"

    alarm.TRIGGER_RELATED = "start"
    assert alarm.TRIGGER_RELATED == "START"
    assert alarm["TRIGGER"].params["RELATED"] == "START"


def test_trigger_related_unknown_value_fallback():
    """Test that unknown/invalid RELATED parameter values fall back to START per RFC 5545."""
    alarm = Alarm()
    alarm.TRIGGER = timedelta(minutes=-15)
    alarm["TRIGGER"].params["RELATED"] = "UNKNOWN_VALUE"

    assert alarm.TRIGGER_RELATED == "START"


def test_alarm_triggers_structure():
    """Test that alarm.triggers splits into start and end correctly regardless of case."""
    alarm_start = Alarm()
    alarm_start.TRIGGER = timedelta(minutes=-15)
    alarm_start["TRIGGER"].params["RELATED"] = "start"
    triggers_start = alarm_start.triggers
    assert triggers_start.start == (timedelta(minutes=-15),)
    assert triggers_start.end == ()

    alarm_end = Alarm()
    alarm_end.TRIGGER = timedelta(minutes=-15)
    alarm_end["TRIGGER"].params["RELATED"] = "end"
    triggers_end = alarm_end.triggers
    assert triggers_end.start == ()
    assert triggers_end.end == (timedelta(minutes=-15),)
