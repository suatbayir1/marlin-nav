---
title: "AI2-THOR"
source: "https://ai2thor.allenai.org/ithor/documentation/initialization"
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

After installing AI2-THOR, we can initialize a controller, which will allow us to execute actions in the environment.

```python
from ai2thor.controller import Controller

controller = Controller(
    agentMode="default",
    visibilityDistance=1.5,
    scene="FloorPlan212",

    # step sizes
    gridSize=0.25,
    snapToGrid=True,
    rotateStepDegrees=90,

    # image modalities
    renderDepthImage=False,
    renderInstanceSegmentation=False,

    # camera properties
    width=300,
    height=300,
    fieldOfView=90
)
```

### Controller Parameters#### [agentMode](https://ai2thor.allenai.org/ithor/documentation/initialization/#initialization-agentmode)

[: str = "default"](https://ai2thor.allenai.org/ithor/documentation/initialization/#initialization-agentmode)

The type of agent that will interact with the scene. For iTHOR, stick with

agentMode="default"

. RoboTHOR provides the

locobot

as an

agentMode

option, and ManipulaTHOR provides the

arm

as an

agentMode

option.#### [visibilityDistance](https://ai2thor.allenai.org/ithor/documentation/initialization/#initialization-visibilitydistance)

[: float = 1.5](https://ai2thor.allenai.org/ithor/documentation/initialization/#initialization-visibilitydistance)

Used to set the maximum goal distance in meters between the agent and an object. This affects each object's

visible

property, where, when

True

, then the agent is within

visibilityDistance

of that object and the object appears in the agent's current egocentric frame.#### [scene](https://ai2thor.allenai.org/ithor/documentation/initialization/#initialization-scene)

[: Optional\[str\] = None](https://ai2thor.allenai.org/ithor/documentation/initialization/#initialization-scene)

The name of which scene to initialize. Valid iTHOR scenes are listed [here](https://ai2thor.allenai.org/ithor/documentation/scenes). If unspecified and the

default

agent is being used, an iTHOR scene will be chosen at random.#### [gridSize](https://ai2thor.allenai.org/ithor/documentation/initialization/#initialization-gridsize)

[: float = 0.25](https://ai2thor.allenai.org/ithor/documentation/initialization/#initialization-gridsize)

The amount, in meters, that the agent moves after calling a move action (e.g.,

MoveAhead

and

MoveBack

).#### [snapToGrid](https://ai2thor.allenai.org/ithor/documentation/initialization/#initialization-snaptogrid)

[: bool = True](https://ai2thor.allenai.org/ithor/documentation/initialization/#initialization-snaptogrid)

Determines whether the agent’s position is snapped to a grid point after any movement action (e.g.,

MoveAhead

and

TeleportFull

). Grid points are spaced out by

gridSize

. Set to

False

to allow diagonal movement.#### [rotateStepDegrees](https://ai2thor.allenai.org/ithor/documentation/initialization/#initialization-rotatestepdegrees)

[: float = 90](https://ai2thor.allenai.org/ithor/documentation/initialization/#initialization-rotatestepdegrees)

The default amount, in degrees, that the agent rotates after calling a rotate action (i.e.,

RotateLeft

or

RotateRight

).#### [renderDepthImage](https://ai2thor.allenai.org/ithor/documentation/initialization/#initialization-renderdepthimage)

[: bool = False](https://ai2thor.allenai.org/ithor/documentation/initialization/#initialization-renderdepthimage)

When

True

, a depth frame is rendered and made available as an

event.depth\_frame

attribute.

Remark

We require this to be explicitly passed in because rendering depth takes longer than rendering RGB alone.#### [renderInstanceSegmentation](https://ai2thor.allenai.org/ithor/documentation/initialization/#initialization-renderinstancesegmentation)

[: bool = False](https://ai2thor.allenai.org/ithor/documentation/initialization/#initialization-renderinstancesegmentation)

When

True

, a instance segmentation frame is rendered and made available as an

event.instance\_segmentation\_frame

attribute. Instance segmentation provides segmentation by object instance, where all objects in view are distinguishable.

Remark

We require this to be explicitly passed in because rendering instance segmentation takes longer than rendering RGB alone.#### [width](https://ai2thor.allenai.org/ithor/documentation/initialization/#initialization-width)

[: int = 300](https://ai2thor.allenai.org/ithor/documentation/initialization/#initialization-width)

The number of horizontal sampled pixels for each frame. This affects every rendered image frame (e.g.,

event.frame

,

event.depth\_frame

,

event.cv2img

).#### [height](https://ai2thor.allenai.org/ithor/documentation/initialization/#initialization-height)

[: int = 300](https://ai2thor.allenai.org/ithor/documentation/initialization/#initialization-height)

The number of vertical sampled pixels for each frame. This affects every rendered image frame (e.g.,

event.frame

,

event.depth\_frame

,

event.cv2img

).#### [fieldOfView](https://ai2thor.allenai.org/ithor/documentation/initialization/#initialization-fieldofview)

[: int = 90](https://ai2thor.allenai.org/ithor/documentation/initialization/#initialization-fieldofview)

Changes the camera's optical field of view, in degrees. Valid values are in the domain $(0:180)$. The default field of view when

agentMode="default"

is 90 degrees.

<iframe src="https://player.vimeo.com/video/554179934?autoplay=1&amp;loop=1&amp;muted=1&amp;autopause=0" frameborder="0" allow="autoplay; fullscreen; picture-in-picture" allowfullscreen=""></iframe>

Warning

Not all agent modes have the same default

fieldOfView

. For instance, the

locobot

has a default

fieldOfView

of $60$ degrees.

## [Reset](https://ai2thor.allenai.org/ithor/documentation/initialization/#reset)

Any parameter can later be changed by calling the reset method. For instance, we can call:

```python
controller.reset(scene="FloorPlan319", rotateStepDegrees=30)
```

The values will default to what they were upon the most recent reset or initialization. For instance, if you initialized with

fieldOfView=45

, then called

reset

with

fieldOfView=60

, calling

reset

again, without passing in

fieldOfView

will keep

fieldOfView=60

.

By default, AI2-THOR executes high-level actions that provide a response from the environment after the action completes execution. For instance, if the agent successfully executes an

OpenObject

action, the response is the state of the environment after the action has completely finished executing.

However, we also provide the ability to observe intermediate results, which is discussed in this section.

PausePhysicsAutoSim

toggles off auto-simulation in the environment, which must be called before one can control how much time passes in-between steps.

```python
controller.step("PausePhysicsAutoSim")
```

AdvancePhysicsStep

responds with an Event after simulating the environment for

timeStep

seconds beyond the current state. Note that

PausePhysicsAutoSim

must be called first, before calling

AdvancePhysicsStep

.

```python
controller.step(
    action="AdvancePhysicsStep",
    timeStep=0.01
)
```

### Advance Physics Step Parameters

The amount of time in seconds to advance the physics simulation. Valid values are in $(0:0.05]$.

UnpausePhysicsAutoSim

toggles back on the default physics auto-simulation, which returns future events after the action finishes execution.

Warning

Unpausing auto-simulation while objects are still in motion (i.e.,

inMotion=True

on an object's metadata) will freeze each object at its current location. Thus, the remaining motion of such an object will be lost.

To capture the entire movement of an object, do not unpause physics with this action until all objects return

inMotion=False

in their object metadata, which can also be checked with the shorthand of

event.metadata\["isSceneAtRest"\]

.

```python
controller.step("UnpausePhysicsAutoSim")
```

Navigated to Initialization