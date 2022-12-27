import sys
sys.path.insert(0, 'src')

from Agent import MoodKeys
from AgentMoodFacet import AgentMoodFacet
from AgentTemperament import AgentTemperament

# Define the mood facets for the agent
happiness_facet = AgentMoodFacet(
    key='happiness',
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
    key='sadness',
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

# Test AgentTemperament
assert temperament.get_facet_modified_value('happiness', 0) == 10
assert temperament.get_facet_modified_value('happiness', 10) == 17.5
assert temperament.get_facet_modified_value('sadness', 0) == 5
assert temperament.get_facet_modified_value('sadness', 15) == 23.75