from AgentMoodEventImpact import AgentMoodEventImpact

class AgentMoodEvent:
    def __init__(
        self,
        event_key,
        impact,
        actor_at_fault="player",
        is_internalized=False,
        internalization_resolution=None,
        internalization_duration=None,
        is_resolved=False,
        resolution_duration=None
    ):
        self.event_key = event_key
        if not isinstance(impact, list):
            self.impact = [impact]
        else:
            self.impact = impact
        for item in impact:
            if not isinstance(item, AgentMoodEventImpact):
                item = AgentMoodEventImpact.rehydrate(item)
        self.actor_at_fault = actor_at_fault
        self._is_internalized = is_internalized
        self.internalization_resolution = internalization_resolution
        self.internalization_duration = internalization_duration
        self._is_resolved = is_resolved
        self.resolution_duration = resolution_duration

    @staticmethod
    def dehydrate(event):
        """
        Convert an AgentMoodEvent instance to a dictionary for storage.

        :todo - dehydrate event impacts as well

        :param event: The event to dehydrate
        :type event: AgentMoodEvent
        :return: A dictionary representation of the event
        :rtype: dict
        """
        data = {
            'event_key': event.event_key,
            'impact': event.impact,
            'actor_at_fault': event.actor_at_fault,
            'is_internalized': event._is_internalized,
            'internalization_resolution': event.internalization_resolution,
            'internalization_duration': event.internalization_duration,
            'is_resolved': event._is_resolved,
            'resolution_duration': event.resolution_duration
        }
        return data

    @staticmethod
    def rehydrate(data):
        """
        Convert a dictionary to an AgentMoodEvent instance.

        :param data: The dictionary to rehydrate
        :type data: dict
        :return: An AgentMoodEvent instance
        :rtype: AgentMoodEvent
        """
        rehydrated_impacts = list(map(AgentMoodEventImpact.rehydrate, data['impact']))
        event = AgentMoodEvent(
            data['event_key'],
            rehydrated_impacts,
            data['actor_at_fault'],
            data['is_internalized'],
            data['internalization_resolution'],
            data['internalization_duration'],
            data['is_resolved'],
            data['resolution_duration']
        )
        return event

    # Report event status
    @property
    def is_active(self):
        """
        Check if the event is both unresolved and not internalized.

        :return: True if the event is active, False otherwise
        :rtype: bool
        """
        return not self.is_resolved and not self.is_internalized

    @property
    def is_forgiven(self):
        """
        Check if the event is both resolved and internalized.

        :return: True if the event is forgiven, False otherwise
        :rtype: bool
        """
        return self.is_resolved and self.is_internalized

    @property
    def is_internalized(self):
        """
        Check if the event is internalized.

        An event is internalized if the "is_internalized" parameter is True,
        or the current date is equal to or after the internalization_duration.

        :return: True if the event is internalized, False otherwise
        :rtype: bool
        """
        if self._is_internalized:
            return True
        elif self.internalization_duration:
            return datetime.now() >= self.internalization_duration
        else:
            return False

    @property
    def is_resolved(self):
        """
        Check if the event is resolved.

        An event is resolved if the "is_resolved" parameter is True,
        or the current date is equal to or after the resolution_duration,
        or all entries in the report dictionary are 0.

        :return: True if the event is resolved, False otherwise
        :rtype: bool
        """
        if self._is_resolved:
            return True
        elif self.resolution_duration:
            return datetime.now() >= self.resolution_duration
        elif all(value == 0 for value in self.report.values()):
            return True
        else:
            return False

    @property
    def report(self):
        """
        Get the combined dictionary of AgentMoodEventImpact.report calls.

        :return: The combined dictionary of AgentMoodEventImpact.report calls
        :rtype: dict
        """
        impacts = {}
        for impact in self.impact:
            impacts.update(impact.report)
        return {
            'event': self.event_key,
            'actor_at_fault': self.actor_at_fault,
            'impact': impacts
        }