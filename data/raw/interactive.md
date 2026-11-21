---
title: "AI2-THOR"
source: "https://ai2thor.allenai.org/ithor/documentation/interactive-physics"
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

## [Pickup Object](https://ai2thor.allenai.org/ithor/documentation/interactive-physics/#sub-pickup-object)

PickupObject

allows the agent to pick up an interactable object specified by its objectId. Compatible objects have

pickupable

as

True

in their object metadata and return their current state with

isPickedUp

. Note that the agent’s hand must be clear of obstruction or the action will fail. If the target object being in the agent’s hand would cause it to clip into the environment, the action will also fail.

Picked up objects can also obstruct the Agent’s view of the environment since the Agent’s hand is always in camera view, so know that picking up larger objects will obstruct the field of vision.

Warning

Certain objects are

receptacles

that can themselves be picked up. If a moveable receptacle is picked up while other Sim Objects are inside of it, the contained objects will be picked up with the moveable receptacle. Here, a sequences like “

Place

the

Egg

on the

Plate

, then to

PickUp

the

Plate

” would

PickUp

the

Plate

with

Egg

on it.

```python
controller.step(
    action="PickupObject",
    objectId="Apple|1|1|1",
    forceAction=False,
    manualInteract=False
)
```

### Pickup Object Parameters

[

#### objectId

: string

](https://ai2thor.allenai.org/ithor/documentation/interactive-physics/#PickupObject-objectid)

required

The target object's

objectId

, found in the object's metadata.#### [forceAction](https://ai2thor.allenai.org/ithor/documentation/interactive-physics/#PickupObject-forceaction)

[: bool = False](https://ai2thor.allenai.org/ithor/documentation/interactive-physics/#PickupObject-forceaction)

Set to

True

to allow an object to be picked up regardless of if it is within the

visibilityDistance

of the agent.#### [manualInteract](https://ai2thor.allenai.org/ithor/documentation/interactive-physics/#PickupObject-manualinteract)

[: bool = False](https://ai2thor.allenai.org/ithor/documentation/interactive-physics/#PickupObject-manualinteract)

By default, objects picked up by the agent teleport into the agent’s hand at a default position in front of the agent camera. Set this to

True

in order to instead pick up an object at the object’s location. This allows the agent to manipulate the object via object manipulation actions without the abstraction of the picked up object teleporting to the agent’s hand.

## [Put Object](https://ai2thor.allenai.org/ithor/documentation/interactive-physics/#sub-put-object)

PutObject

attempts to put an object the agent is holding onto or into the target receptacle. Valid target receptacle objects have

receptacle

as

True

in their object metadata.

```python
controller.step(
    action="PutObject",
    objectId="Apple|1|1|1",
    forceAction=False,
    placeStationary=True
)
```

### Put Object Parameters

[

#### objectId

: string

](https://ai2thor.allenai.org/ithor/documentation/interactive-physics/#PutObject-objectid)

required

The target object's

objectId

, found in the object's metadata.#### [forceAction](https://ai2thor.allenai.org/ithor/documentation/interactive-physics/#PutObject-forceaction)

[: bool = False](https://ai2thor.allenai.org/ithor/documentation/interactive-physics/#PutObject-forceaction)

Enable to ignore any Receptacle Restrictions when attempting to place objects. Normally objects will fail to be put on a receptacle if that receptacle is not valid for the object. This will also ignore interaction range restrictions of the agent. Note this does not guarantee an object will be placed in a receptacle, as some objects will not fit inside a receptacle regardless of the default object restrictions.#### [placeStationary](https://ai2thor.allenai.org/ithor/documentation/interactive-physics/#PutObject-placestationary)

[: bool = True](https://ai2thor.allenai.org/ithor/documentation/interactive-physics/#PutObject-placestationary)

If

False

, a placed object will use the physics engine to resolve the final position. This means placing an object on an uneven surface may cause inconsistent results due to the object rolling around or even falling off of the target receptacle. Note that because of variances in physics resolution, this placement mode is non-deterministic! If

True

, the object will be placed in/on the valid receptacle without using physics to resolve the final position. This means that the object will be placed so that it will not roll around. For deterministic placement make sure to set to

True

!

## [Drop Object](https://ai2thor.allenai.org/ithor/documentation/interactive-physics/#sub-drop-object)

DropHandObject

attempts to drop an object currently in the agent’s hand and let physics resolve where it lands. The action is different from

PutObject

, as this does not guarantee the held object will be put into a specified receptacle. This is meant to be used in tandem with the Move/Rotate Hand functions to maneuver a held object to a target area, and the let it drop.

Additionally, this drop action will fail if the held object is not clear from all collisions. Most importantly, the agent’s collision will prevent drop, as dropping an object if it is “inside” the agent will lead to unintended behavior.

```python
controller.step(
    action="DropHandObject",
    forceAction=False
)
```

### Drop Object Parameters#### [forceAction](https://ai2thor.allenai.org/ithor/documentation/interactive-physics/#DropObject-forceaction)

[: bool = False](https://ai2thor.allenai.org/ithor/documentation/interactive-physics/#DropObject-forceaction)

Set to

True

to forcibly drop an object even if this would cause clipping with the environment, other objects, or the agent.

## [Throw Object](https://ai2thor.allenai.org/ithor/documentation/interactive-physics/#sub-throw-object)

ThrowObject

is an extension of

DropHandObject

. It throws the object currently in the agent’s hand in the forward facing direction of the agent with a force of

moveMagnitude

newtons. Since objects have different mass properties, objects require different forces to throw them same distance.

```python
controller.step(
    action="ThrowObject",
    moveMagnitude=150.0,
    forceAction=False
)
```

### Throw Object Parameters

[

#### moveMagnitude

: float

](https://ai2thor.allenai.org/ithor/documentation/interactive-physics/#ThrowObject-movemagnitude)

required

The amount of force used to throw the object in newtons. Note that objects of different masses will have different throw distances if this magnitude is not changed.#### [forceAction](https://ai2thor.allenai.org/ithor/documentation/interactive-physics/#ThrowObject-forceaction)

[: bool = False](https://ai2thor.allenai.org/ithor/documentation/interactive-physics/#ThrowObject-forceaction)

Set to

True

to forcibly throw an object even if this would cause clipping with the environment or other objects.

## [Move Held Object](https://ai2thor.allenai.org/ithor/documentation/interactive-physics/#sub-move-held-object)

While the agent is holding an object, it has several available actions to manipulate it. One such action is the ability to move the held object closer or further away from it. Held object movement is useful if we want to drop an object on a surface that is relatively far away.

There are several directions that the agent can move the held object. They include:

MoveHeldObjectAhead

,

MoveHeldObjectBack

,

MoveHeldObjectLeft

,

MoveHeldObjectRight

,

MoveHeldObjectUp

, and

MoveHeldObjectDown

. Each direction supports the same additional parameters.

Warning

After calling a move action (e.g.,

MoveAhead

) or a rotate action (e.g.,

RotateRight

) the position of the held object will reset to its default position in-front of the agent.

```python
controller.step(
    action="MoveHeldObjectAhead",
    moveMagnitude=0.1,
    forceVisible=False
)

# Other supported directions
controller.step("MoveHeldObjectBack")
controller.step("MoveHeldObjectLeft")
controller.step("MoveHeldObjectRight")
controller.step("MoveHeldObjectUp")
controller.step("MoveHeldObjectDown")
```

### Move Held Object Parameters

[

#### moveMagnitude

: float

](https://ai2thor.allenai.org/ithor/documentation/interactive-physics/#MoveHeldObject-movemagnitude)

required

The distance, in meters, to move the held object in the specified direction.#### [forceVisible](https://ai2thor.allenai.org/ithor/documentation/interactive-physics/#MoveHeldObject-forcevisible)

[: bool = False](https://ai2thor.allenai.org/ithor/documentation/interactive-physics/#MoveHeldObject-forcevisible)

Setting

forceVisible=True

results in action failing if the object is not visible to the agent. This prevents the agent from hiding the held object inside or behind another object, or moving it too far, such that it's out of the agent's field of view.

We also provide a separate helper action,

MoveHeldObject

, which allows the held object to move in several directions with only a single action:

```python
controller.step(
    action="MoveHeldObject",
    ahead=0.1,
    right=0.05,
    up=0.12,
    forceVisible=False
)
```

<iframe src="https://player.vimeo.com/video/577376697?autoplay=1&amp;loop=1&amp;muted=1&amp;autopause=0" frameborder="0" allow="autoplay; fullscreen; picture-in-picture" allowfullscreen=""></iframe>

### Move Held Object Parameters

[

#### ahead

: float

](https://ai2thor.allenai.org/ithor/documentation/interactive-physics/#MoveHeldObject2-ahead)

required

The distance, in meters, to move the held object forward, from the agent's current facing direction.

[

#### right

: float

](https://ai2thor.allenai.org/ithor/documentation/interactive-physics/#MoveHeldObject2-right)

required

The distance, in meters, to move the held object rightwards, from the agent's current facing direction.

[

#### up

: float

](https://ai2thor.allenai.org/ithor/documentation/interactive-physics/#MoveHeldObject2-up)

required

The distance, in meters, to move the held object upwards, from the agent's current facing direction.#### [forceVisible](https://ai2thor.allenai.org/ithor/documentation/interactive-physics/#MoveHeldObject2-forcevisible)

[: bool = False](https://ai2thor.allenai.org/ithor/documentation/interactive-physics/#MoveHeldObject2-forcevisible)

Setting

forceVisible=True

results in action failing if the object is not visible to the agent. This prevents the agent from hiding the held object inside or behind another object, or moving it too far, such that it's out of the agent's field of view.

## [Rotate Held Object](https://ai2thor.allenai.org/ithor/documentation/interactive-physics/#sub-rotate-held-object)

RotateHeldObject

attempts to rotate the held object relative to its current rotation.

Warning

After calling a move action (e.g.,

MoveAhead

) or a rotate action (e.g.,

RotateRight

) the rotation of the held object will reset to its default rotation.

```python
controller.step(
    action="RotateHeldObject",
    pitch=90,
    yaw=25,
    roll=45
)
```

### Rotate Held Object Parameters

[

#### pitch

: float = 0

](https://ai2thor.allenai.org/ithor/documentation/interactive-physics/#RotateHeldObject-pitch)

required

Increments the pitch of an object from the agent's current facing direction. Specified in degrees. The video below shows the held object's

pitch

incrementing in $15$ degree increments.

<iframe src="https://player.vimeo.com/video/577392020?autoplay=1&amp;loop=1&amp;muted=1&amp;autopause=0" frameborder="0" allow="autoplay; fullscreen; picture-in-picture" allowfullscreen=""></iframe>

[

#### yaw

: float = 0

](https://ai2thor.allenai.org/ithor/documentation/interactive-physics/#RotateHeldObject-yaw)

required

Increments the yaw of an object from the agent's current facing direction. Specified in degrees. The video below shows the held object's

yaw

incrementing in $15$ degree increments.

<iframe src="https://player.vimeo.com/video/577392033?autoplay=1&amp;loop=1&amp;muted=1&amp;autopause=0" frameborder="0" allow="autoplay; fullscreen; picture-in-picture" allowfullscreen=""></iframe>

[

#### roll

: float = 0

](https://ai2thor.allenai.org/ithor/documentation/interactive-physics/#RotateHeldObject-roll)

required

Increments the roll of an object from the agent's current facing direction. Specified in degrees. The video below shows the held object's

roll

incrementing in $15$ degree increments.

<iframe src="https://player.vimeo.com/video/577392050?autoplay=1&amp;loop=1&amp;muted=1&amp;autopause=0" frameborder="0" allow="autoplay; fullscreen; picture-in-picture" allowfullscreen=""></iframe>

An overload of

RotateHeldObject

can be used to rotate the held object to a fixed rotation.

```python
controller.step(
    action="RotateHeldObject",
    rotation=dict(x=90, y=15, z=25)
)
```

### Rotate Held Object Parameters

[

#### rotation

: dict\[str, float\]

](https://ai2thor.allenai.org/ithor/documentation/interactive-physics/#RotateHeldObject2-rotation)

required

Sets the rotation of the object to the provided rotation, in degrees. The rotation is relative to the object's axes. So, the set rotation is independent of the object's current rotation. Rotations are specified in degrees.

## [Pushing Objects](https://ai2thor.allenai.org/ithor/documentation/interactive-physics/#pushing-objects)

## [Directional Push](https://ai2thor.allenai.org/ithor/documentation/interactive-physics/#sub-directional-push)

DirectionalPush

attempts to push an object in a given direction. Since objects can have different mass properties, pushing different objects often requires differing amounts of force to move them the same distance. Only

pickupable

and

moveable

objects can be pushed.

```python
controller.step
    action="DirectionalPush",
    objectId="Sofa|3|2|1",
    moveMagnitude="100",
    pushAngle="90"
)
```

### Directional Push Parameters

[

#### moveMagnitude

: float

](https://ai2thor.allenai.org/ithor/documentation/interactive-physics/#directional-push-movemagnitude)

required

The amount of force used to pull the object in newtons. Following natural physics, objects of different masses may move different distances with the same amount of force.

[

#### pushAngle

: float

](https://ai2thor.allenai.org/ithor/documentation/interactive-physics/#directional-push-pushangle)

required

The direction vector to push the object. Values in $[0:360]$ are valid, with $0$ being the current forward direction of the agent. This value will change the push direction clockwise from the agent’s forward. (i.e., $90$ will push the object directly right, a value of $180$ will push the object backwards).

required

The target object's

objectId

, found in the object's metadata.

Set to

True

to allow an object to be picked up regardless of if it is within the

visibilityDistance

of the agent.

PushObject

is syntactic sugar for

DirectionalPush

with a

pushAngle

of $0$.

```python
controller.step(
    action="PushObject",
    objectId="Mug|0.25|-0.27",
    forceAction=False
)
```

### Push Object Parameters

required

The amount of force used to push the object in newtons. Note that objects of different masses will move different distances if this magnitude is not changed.

required

The target object's

objectId

, found in the object's metadata.

Set to

True

to allow an object to be picked up regardless of if it is within the

visibilityDistance

of the agent.

PullObject

is syntactic sugar for

DirectionalPush

with a

pushAngle

of $180$.

```python
controller.step(
    action="PullObject",
    objectId="Mug|0.25|-0.27",
    forceAction=False
)
```

### Push Object Parameters

required

The amount of force used to pull the object in newtons. Note that objects of different masses will move different distances if this magnitude is not changed.

required

The target object's

objectId

, found in the object's metadata.

Set to

True

to allow an object to be picked up regardless of if it is within the

visibilityDistance

of the agent.

TouchThenApplyForce

allows the agent to push an object at a certain point on the object, in a given direction. If a

pickupable

or

moveable

sim object is hit along the path of this ray, it will have a force determined by

moveMagnitude

applied to it instantaneously. This action will return feedback in the

actionReturn

attribute of the event metadata return.

```python
event = controller.step(
    action="TouchThenApplyForce",
    x=0.5,
    y=0.5,
    direction={
        "x": 0.0,
        "y": 1.0,
        "z": 0.0
    },
    moveMagnitude=80,
    handDistance=1.5
)
```

### Parameters

required

Used instead of

objectId

as an alternate way to target an object based on the last image frame. Valid values are in $[0:1]$, corresponding to how far left the image is from the previous frame.

required

Used in tandem with

x

to target an object based on the last image frame, rather than an

objectId

. Valid values are in $[0:1]$, corresponding to how from the top the object is from the previous frame.

required

The direction vector relative to the agent’s current forward to push any object touched.

required

The amount of force to apply to a touched object in newtons.

required

The maximum Euclidean distance from the agent's camera that the (x, y) point that targets the object can be, in meters. If the point on the object is further away than

handDistance

, the action will fail.

```
{
    "didHandTouchSomething": True
    "objectId": "Apple|+1|+1|+1"
    "armsLength": 1.20
}
```

### event.metadata\["actionReturn"\]

Returns

True

if a sim object was touched within the ray’s length of

handDistance

meters.

The unique string id of the object touched by the ray. If the object touched in the scene has collision but is not a sim object, this

objectId

attribute will be "not a sim object, a structure was touched".

The distance from the touched point on the object to the agent’s camera. This distance will never exceed the handDistance value passed in originally unless the action finishes as a failed action (see below).

This action will return a failure (event.metadata\["lastActionSuccess"\] == False) only in two cases:

1. The raycast hit an object, but the object was outside of the maximum visibility range of the agent (ie: a handDistance of 10 is passed in, and hits an object 9 meters away, but the agent’s max visibility distance is 1.5 meters, causing a failure). The feedback object generated in this case will be didHandTouchSomething=False, objectId="", armsLength=handDistance.
2. The handDistance of the action is larger than the agent’s max visibility distance and no object was hit. The feedback object generated in this case will be didHandTouchSomething=False, objectId="", armsLength=handDistance with a metadata errormessage of “the position the hand would have moved to is outside the agent’s max interaction range”.

Note that this action interacts with the visibility of an object in order to determine what can be poked. The visibility of an object is defined by:

1. An object must be within the agent camera’s field of view.
2. An object must be within the area of a cylinder defined by a radius of length visibilityDistance around the agent’s vertical y axis.
3. If that object is within the cylinder, a line must be able to be cast from the agent’s camera position to a point on that object unobstructed.

Because visibility is defined by the cylinder with radius visibilityDistance, the total area of objects that are touchable by this action is the intersection of the sphere of radius handDistance centered around the agent’s camera, and the cylinder of radius visibilityDistance about the agent’s vertical axis. Note that the agent camera is also centered around the agent’s vertical axis.

PlaceObjectAtPoint

attempts to place an object flush with the surface of a receptacle. This can only be used on objects that are

pickupable

or

moveable

. The point to place an object at can be generated by the

GetSpawnCoordinatesAboveReceptacle

action below. Combine these two actions in order to teleport objects onto different receptacle surfaces.

```python
controller.step(
    action="PlaceObjectAtPoint",
    objectId="Toaster|1|1|1",
    position={
        "x": -1.25,
        "y": 1.0,
        "z": -1.0
    }
)
```

### Place Object At Point Parameters

required

The target object's

objectId

, found in the object's metadata.

required

Global $(x, y, z)$ coordinates for the point to try and place the object.

GetSpawnCoordinatesAboveReceptacle

is to explicitly be used in tandem with the

PlaceObjectAtPoint

action. It returns an array of xyz dictionary representing the $(x, y, z)$ coordinates of valid spawn positions above a

receptacle

object. The array of xyz dictionary is returned in the actionReturn metadata.

```python
controller.step(
    action="GetSpawnCoordinatesAboveReceptacle",
    objectId="CounterTop|1|1|1",
    anywhere=False
)
```

### Parameters

required

The target object's

objectId

, found in the object's metadata.

If

True

, spawn coordinates will be returned even if the exact position of the coordinate is outside of the agent’s field of view. Keep False to return spawn coordinates even if they are not in view of the agent.

Navigated to Held Objects