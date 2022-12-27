class AgentMoodEventStore:
    def __init__(self, events):
        """
        Initialize the event store.

        :param events: A list of dehydrated AgentMoodEvent objects
        :type events: list[dict]
        """
        self.events = []
        for event in events:
            self.events.append(AgentMoodEvent.rehydrate(event))

    @property
    def active_events(self):
        """
        Get a list of active events.

        :return: A list of active events
        :rtype: list[AgentMoodEvent]
        """
        return [event for event in self.events if event.is_active]

    @property
    def resolved_events(self):
        """
        Get a list of resolved events.

        :return: A list of resolved events
        :rtype: list[AgentMoodEvent]
        """
        return [event for event in self.events if event.is_resolved]

    @property
    def internalized_events(self):
        """
        Get a list of internalized events.

        :return: A list of internalized events
        :rtype: list[AgentMoodEvent]
        """
        return [event for event in self.events if event.is_internalized]

    @property
    def forgiven_events(self):
        """
        Get a list of forgiven events.

        :return: A list of forgiven events
        :rtype: list[AgentMoodEvent]
        """
        return [event for event in self.events if event.is_forgiven]