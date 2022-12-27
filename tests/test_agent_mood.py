import sys
sys.path.insert(0, 'src')

from Agent import MOOD_KEYS
from AgentMood import AgentMood
from AgentMoodFacet import AgentMoodFacet
from AgentTemperament import AgentTemperament

# Define the mood facets for the agent
happiness_facet = AgentMoodFacet(
    key=MOOD_KEYS.happy,
    name='Happiness',
    baseline=10,
    sensitivity=.75,
    strength_labels={
        'content': 50,
        'happy': 75,
        'ecstatic': 100
    }
)
sadness_facet = AgentMoodFacet(
    key=MOOD_KEYS.sad,
    name='Sadness',
    baseline=5,
    sensitivity=1.25,
    strength_labels={
        'sad': 50,
        'depressed': 75,
        'devastated': 100
    }
)

# Define the temperament for the agent
temperament = AgentTemperament(
    facets={happiness_facet.key: happiness_facet, sadness_facet.key: sadness_facet}
)


# Test AgentMood
mood = AgentMood(
    temperament
)
assert mood.temperament == temperament
# assert mood.report == {}

mood.report(
    'test_event1',
    [{'facet_key': MOOD_KEYS.happy, 'start_value': 10}]
)

mood.report(
    'test_event2',
    [{'facet_key': MOOD_KEYS.happy, 'start_value': 15}]
)

mood.report(
    'test_event3',
    [
        {'facet_key': MOOD_KEYS.happy, 'start_value': 25},
        {'facet_key': MOOD_KEYS.sad, 'start_value': 24}
    ]
)

assert mood.evaluate({MOOD_KEYS.happy: 20}) == True
assert mood.evaluate({MOOD_KEYS.happy: 45}) == True
assert mood.evaluate({MOOD_KEYS.happy: 50}) == False

assert mood.evaluate({MOOD_KEYS.sad: 20}) == True

assert mood.evaluate({MOOD_KEYS.happy: 45, MOOD_KEYS.sad: 20}) == True
assert mood.evaluate({MOOD_KEYS.happy: 50, MOOD_KEYS.sad: 20}) == False

# TODO: Tests for resolutions.
