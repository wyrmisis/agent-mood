from collections import namedtuple

# Define the keys for the mood facets
MoodKeys = namedtuple('MoodKeys', ['happy', 'sad'])
MOOD_KEYS = MoodKeys('happiness', 'sadness')


class Agent:
    def __init__(self, name):
        self.name = name
        self.mood = AgentMood()

    def report_event(self, event):
        self.mood.report_event(event)

    def resolve_events(self):
        self.mood.resolve_events()

    def get_mood(self, mood_filters):
        return self.mood.evaluate(mood_filters)
