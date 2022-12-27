class AgentMoodFacet:
    def __init__(self, key, name, baseline, sensitivity, strength_labels=None):
        self.key = key
        self.name = name
        self.baseline = baseline
        self.sensitivity = sensitivity
        self.strength_labels = strength_labels or {}

    def get_strength_label(self, strength):
        """
        Get the strength label for the given strength.

        :param strength: The strength to get the label for
        :type strength: int
        :return: The strength label, or None if no label exists
        :rtype: str or None
        """
        sorted_labels = sorted(self.strength_labels.items(), key=lambda item: item[1], reverse=True)
        for label, min_strength in sorted_labels:
            if strength >= min_strength:
                return label
        return None

    @property
    def modifiers(self):
        """
        Get the modifiers for the mood facet.

        :return: A dictionary containing the baseline, resistance, and sensitivity for the mood facet
        :rtype: dict
        """
        return {
            'baseline': self.baseline,
            'sensitivity': self.sensitivity
        }

    def get_modified_value(self, value):
        return self.baseline + (value * self.sensitivity)