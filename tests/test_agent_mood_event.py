import sys
from datetime import datetime, timedelta

sys.path.insert(0, 'src')

from AgentMoodEvent import AgentMoodEvent
from AgentMoodEventImpact import AgentMoodEventImpact

impact = AgentMoodEventImpact('happiness', 50)

# Test AgentMoodEvent
event = AgentMoodEvent('event_key', impact)
assert event.event_key == 'event_key'
assert event.impact == [impact]
assert event.actor_at_fault == 'player'
assert event.is_internalized is False
assert event.internalization_resolution is None
assert event.internalization_duration is None
assert event.is_resolved is False
assert event.resolution_duration is None
assert event.is_active is True
assert event.is_forgiven is False

event = AgentMoodEvent(
    'event_key',
    impact,
    is_internalized=True,
    internalization_resolution='acceptance',
    internalization_duration=timedelta(days=1),
    is_resolved=True,
    resolution_duration=timedelta(days=2)
)
assert event.event_key == 'event_key'
assert event.impact == [impact]
assert event.actor_at_fault == 'player'
assert event.is_internalized is True
assert event.internalization_resolution == 'acceptance'
assert event.internalization_duration == timedelta(days=1)
assert event.is_resolved is True
assert event.resolution_duration == timedelta(days=2)
assert event.is_active is False
assert event.is_forgiven is True

# Test dehydration
event_data = AgentMoodEvent.dehydrate(event)
assert event_data['event_key'] == 'event_key'
assert event_data['impact'] == [impact]
assert event_data['actor_at_fault'] == event.actor_at_fault
assert event_data['is_internalized'] == event.is_internalized
assert event_data['internalization_resolution'] == event.internalization_resolution
assert event_data['internalization_duration'] == event.internalization_duration
assert event_data['is_resolved'] == event.is_resolved
assert event_data['resolution_duration'] == event.resolution_duration

# Test rehydration
event_copy = AgentMoodEvent.rehydrate(event_data)
assert event_copy.event_key == event.event_key
assert event_copy.impact == [impact]
assert event_copy.actor_at_fault == event.actor_at_fault
assert event_copy.is_internalized == event.is_internalized
assert event_copy.internalization_resolution == event.internalization_resolution
assert event_copy.internalization_duration == event.internalization_duration
assert event_copy.is_resolved == event.is_resolved
assert event_copy.resolution_duration == event.resolution_duration