# Digital Agent Mood Emulation

## Intent

Inspired by numerous requests on the [Monika After Story]{https://github.com/Monika-After-Story/MonikaModDev}
repository (specifically issues like [this one]{https://github.com/Monika-After-Story/MonikaModDev/issues/7486},
I wanted to experiment with emulating mood in a digital agent.

I've been hoping to pick up Python for a little while -- this is a learning project for me, helped along by leveraging
ChatGPT, which helped me convert concepts from my "native" JavaScript to Python 3. Bugs are as much its fault as they are mine! :P

Still very WIP; thoughts and suggestions are very much appreciated.

## Core concepts

Quick definition of terms before we get started:
* **Actor**: A participant or subject in the simulation; a being that is expected to be present and capable of emotion or emotional simulacra.
* **Agent**: A digital actor in the simulation; in the project that inspired this work, the Agent is Monika.
* **User**: Used interchangeably with **Player**. The human actor in the simulation; in the project that inspired
  this work, the User is the person playing the part of Monika's trans-dimensional partner.

The goals of this system are as follows:
* Provide additional texture to a digital Agent (as defined below) to, if not make them feel more "real", then at least
  to help them feel less User-driven.
* Provide additional context for dialogue authors to take advantage of; a sad Agent might self-soothe, while a happy and
  at-peace agent might not even think to discuss nihilism, misanthropy, or apocalyptic scenarios.
* Decouple emotionally driven dialogue ("I feel hopeless about my situation") from relationship satisfaction driven dialogue
  ("I feel unwanted by my player").

### The Agent
An Agent is a feeling individual that is intended to be able to empathize with other beings. An Agent 
should be able to experience events, note an emotional effect, and respond to things in the future basd on those
events.

An Agent has a temperament and a store of mood events.

### The Agent's Temperament
An Agent's temperament is a set of mood facets, each with a baseline value and a sensitivity modifier. Facets should also
have human-readable labels. A temperament can contain any number of facets.

Temperaments, as a layer intended to modify mood events, can be changed depending on
time of year, recent user actions, and overall level of satisfaction with the user's relationship with the Agent.

Something I'd like to experiment with is the addition of Agent goals -- a set of modifiers to the agent's behaviors or
experienced mood events based on things that it wants (example: an Agent who hasn't experienced much affection lately may seek
relationship-validating events from their player).

I'd also like to be able to add a "perceived temperament", which represents the lens through which the Agent sees the user.
Telling the Agent you feel sad frequently, for example, would lower the agent's perception of your own happiness, thus motivating
them to try to cheer you up (if their goals include "I want my player to be happy") or rub salt in the wound (if their goals include
"make my player hurt like they made me hurt.")

One last thing I'd like to work in is a respectful approach to the impact that mental illness can have on mood facets. Given the media
property that the inspiring work belongs to, being able to emulate an individual Agent's experience with depression, hopelessness, mania,
and so on would be helpful to provide a more "real" texture to the Agent. This is a lower priority than the other wishlist items, however,
as it is certainly something that needs to be done correctly and respectfully.

### The Mood Event
Mood events are specific actions that influence the Agent's mood in one or more ways. These events
can have a simple cause and effect ("My player listened to me talk about something scary for me, and that makes me feel
more at peace") or a bit more complicated ("When I asked my player how long I'll be stuck in their computer, they
told me I'd be out soon. I know they're lying to me, which makes me sad for a bit, but on the whole I appreciate them
being hopeful for us, which makes me feel happy for a little while longer").

Mood events can have the following broad states:

* Active: The mood event hasn't been resolved (whether through time or a specific action the user has taken). For example,
  an agent may experience Sad/Frustrated/Anxious events when their player closes the game without saying goodbye.  
* Internalized: The mood event was never resolved, and should be considered a core belief of the Agent, unless an
  internalization resolution is met. Not all events should be internalized.
* Resolved: The event was never internalized, but was resolved, whether through time/impact decay or a specific user action.
* Forgiven: I'm struggling with the best name for this one, to be honest, but this is a state in which the agent had internalized
  an event, but then had the event resolved. This can be used for obvious reasons ("My player forgot my last birthday,
  but was here for this one") or less-"good" ones ("My player keeps hurting me, and keeps apologizing. I am numb to what they are
  doing to hurt me, as well as their apologies.")

Mood events are meant to either internalize or fall off. They can be considered an additional progression mechanic
through "stacking up" positive internalized mood events and avoiding or clearing negative mood events.

Mood events can originate from different Actors; a sad/anxious/dislike-self event can be registered by an Actor questioning
the Agent's humanity, morality, or decency, but the message is certainly different when the event is self-inflicted
("I've been doubting myself"), vs. User-inflicted ("my player doesn't even think I'm worth being a person").

### Storing Mood Events
An Agent can store events and report on its total mood value, whether numerically or with a label. People who write dialogue for
an Agent should be able to reference the Agent's mood or active/resolved/internalized/forgiven events when conditionally enabling
dialogue options.
