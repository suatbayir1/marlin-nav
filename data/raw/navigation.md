---
title: "AI2-THOR"
source: "https://ai2thor.allenai.org/ithor/documentation/navigation"
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

Move the agent in a cardinal direction, relative to it's forward facing direction. Supported action directions are

MoveAhead

,

MoveBack

,

MoveLeft

, and

MoveRight

.

```python
controller.step(
    action="MoveAhead",
    moveMagnitude=None
)

# Other supported directions
controller.step("MoveBack")
controller.step("MoveLeft")
controller.step("MoveRight")
```

### Movement Parameters#### [moveMagnitude](https://ai2thor.allenai.org/ithor/documentation/navigation/#MoveAhead-movemagnitude)

[: Optional\[float\] = None](https://ai2thor.allenai.org/ithor/documentation/navigation/#MoveAhead-movemagnitude)

Overrides the initialized step size of

gridSize

. The units are specified in meters. By default, the

gridSize

is initialized to 0.25 meters.

## [Agent Rotation](https://ai2thor.allenai.org/ithor/documentation/navigation/#agent-rotation)

Changes the yaw rotation of the agent's body. Supported action directions are

RotateRight

and

RotateLeft

.

```python
controller.step(
    action="RotateRight",
    degrees=None
)

# Other supported direction
controller.step("RotateLeft")
```

### Rotate Parameters#### [degrees](https://ai2thor.allenai.org/ithor/documentation/navigation/#RotateRight-degrees)

[: Optional\[float\] = None](https://ai2thor.allenai.org/ithor/documentation/navigation/#RotateRight-degrees)

Overrides the initialized rotation amount of

rotateStepDegrees

.

## [Camera Rotation](https://ai2thor.allenai.org/ithor/documentation/navigation/#camera-rotation)

We can adjust the camera's pitch by utilizing the

LookUp

and

LookDown

commands. Both increment in $30^\circ$ intervals, with angles being clamped between $60^\circ$ in the downward direction and $30^\circ$ in the upward direction.

```python
controller.step(
    action="LookUp",
    degrees=30
)

# Other supported direction
controller.step("LookDown")
```

### Camera Rotation Parameters#### [degrees](https://ai2thor.allenai.org/ithor/documentation/navigation/#LookUp-degrees)

[: float = 30](https://ai2thor.allenai.org/ithor/documentation/navigation/#LookUp-degrees)

Specifies the number of degrees to look up or down. Must be greater than $0$.

```python
controller.step(action="Crouch")
```

### Crouch Description

Crouches the agent from a standing position. The standing position is roughly $0.22$ meters taller than the crouching position.

```python
controller.step(action="Stand")
```

### Stand Description

Stands the agent from a crouching position. The crouching position is roughly $0.22$ meters shorter than the standing position.

Teleport

allows the agent to set its pose to anywhere in the scene in a single step. Valid poses do not place the agent outside the outer boundaries of the scene or in an area that it collides with an object.

```python
controller.step(
    action="Teleport",
    position=dict(x=1, y=0.9, z=-1.5),
    rotation=dict(x=0, y=270, z=0),
    horizon=30,
    standing=True
)
```

### Teleport Parameters

The position of the agent's body in global 3D coordinate space. If unspecified, the position of the agent remains the same.

The rotation of the agent's body in global 3D space. Here, the rotation changes the [agent's yaw rotation](https://ai2thor.allenai.org/ithor/documentation/navigation/#sub-agent-rotation).

Remark

The default agent's body cannot change in pitch or roll; hence, why the $x, z=0$.

If unspecified, the rotation of the agent remains the same.

The

horizon

change's the [camera's rotation](https://ai2thor.allenai.org/ithor/documentation/navigation/#sub-camera-rotation). Values are clamped between \[-30:60\].

Since the agent looks up and down in $30^\circ$ increments, it most common for the horizon to be in $\lbrace -30, 0, 30, 60\rbrace$.

Warning

Negative camera

horizon

values correspond to agent looking up, whereas positive

horizon

values correspond to the agent looking down.

If unspecified, the horizon of the agent remains the same.

Denotes whether the agent is in a standing or crouched position. If unspecified, the standing state of the agent remains the same.

In addition to being able to

Teleport

, we also have an equivalent action

TeleportFull

that strictly requires every degree of freedom to be specified. The strictness of this action is often useful in large projects, where we don't want to any part of the agent implied implicitly.

Warning

TeleportFull

does not guarantee backwards compatibility in future releases. If a new degree of freedom is added to the agent, it will be added as a required parameter. If this is an issue, we recommend using

Teleport

.

```python
controller.step(
    action="TeleportFull",
    position=dict(x=1, y=0.9, z=-1.5),
    rotation=dict(x=0, y=270, z=0),
    horizon=30,
    standing=True
)
```

### TeleportFull Parameters

required

The position of the agent's body in global 3D coordinate space.

required

The rotation of the agent's body in global 3D space. Here, the rotation changes the [agent's yaw rotation](https://ai2thor.allenai.org/ithor/documentation/navigation/#sub-agent-rotation).

Remark

The default agent's body cannot change in pitch or roll; hence, why the $x, z=0$.

required

The

horizon

change's the [camera's rotation](https://ai2thor.allenai.org/ithor/documentation/navigation/#sub-camera-rotation). Values are clamped between \[-30:60\].

Since the agent looks up and down in $30^\circ$ increments, it most common for the horizon to be in $\lbrace -30, 0, 30, 60\rbrace$.

Warning

Negative camera

horizon

values correspond to agent looking up, whereas positive

horizon

values correspond to the agent looking down.

required

Denotes whether the agent is in a standing or crouched position.

It is often useful to randomize the position of the agent in the scene, before starting an episode. Here, we can use:

1. [GetReachablePositions](https://ai2thor.allenai.org/ithor/documentation/environment-state/#sub-get-reachable-positions), which does an optimized BFS over a grid spaced out by the initialized
	gridSize
	. The valid positions are then added and returned in a list.
2. Teleport
	, which can take a given position, and transform the agent to that position.

The process is illustrated below:

```python
positions = controller.step(
    action="GetReachablePositions"
).metadata["actionReturn"]
```

```
[
    dict(x=(...), y=(...), z=(...)),
    dict(x=(...), y=(...), z=(...)),
    dict(x=(...), y=(...), z=(...)),
    {...}
    dict(x=(...), y=(...), z=(...)),
]
```

Step 2: Teleport to a Position

```python
import random
position = random.choice(positions)
controller.step(
    action="Teleport",
    position=position
)
```

### Get Reachable Positions Response

A list of each position that the agent can be at, without colliding into any other objects or going beyond the walls.

The

Done

action nothing to the state of the environment. But, it returns a cleaned up event with respect to the metadata.

```python
controller.step(action="Done")
```

It is often used in the definition of a successful navigation task (see [Anderson et al.](https://arxiv.org/pdf/1807.06757.pdf)), where the agent must call the done action to signal that it knows that it's done, rather than arbitrarily or biasedly guessing.

Warning

The

Done

action does literally nothing to the state of the environment. For instance, if the agent calls

Done

and then

MoveAhead

, the

Done

action will have no affect on preventing a

MoveAhead

action from executing.

It is often used to return a cleaned up version of the metadata.

Navigated to Movement