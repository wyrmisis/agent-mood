import sys
sys.path.insert(0, 'src')

from AgentMoodFacet import AgentMoodFacet

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

# Test AgentMoodFacet
assert happiness_facet.get_strength_label(50) == 'content'
assert happiness_facet.get_strength_label(75) == 'happy'
assert happiness_facet.get_strength_label(100) == 'ecstatic'
assert happiness_facet.modifiers == {'baseline': 10, 'sensitivity': .75}

assert sadness_facet.get_strength_label(50) == 'sad'
assert sadness_facet.get_strength_label(75) == 'depressed'
assert sadness_facet.get_strength_label(100) == 'devastated'
assert sadness_facet.modifiers == {'baseline': 5, 'sensitivity': 1.25}