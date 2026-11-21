---
title: "AI2-THOR"
source: "https://ai2thor.allenai.org/ithor/documentation/object-state-changes"
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

OpenObject

attempts to open an Openable object to a specified amount, parameterized by

openness

. The full list of openable object types can be filtered on the [Object Types](https://ai2thor.allenai.org/ithor/documentation/objects/object-types) page.

Warning

An object can fail to open if it hits another object as it is opening. In this case the action will fail and the target object will reset to the position it was last in.

```python
event = controller.step(
    action="OpenObject",
    objectId="Book|0.25|-0.27|0.95",
    openness=1,
    forceAction=False
)
```

### Open Object Parameters

[

#### objectId

: string

](https://ai2thor.allenai.org/ithor/documentation/object-state-changes/#OpenObject-objectid)

required

The target object's

objectId

, found in the object's metadata.#### [openness](https://ai2thor.allenai.org/ithor/documentation/object-state-changes/#OpenObject-openness)

[: float = 1](https://ai2thor.allenai.org/ithor/documentation/object-state-changes/#OpenObject-openness)

The proportion regarding how far the object should open. Valid values are in $[0:1]$, where the value $0$ corresponds to completely closed, $1$ corresponds to completely open, and $0.5$ corresponds to halfway open, for instance.#### [forceAction](https://ai2thor.allenai.org/ithor/documentation/object-state-changes/#OpenObject-forceaction)

[: bool = False](https://ai2thor.allenai.org/ithor/documentation/object-state-changes/#OpenObject-forceaction)

If

False

, the agent will not be able to interact with the object unless it is within the initialized

visibilityDistance

of the object and the object appears in the agent's current frame. This prevents the agent from unnaturally interacting with objects that are too far away.

Each object contains metadata in the event pertaining to the state of its openness.

```python
event.metadata["objects"][i]
```

```
{
    "openable": True,
    "openness": 0.75,
    "isOpen": True,

    {...}
}
```

### Open Object Response#### [openable](https://ai2thor.allenai.org/ithor/documentation/object-state-changes/#OpenObjectResponse-openable)

[: bool](https://ai2thor.allenai.org/ithor/documentation/object-state-changes/#OpenObjectResponse-openable)

Can this object be opened?#### [openness](https://ai2thor.allenai.org/ithor/documentation/object-state-changes/#OpenObjectResponse-openness)

[: float](https://ai2thor.allenai.org/ithor/documentation/object-state-changes/#OpenObjectResponse-openness)

The proportion that the object is open, linearly scaled to the range $[0:1]$. For instance, if an object is a quarter of the way open, then its openness would be $0.25$.#### [isOpen](https://ai2thor.allenai.org/ithor/documentation/object-state-changes/#OpenObjectResponse-isopen)

[: bool](https://ai2thor.allenai.org/ithor/documentation/object-state-changes/#OpenObjectResponse-isopen)

False

when the object's openness is $0$,

True

otherwise.

## [Close Object](https://ai2thor.allenai.org/ithor/documentation/object-state-changes/#close-object)

CloseObject

is syntactic sugar for

OpenObject

with an

openness

of 0.

Warning

An object can fail to close if it hits another object as it is opening. In this case the action will fail and the target object will reset to the position it was last in.

```python
controller.step(
    action="CloseObject",
    objectId="Book|0.25|-0.27|0.95",
    forceAction=False
)
```

### Close Object Parameters

required

The target object's

objectId

, found in the object's metadata.

If

False

, the agent will not be able to interact with the object unless it is within the initialized

visibilityDistance

of the object and the object appears in the agent's current frame. This prevents the agent from unnaturally interacting with objects that are too far away.

BreakObject

attempts to break a breakable object. If successful, the object appears visibly different. For instance, breakable objects may shatter completely into pieces or have their screens cracked. The full list of breakable object types can be filtered on the [Object Types](https://ai2thor.allenai.org/ithor/documentation/objects/object-types) page. Broken objects cannot be unbroken (until the scene has reset).

```python
event = controller.step(
    action="BreakObject",
    objectId="Vase|0.25|0.27|-0.95",
    forceAction=False
)
```

### Break Object Parameters

required

The target object's

objectId

, found in the object's metadata.

If

False

, the agent will not be able to interact with the object unless it is within the initialized

visibilityDistance

of the object and the object appears in the agent's current frame. This prevents the agent from unnaturally interacting with objects that are too far away.

Each object contains metadata in the event pertaining to if it is broken.

```python
event.metadata["objects"][i]
```

```
{
    "breakable": True,
    "isBroken": False,

    {...}
}
```

### Break Object Response

Can this object break?

Is this object currently broken?

CookObject

attempts to switch an object to its cooked state. Objects cannot not be uncooked (unless the scene is reset). The full list of cookable object types can be filtered on the [Object Types](https://ai2thor.allenai.org/ithor/documentation/objects/object-types) page.

```python
event = controller.step(
    action="CookObject",
    objectId="Egg|0.25|-0.27|0.95",
    forceAction=False
)
```

### Cook Object Parameters

required

The target object's

objectId

, found in the object's metadata.

If

False

, the agent will not be able to interact with the object unless it is within the initialized

visibilityDistance

of the object and the object appears in the agent's current frame. This prevents the agent from unnaturally interacting with objects that are too far away.

Each object contains metadata in the event pertaining to if it is cooked.

```python
event.metadata["objects"][i]
```

```
{
    "cookable": True,
    "isCooked": False,

    {...}
}
```

### Cook Object Response

Can this object be cooked?

Is this object currently cooked?

SliceObject

attempts to slice an object.

If an object, such as an Apple, is successfully sliced, there may include several new AppleSliced objects in the scene and metadata, one for each slice. Other objects, like Egg, may only break after being sliced. Sliced objects cannot be unsliced (unless the scene is reset).

The full list of sliceable objects can be filtered on the [Object Types](https://ai2thor.allenai.org/ithor/documentation/objects/object-types) page.

```python
event = controller.step(
    action="SliceObject",
    objectId="Potato|0.25|-0.27|0.95",
    forceAction=False
)
```

### Slice Object Parameters

required

The target object's

objectId

, found in the object's metadata.

If

False

, the agent will not be able to interact with the object unless it is within the initialized

visibilityDistance

of the object and the object appears in the agent's current frame. This prevents the agent from unnaturally interacting with objects that are too far away.

Each object contains metadata in the event pertaining to if it is sliced.

```python
event.metadata["objects"][i]
```

```
{
    "sliceable": True,
    "isSliced": False,

    {...}
}
```

### Slice Object Response

Can this object be sliced?#### [isSliced](https://ai2thor.allenai.org/ithor/documentation/object-state-changes/#SliceObjectResponse-issliced)

[: bool](https://ai2thor.allenai.org/ithor/documentation/object-state-changes/#SliceObjectResponse-issliced)

Is this object currently sliced?

## [Toggle Object](https://ai2thor.allenai.org/ithor/documentation/object-state-changes/#toggle-object)

ToggleObjectOn

and

ToggleObjectOff

toggles an object between on and off states, respectively. Examples include Lamps, Light Switches, Stove Knobs, and Laptops. The full list of toggleable objects can be filtered on the [Object Types](https://ai2thor.allenai.org/ithor/documentation/objects/object-types) page.

```python
event = controller.step(
    action="ToggleObjectOn",
    objectId="LightSwitch|0.25|-0.27|0.95",
    forceAction=False
)
```

```python
event = controller.step(
    action="ToggleObjectOff",
    objectId="LightSwitch|0.25|-0.27|0.95",
    forceAction=False
)
```

### Toggle Object Parameters

[

#### objectId

: string

](https://ai2thor.allenai.org/ithor/documentation/object-state-changes/#ToggleOn-objectid)

required

The target object's

objectId

, found in the object's metadata.#### [forceAction](https://ai2thor.allenai.org/ithor/documentation/object-state-changes/#ToggleOn-forceaction)

[: bool = False](https://ai2thor.allenai.org/ithor/documentation/object-state-changes/#ToggleOn-forceaction)

If

False

, the agent will not be able to interact with the object unless it is within the initialized

visibilityDistance

of the object and the object appears in the agent's current frame. This prevents the agent from unnaturally interacting with objects that are too far away.

Each object contains metadata in the event pertaining to if it is toggled.

```python
event.metadata["objects"][i]
```

```
{
    "toggleable": True,
    "isToggled": True,

    {...}
}
```

### Toggle Object Response#### [toggleable](https://ai2thor.allenai.org/ithor/documentation/object-state-changes/#ToggleObjectResponse-toggleable)

[: bool](https://ai2thor.allenai.org/ithor/documentation/object-state-changes/#ToggleObjectResponse-toggleable)

Can this object be toggled?

Is this object currently toggled on?

DirtyObject

attempts to make an object look dirty.

CleanObject

can then be used to make the object look clean again. The full list of dirtyable object types can be filtered on the [Object Types](https://ai2thor.allenai.org/ithor/documentation/objects/object-types) page.

```python
event = controller.step(
    action="DirtyObject",
    objectId="Mug|0.25|-0.27|0.95",
    forceAction=False
)
```

```python
event = controller.step(
    action="CleanObject",
    objectId="Mug|0.25|-0.27|0.95",
    forceAction=False
)
```

### Dirty Object Parameters

required

The target object's

objectId

, found in the object's metadata.

If

False

, the agent will not be able to interact with the object unless it is within the initialized

visibilityDistance

of the object and the object appears in the agent's current frame. This prevents the agent from unnaturally interacting with objects that are too far away.

Each object contains metadata in the event pertaining to if it is toggled.

```python
event.metadata["objects"][i]
```

```
{
    "toggleable": True,
    "isToggled": True,

    {...}
}
```

### Dirty Object Response

Can this object be toggled?

Is this object currently toggled on?

FillObjectWithLiquid

attempts to fill an object with

fillLiquid

. Only compatible objects that are empty can be filled. The full list of object types that can be filled with liquid can be filtered on the [Object Types](https://ai2thor.allenai.org/ithor/documentation/objects/object-types) page.

```python
event = controller.step(
    action="FillObjectWithLiquid",
    objectId="Mug|0.25|-0.27|0.95",
    fillLiquid="coffee",
    forceAction=False
)
```

### Fill Object with Liquid Parameters

required

The target object's

objectId

, found in the object's metadata.

required

The type of liquid that fills the object. Valid liquids are

"coffee"

,

"wine"

, and

"water"

.

If

False

, the agent will not be able to interact with the object unless it is within the initialized

visibilityDistance

of the object and the object appears in the agent's current frame. This prevents the agent from unnaturally interacting with objects that are too far away.

Each object contains metadata in the event pertaining to if it is filled with liquid.

```python
event.metadata["objects"][i]
```

```
{
    "fillLiquid": "coffee",
    "canFillWithLiquid": True,
    "isFilledWithLiquid": True,

    {...}
}
```

### Fill Object with Liquid Response

Which liquid is the object filled with? If the object is not filled with liquid, it will report

None

. Valid liquids are

"coffee"

,

"wine"

, and

"water"

.

Can this object be filled with liquid?

Is this object currently filled with liquid?

EmptyLiquidFromObject

attempts to empty the liquid from an object if it is currently filled with liquid (i.e.,

isFilledWithLiquid

is True).

Remark

If an object is rotated downward far enough, gravity may cause the object to lose its liquid automatically, causing

isFilledWithLiquid

to be

False

. Here, the liquid will not appear spilled on the ground like a puddle. Instead, it disappears.

```python
event = controller.step(
    action="EmptyLiquidFromObject",
    objectId="Mug|0.25|-0.27|0.95",
    forceAction=False
)
```

### Empty Liquid From Object Parameters

required

The target object's

objectId

, found in the object's metadata.

If

False

, the agent will not be able to interact with the object unless it is within the initialized

visibilityDistance

of the object and the object appears in the agent's current frame. This prevents the agent from unnaturally interacting with objects that are too far away.

Each object contains metadata in the event pertaining to if it can be emptied of liquid.

```python
event.metadata["objects"][i]
```

```
{
    "fillLiquid": None,
    "canFillWithLiquid": True,
    "isFilledWithLiquid": False,

    {...}
}
```

### Empty Liquid from Object Response

Which liquid is the object filled with? If the object is not filled with liquid, it will report

None

. Valid liquids are

"coffee"

,

"wine"

, and

"water"

.

Can this object be emptied with liquid?

Is this object currently filled with liquid?

UseUpObject

attempts to use up parts of an object. The action works with objects like ToiletPaper, TissueBox, and PaperTowelRoll, which each has an full/empty state. The full list of object types that can be used up can be filtered on the [Object Types](https://ai2thor.allenai.org/ithor/documentation/objects/object-types) page.

```python
event = controller.step(
    action="UseUpObject",
    objectId="ToiletPaper|0.25|-0.27|0.95",
    forceAction=False
)
```

### Use Up Object Parameters

[

#### objectId

: string

](https://ai2thor.allenai.org/ithor/documentation/object-state-changes/#UseUpObject-objectid)

required

The target object's

objectId

, found in the object's metadata.#### [forceAction](https://ai2thor.allenai.org/ithor/documentation/object-state-changes/#UseUpObject-forceaction)

[: bool = False](https://ai2thor.allenai.org/ithor/documentation/object-state-changes/#UseUpObject-forceaction)

If

False

, the agent will not be able to interact with the object unless it is within the initialized

visibilityDistance

of the object and the object appears in the agent's current frame. This prevents the agent from unnaturally interacting with objects that are too far away.

Each object contains metadata in the event pertaining to if it is used up.

```python
event.metadata["objects"][i]
```

```
{
    "canBeUsedUp": True,
    "isUsedUp": False,

    {...}
}
```

### Use Up Object Response

Can this object be used up?

Is this object currently used up?

Navigated to Open Object