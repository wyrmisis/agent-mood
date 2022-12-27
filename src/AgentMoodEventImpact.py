from datetime import datetime, timedelta

class AgentMoodEventImpact:
    def __init__(
        self,
        facet_key,
        value,
        start_date=None,
        decay_date=None,
    ):
        self._facet_key = facet_key
        self._start_date = start_date or datetime.now()
        self._start_value = value
        self._decay_date = decay_date

    @staticmethod
    def dehydrate(impact):
        """
        Convert an AgentMoodEventImpact instance to a dictionary for storage.

        :param impact: The impact to dehydrate
        :type impact: AgentMoodEventImpact
        :return: A dictionary representation of the impact
        :rtype: dict
        """
        data = {
            'facet_key': impact._facet_key,
            'start_date': impact._start_date,
            'start_value': impact._start_value,
            'decay_date': impact._decay_date,
        }
        return data

    @staticmethod
    def rehydrate(data):
        """
        Convert a dictionary to an AgentMoodEventImpact instance.

        :param data: The dictionary to rehydrate
        :type data: dict
        :return: An AgentMoodEventImpact instance
        :rtype: AgentMoodEventImpact
        """
        impact = AgentMoodEventImpact(
            data['facet_key'],
            data['start_value'],
            data.get('start_date', None),
            data.get('decay_date', None),
        )
        return impact


    @property
    def report(self):
        if self._decay_date:
            total_minutes = (self._decay_date - self._start_date).total_seconds() / 60
            remaining_minutes = (self._decay_date - datetime.now()).total_seconds() / 60
            decay_factor = remaining_minutes / total_minutes
            if (decay_factor < 0):
                decay_factor = 0

            value = self._start_value * decay_factor
        else:
            value = self._start_value

        return {
            self._facet_key: round(value, 2)
        }