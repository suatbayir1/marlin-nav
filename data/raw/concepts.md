---
title: "AI2-THOR"
source: "https://ai2thor.allenai.org/ithor/documentation/concepts"
author:
  - "[[Allen Institute for AI]]"
published:
created: 2026-06-22
description:
tags:
  - "clippings"
---
[NEW](https://procthor.allenai.org/)

[Big News! We've announced ProcTHOR](https://procthor.allenai.org/)

An agent is a capsule shaped entity that can navigate within scenes and interact with objects.

## [Scene](https://ai2thor.allenai.org/ithor/documentation/concepts/#scene)

A scene within AI2-THOR represents a virtual room that an agent can navigate and interact in. There are 4 scene Categories, each with 30 unique scenes within them: Kitchen, Living Room, Bedroom, Bathroom.

## [Action](https://ai2thor.allenai.org/ithor/documentation/concepts/#action)

An action is a discrete command for the agent to perform within a scene (e.g. MoveAhead, RotateRight, PickupObject).

## [Sim Object](https://ai2thor.allenai.org/ithor/documentation/concepts/#sim-object)

A sim object is an object that can be interacted with by the agent. Objects have a range of interactions based on their assigned

ObjectType

.

## [Object Visibility](https://ai2thor.allenai.org/ithor/documentation/concepts/#object-visibility)

An object is considered

visible

when it satisfies two conditions:

1. **In frame**. The object appears in the camera's frame (i.e., it is within the camera's field of view). Even if an object is partially blocked by another object, as long as some of it is in the frame, that is sufficient for this condition.
2. **Proximity**. The object is within a distance of *visibilityDistance* from the agent's central vertical axis. By default, *visibilityDistance* is set to $1.5$ meters, but it can be overwritten upon [initialization](https://ai2thor.allenai.org/ithor/documentation/initialization/#initialization-visibilitydistance).
3. **Obstruction.** The object is not obstructed. Here, a ray emitted from the camera must hit the object without first hitting another object.

Warning

An object rendered in an image will not always be visible to the agent. For example, an object outside the $1.5$ meter threshold could be seen in an image, but will be reported as not-visible to the agent.

Each object's visibility is reported [in the metadata](https://ai2thor.allenai.org/ithor/documentation/environment-state/#object-metadata-visible).

## [Object Interactability](https://ai2thor.allenai.org/ithor/documentation/concepts/#object-interactability)

An object is said to be interactable if it is both

visible

and if it is unobstructed by any other objects. For instance, if a

Sponge

is behind

ShowerGlass

, then it will report

visible

as

True

, but the agent will be unable to interact with it due to the obstruction.

Warning

If an object is interactable, then that implies the object is visible. But, if an object is visible, that does not imply it is interactable.

A

Receptacle

is a type of object that may be the parent of another object. Examples include

TableTop

,

Cup

,

Sofa

,

Bed

,

Desk

, and

Bowl

. The full set of

Receptacle

object types can be filtered on the [Object Types](https://ai2thor.allenai.org/ithor/documentation/objects/object-types).

Navigated to Agent