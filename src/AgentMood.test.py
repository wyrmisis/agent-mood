from AgentMood import Agent, AgentTemperament, AgentMood, AgentMoodFacet, AgentMoodEvent, AgentMoodEventStore
from datetime import datetime, timedelta
from collections import namedtuple

def test_classes():
    # Define the mood facets for the agent
    happiness_facet = AgentMoodFacet(
        key='happiness',
        name='Happiness',
        baseline=50,
        resistance=20,
        sensitivity=None,
        strength_labels={
            'content': 50,
            'happy': 75,
            'ecstatic': 100
        }
    )
    sadness_facet = AgentMoodFacet(
        key='sadness',
        name='Sadness',
        baseline=50,
        resistance=None,
        sensitivity=20,
        strength_labels={
            'sad': 50,
            'depressed': 75,
            'devastated': 100
        }
    )

    # Define the temperament for the agent
    temperament = AgentTemperament({
        mood_key: facet.modifiers for mood_key, facet in [
            (happiness_facet.key, happiness_facet),
            (sadness_facet.key, sadness_facet),
        ]
    })

    # Define the mood for the agent
    mood = AgentMood(temperament)

    # Create the agent
    agent = Agent('Test Agent')

    print(happiness_facet.strength_labels)

    # Test AgentMoodFacet
    assert happiness_facet.get_strength_label(50) == 'content'
    assert happiness_facet.get_strength_label(75) == 'happy'
    assert happiness_facet.get_strength_label(100) == 'ecstatic'
    assert happiness_facet.modifiers == {'baseline': 50, 'resistance': 20, 'sensitivity': None}

    assert sadness_facet.get_strength_label(50) == 'sad'
    assert sadness_facet.get_strength_label(75) == 'depressed'
    assert sadness_facet.get_strength_label(100) == 'devastated'
    assert sadness_facet.modifiers == {'baseline': 50, 'resistance': None, 'sensitivity': 20}

    # Test AgentTemperament
    assert temperament.get_modifiers('happiness') == {'baseline': 50, 'resistance': 20, 'sensitivity': None}
    assert temperament.get_modifiers('sadness') == {'baseline': 50, 'resistance': None, 'sensitivity': 20}

    # Test AgentMood
    assert mood.get_mood_report() == {'happiness': 50, 'sadness': 50}

    # Test AgentMoodEventImpact
    impact = AgentMoodEventImpact('happiness', 50)
    assert impact.facet_key == 'happiness'
    assert impact.start_date is not None
    assert impact.start_value == 50
    assert impact.decay_rate == 0
    assert impact.decay_date is None
    assert impact.report == {'happiness': 50}

    impact = AgentMoodEventImpact('happiness', 50, decay_rate=0.1, decay_date=datetime.now() + timedelta(days=1))
    assert impact.facet_key == 'happiness'
    assert impact.start_date is not None
    assert impact.start_value == 50
    assert impact.decay_rate == 0.1
    assert impact.decay_date is not None
    assert impact.report == {'happiness': 50}  # Value will only decay after decay_date

    # Test AgentMoodEvent
    event = AgentMoodEvent('event_key', impact)
    assert event.event_key == 'event_key'
    assert event.impact == impact
    assert event.actor_at_fault == 'player'
    assert event.is_internalized is False
    assert event.internalization_resolution is None
    assert event.internalization_duration is None
    assert event.is_resolved is False
    assert event.resolution_duration is None
    assert event.is_active is True
    assert event.is_forgiven is False
    assert event.is_unresolved_and_unforgiven is True
    assert event.is_unresolved_and_forgiven is False
    assert event.is_resolved_and_unforgiven is False
    assert event.is_resolved_and_forgiven is False

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
    assert event.impact == impact
    assert event.actor_at_fault == 'player'
    assert event.is_internalized is True
    assert event.internalization_resolution == 'acceptance'
    assert event.internalization_duration == timedelta(days=1)
    assert event.is_resolved is True
    assert event.resolution_duration == timedelta(days=2)
    assert event.is_active is False
    assert event.is_forgiven is True
    assert event.is_unresolved_and_unforgiven is False
    assert event.is_unresolved_and_forgiven is False
    assert event.is_resolved_and_unforgiven is False
    assert event.is_resolved_and_forgiven is True

    event_data = AgentMoodEvent.dehydrate(event)
    assert event_data == {
        'event_key': 'event_key',
        'impact': impact,
        'actor_at_fault': 'player',
        'is_internalized': True,
        'internalization_resolution': 'acceptance',
        'internalization_duration': timedelta(days=1),
        'is_resolved': True,
        'resolution_duration': timedelta(days=2)
    }
    event_copy = AgentMoodEvent.rehydrate(event_data)
    assert event_copy.event_key == event.event_key
    assert event_copy.impact == event.impact
    assert event_copy.actor_at_fault == event.actor_at_fault
    assert event_copy.is_internalized == event.is_internalized
    assert event_copy.internalization_resolution == event.internalization_resolution
    assert event_copy.internalization_duration == event.internalization_duration
    assert event_copy.is_resolved == event.is_resolved
    assert event_copy.resolution_duration == event.resolution_duration

    # Test AgentMood
    mood = AgentMood(temperament, [impact])
    assert mood.temperament == temperament
    assert mood.event_store.events == [event]
    assert mood.facets == [happiness]
    assert mood.mood_report == {
        'happiness': 50
    }

    mood.report_event(event)
    assert mood.event_store.events == [event, event]
    assert mood.mood_report == {
        'happiness': 100
    }

    mood.resolve_events()
    assert mood.event_store.events == []
    assert mood.mood_report == {
        'happiness': 0
    }

    # Test AgentTemperament
    temperament = AgentTemperament({
        'happiness': {
            'baseline': 50,
            'sensitivity': 0.5,
            'resistance': 1.5
        }
    })
    assert temperament.report == {
        'happiness': {
            'baseline': 50,
            'sensitivity': 0.5,
            'resistance': 1.5
        }
    }


test_classes()
