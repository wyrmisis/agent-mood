from datetime import datetime, timedelta
from AgentMoodEventStore import AgentMoodEventStore
from AgentMoodEvent import AgentMoodEvent
from AgentMoodEventImpact import AgentMoodEventImpact

class AgentMood:
    def __init__(
        self,
        temperament,
        dehydrated_events=None,
        dehydrated_beliefs=None
    ):
        self.temperament = temperament
        self.events = AgentMoodEventStore(dehydrated_events or [])

    def report(self, event_key, impact, *, actor_at_fault='player', is_internalized=False, internalization_resolution=None, internalization_duration=None, is_resolved=False, resolution_duration=None):
        """
        Report an event to the AgentMood instance.

        :param event_key: The key for the event to report
        :type event_key: str
        :param impact: The impact of the event to report
        :type impact: list[dict]
        :param actor_at_fault: The actor responsible for the event
        :type actor_at_fault: str
        :param is_internalized: Whether the event has been internalized or not
        :type is_internalized: bool
        :param internalization_resolution: The resolution for internalizing the event
        :type internalization_resolution: str
        :param internalization_duration: The duration for internalizing the event
        :type internalization_duration: datetime
        :param is_resolved: Whether the event has been resolved or not
        :type is_resolved: bool
        :param resolution_duration: The duration for resolving the event
        :type resolution_duration: datetime
        :return: The reported event
        :rtype: AgentMoodEvent
        """
        rehydrated_impacts = list(map(AgentMoodEventImpact.rehydrate, impact))
        # Create a new event
        event = AgentMoodEvent(
            event_key,
            rehydrated_impacts,
            actor_at_fault,
            is_internalized,
            internalization_resolution,
            internalization_duration,
            is_resolved,
            resolution_duration
        )
        self.events.events.append(event)
        return event

    def check_resolutions(self):
        """
        A stubbed function to check active events and internalized events for resolution

        TODO: Check and flip active events, if appropriate
        TODO: Check and flip internalized events, if appropriate
        """
        return False

    def evaluate(self, conditions):
        """
        Evaluate the mood of the Agent based on the given conditions.

        :param conditions: The conditions to evaluate
        :type conditions: dict
        :return: True if the conditions are met, False otherwise
        :rtype: bool
        """
        # Calculate the current mood
        facets = self.temperament.facets
        # Initialize a dictionary to hold the total values of each mood facet
        total_values = {}
        condition_keys = conditions.keys()

        # Iterate through the active events
        for event in self.events.active_events:
            event_impact_report = event.report["impact"]
            for facet_key, value in event_impact_report.items():
                if not facet_key in condition_keys:
                    continue
                if facet_key in total_values:
                    total_values[facet_key] += value
                else:
                    total_values[facet_key] = value

        for value_key, value in total_values.items():
            total_values[value_key] = facets[value_key].get_modified_value(value)

        # Check if the conditions are met
        for facet, value in conditions.items():
            if total_values.get(facet, 0) < value:
                return False
        return True
