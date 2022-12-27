import sys
from datetime import datetime, timedelta

sys.path.insert(0, 'src')

from AgentMoodEventImpact import AgentMoodEventImpact

# Test AgentMoodEventImpact
impact = AgentMoodEventImpact('happiness', 50)
assert impact._facet_key == 'happiness'
assert impact._start_date is not None
assert impact._start_value == 50
assert impact._decay_date is None
assert impact.report == {'happiness': 50}

# This impact is at full strength but will decay off in one day.
impact = AgentMoodEventImpact('happiness', 50, decay_date=datetime.now() + timedelta(days=1))
assert impact._facet_key == 'happiness'
assert impact._start_date is not None
assert impact._start_value == 50
assert impact._decay_date is not None
assert impact.report == {'happiness': 50}

# This impact should be halfway to decaying off
impact = AgentMoodEventImpact('happiness', 50, start_date=datetime.now() - timedelta(days=1), decay_date=datetime.now() + timedelta(days=1))
assert impact._facet_key == 'happiness'
assert impact._start_date is not None
assert impact._start_value == 50
assert impact._decay_date is not None
assert impact.report == {'happiness': 25}

# This impact has decayed off
impact = AgentMoodEventImpact('happiness', 50, start_date=datetime.now() - timedelta(days=2), decay_date=datetime.now() - timedelta(days=1))
assert impact._facet_key == 'happiness'
assert impact._start_date is not None
assert impact._start_value == 50
assert impact._decay_date is not None
assert impact.report == {'happiness': 0}

# Data hydration/dehydration setup
impact = AgentMoodEventImpact('facet_key', 50.0, datetime.now(), datetime.now() + timedelta(days=1))

# Dehydrate the impact
data = AgentMoodEventImpact.dehydrate(impact)

# Rehydrate the impact
rehydrated_impact = AgentMoodEventImpact.rehydrate(data)

# Assert that the original impact and the rehydrated impact are the same
assert impact._facet_key == rehydrated_impact._facet_key
assert impact._start_date == rehydrated_impact._start_date
assert impact._start_value == rehydrated_impact._start_value
assert impact._decay_date == rehydrated_impact._decay_date