class AgentTemperament:
    def __init__(self, facets=[]):
        """
        Initialize the temperament.

        TODO: Add goals -- things the agent wants to achieve/avoid with this temperament

        :param facets: Mood facets, which represent the baseline and sensitivity values for the agent
        :type baselines: dict[str, AgentMoodFacet]
        """
        self.facets = facets
        self.goals = {}  # Stubbed-out class member for agent's temperament-based goals
