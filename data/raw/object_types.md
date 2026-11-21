---
title: "AI2-THOR"
source: "https://ai2thor.allenai.org/ithor/documentation/objects/object-types"
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

Each SimObject is assigned to an object type, which is accessible from the object’s metadata:

```python
from ai2thor.controller import Controller
controller = Controller(scene='FloorPlan1')

for obj in controller.last_event.metadata["objects"]:
    print(obj["objectType"])
```

## [iTHOR Object Types](https://ai2thor.allenai.org/ithor/documentation/objects/object-types/#ithor-object-types)

The table below provides information about the behavior of every object type that appears in iTHOR. Definitions can be found at the bottom of the page.

Object Types that have a (\*) next to them are only referenced after an interaction. For instance,

Apple

becomes

AppleSliced

once the

Slice

action has been applied to the

Apple

.

## [Definitions](https://ai2thor.allenai.org/ithor/documentation/objects/object-types/#definitions)

## [Actionable Properties](https://ai2thor.allenai.org/ithor/documentation/objects/object-types/#sub-actionable-properties)

Objects in this framework can have a number of Actionable Properties associated with the object type. Actionable Properties are specific properties that have an Action associated with them. For example, an object that is Openable means that the OpenObject and CloseObject actions can be used to interact with that object. Below is a list of all Actionable Properties and their detailed descriptions.

### Openable

These objects can be opened or closed using the OpenObject and CloseObject actions. Receptacles that are Openable allow for objects to be placed inside them.

All Openable objects will return openable=True in their object metadata to indicate that they have this property. The object metadata also indicates an Openable object’s current open/closed state. If isOpen=True, the object is open. If isOpen=False, the object is closed.

### Pickupable

These objects are able to be picked up or put down into Receptacles objects by the Agent using the PickupObject and PutObject actions. Picked up objects can also be dropped using DropHandObject which will remove the object from the Agent’s hand without needing a target receptacle. Throw is an extension of dropping an object, where an additional force is added to throw object about the scene. Pickupable objects can also be shoved around using the Push and Pull actions. Some Receptacle objects are also pickupable. Any objects placed inside a pickupable receptacle are moved all at once, so complex sequences like (Put Apple on Plate, then Move Plate with Apple to Sink) are possible.

All Pickupable objects will return pickupable=True in their object metadata to indicate that they have this property. The object metadata also indicates a Pickupable object’s current state of whether it is currently picked up by the agent or not. If isPickedUp=True the agent is actively holding the object. If isPickedUp=False then the object is not being picked up by the agent.

### Moveable

These are non-static objects that can be moved around the scene by using actions like Push and Pull. They can also be repositioned due to forces from other objects, such as using Throw to toss a Pickupable object at a Moveable object. The key difference between Moveable and Pickupable objects are that Moveable objects are too large to be held in the agent’s hand as Pickupable objects are, so actions like PickupObject will not work on Moveable objects.

All Moveable objects will return moveable=True in their object metadata to indicate that they have this property. The object metadata also indicates if an object is currently in motion. If isMoving=True then the object is actively moving. If isMoving = False the object is not moving. Note that both Moveable and Pickupable objects can be moving, so the isMoving metadata value is not restricted to only Moveable objects.

### Toggleable

Interact with these objects using the ToggleObjectOn and ToggleObjectOff actions. All Toggleable objects have a visible state change that occurs when toggled on or off (i.e., laptop screen will be on with an image or blank when off, a lamp will be lit when on and dim when off).

All Toggleable objects will return toggleable=True in their object metadata to indicate that they have this property. The object metadata also indicates if a Toggleable object is currently toggled On or Off. If isToggled=True, the object is turned on. If isToggled=False, the object is turned off.

### Receptacle

Receptacle objects allow other objects to be placed on or in them if the other object can physically fit the receptacle. Some receptacles are restricted to specific object types (i.e. ToiletPaper is the only type that can go on a ToiletPaperHanger). Note that any receptacles that are also Pickupable can be moved about the scene with any sim objects they actively contain (ie: Pick up a Plate with an Apple on it to move both the Plate and Apple around the scene simultaneously).

All Receptacle objects will return receptacle=True in their object metadata to indicate they have this property. The object metadata also indicates if a Receptacle object contains any other objects via the receptacleObjectIds metadata string list, which lists all objectIds of any sim objects contained by the Receptacle. Additionally, objects report back any receptacles that they are contained by via the parentReceptacles list of strings in the object metadata.

### Fillable

These objects can be filled with various liquids using the FillObjectWithLiquid action. Fillable objects can be filled with Water, Coffee, or Wine. If an object is filled with one of the liquid types and is rotated greater than 90 degrees from the global upward axis, the object will automatically empty itself because the liquid has “spilled.” Additionally, some fill interactions are context sensitive. For example, placing an empty mug in a coffee maker object that is turned on will automatically fill the mug with coffee. Similarly, moving an empty mug under a running faucet will automatically fill the mug with water.

All Fillable objects will return canFillWithLiquid=True in their object metadata to indicate they have this property. The object metadata also indicates if an object is actively filled with a liquid. If isFilledWithLiquid=True the object is filled by some liquid. If isFilledWithLiquid=False, the object is empty.

### Sliceable

These objects can be sliced into smaller pieces using the SliceObject action. This destroys the source object and spawns in multiple “sliced” pieces of the source object in the exact same location. This is a one-way state change, so only a scene reset will revert sliced objects to their whole versions. Sliced objects will still report metadata information even after being destroyed. This allows you to check the last position the source object was before the Slice action finished.

All Sliceable objects will return sliceable=True in their object metadata to indicate if they have this property. The object metadata also indicates if a Sliceable object has been sliced or not. If isSliced=True the object has been sliced and is no longer interactable (although the pieces it spawns are interactable). If isSliced=False the object has not been sliced and is whole.

### Cookable

These objects have a cooked state that can be switched to with the CookObject action. This is a one-way state change, so only a scene reset will revert cooked objects back to their uncooked state. Cookable objects can interact with objects that are heat sources (canChangeTempToHot=True) to automatically change the object to a cooked state. This means interactions like turning on a Microwave with a Potato in it will turn the Potato to the cooked state without using the CookObject action.

All Cookable objects will return cookable=True in their object metadata to indicate that they have this property. The object metadata also indicates if a Cookable object is currently cooked. If isCooked=True, the object is cooked. If isCooked=False, the object is not cooked.

### Breakable

These objects have a broken state that can be switched to with the BreakObject action. This is a one-way state change, so only a scene reset will revert broken objects to their unbroken state. Breakable objects also break automatically if they collide with a high enough force. This force threshold is different between objects because some objects are more fragile than others. This automatic breaking can be toggled off via the MakeObjectsOfTypeUnbreakable action. When some objects break, they will shatter into pieces that will not be interacatble, as the fractured remains of the object are not themselves sim objects. Objects that can shatter like certain Cup or Vase objects made of glass or ceramic will shatter in this way when broken. Other objects may remain interactable in a limited way after they break. A Laptop, for example, when broken will have its screen become cracked. You will still be able to open, close, and pickup the Laptop if it is broken, but you will no longer be able to toggle it on.

All Breakable objects will return breakable=True in their object metadata to indicate that they have this property. The object metadata also indicates if a Breakable object is currently broken. If isBroken=True, the object has broken. If isBroken=False, the object is whole and not broken.

### Dirtyable

These objects have a clean and Dirtyable state that can be toggled between using the DirtyObject action. This includes objects like Mugs that can have grime on them, or a Bed that has the covers messy or made. Certain Dirtyable objects can contextually be switched to their clean state if they are moved under running water. (a grimy Bowl moved under a Faucet that is toggled on will clean the bowl automatically).

All Dirtyable objects will return dirtyable=True in their object metadata to indicate that they have this property. The object metadata also indicates if a Dirtyable object is currently in the dirty or clean state. If isDirty=True, the object is in its dirty state. if isDirty=False, the object is in its clean state.

### UsedUp

These objects can have parts of themselves used up with the UseUpObject action. This is a one-way interaction and can not be reversed unless the scene is reset. This can change the overall look of the object to show that its contents have been “Used Up.” ToiletPaper, TissueBox, and PaperTowelRoll objects are examples of objects that, when used upp, change form in some way.

All UsedUp objects will return canBeUsedUp=True in their object metadata to indicate that they have this property. The object metadata also indicates if a UsedUp object is currently used up or full. If isUsedUp=True, the object has been used up. If isUsedUp=False, the object is full.

## [Material Properties](https://ai2thor.allenai.org/ithor/documentation/objects/object-types/#sub-material-properties)

Material Properties are properties of objects that don’t have an Action directly associated with them. These properties cannot be directly manipulated- they only update based on contextual interactions with other sim objects or the environment.

### Temperature

All objects have an abstracted Temperature value that can be either Hot, Cold, or Room Temperature.

### ChangeTemp

These objects can change the Temperature value (Hot, Cold, Room Temp) of other sim objects depending on if the ChangeTemp object is a Heat or Cold source. For example, objects placed on a turned on Stove Burner will have their temperature changed to Hot automatically. Similarly, objects placed in a Refrigerator object will have their temperature changed to Cold automatically. Objects removed from either a Hot or Cold source will return to Room Temperature over time.

### Mass

All Pickupable objects have a mass value in Kilograms. Using actions like Throw will realistically cause behavior that is reliant on different mass (i.e., Throwing a 0.1kg object with 100 newtons of force will fly farther than Throwing a 200kg object with 100 newtons of force). Note the mass of objects that spawn from other objects is persistent (i.e., A source Potato that has a mass of 0.5 kg, when Sliced would result in slices that add up to 0.5 kg total). Note that static objects like counter-tops or cabinets that are built into the “structure” of a scene do not have a Mass value that can be manipulated.

### SalientMaterials

All Pickupable objects have a set of Salient Materials which describe what the object is made up of. Salient materials include: Metal, Wood, Plastic, Glass, Ceramic, Stone, Fabric, Rubber, Food, Paper, Wax, Soap, Sponge, Organic. Check any object’s Metadata to see what Salient Materials it has, as objects in the same object type category can vary in composition (i.e., Bowls can be Plastic, Glass, or Ceramic).

### Inherited

Some sim objects are created from a source sim object after certain actions. For example, PotatoSliced objects are generated after a Potato object has had the Slice action used on it. Inherited objects inerit the objectId of their source object. So if Potato|1|1|1| was sliced, it would result in multiple slices Potato|1|1|1|Slice\_1, Potato|1|1|1|Slice\_2, etc.

Some objects can also be Inherited if they are intrinsically a part of another object. An example of this would be every Sink object has a SinkBasin object within it. They inherit objectIds from their “parent” object similar to inherited objects that result from actions (i.e., Sink|1|2|3| would contain a SinkBasin sim object called Sink|1|2|3|SinkBasin). This is to differentiate interacting with the Sink or the interior basin of the sink, as sometimes objects want to be placed on the edge/surface of a Sink instead of the actual basin.

Note that the below table lists the Action used and original object type that results in the Inherited object type if the Inherited type is dependant on an action: PotatoSliced results from Slice(Potato). Other Object Types, like the before mentioned SinkBasin, do not require an action are are listed with just their source object that they are a part of: Bathtubs contain a BathtubBasin.

Some objects are able to contextually affect the state or behavior of other objects. For example, turning on a Microwave with a Potato object in it will cause the Potato’s metadata to automatically change the members isCooked to True and ObjectTemperature to Hot. Additionally, some objects might have certain restricted interactions with others. ToiletPaperHanger objects, which are receptacles, can only have ToiletPaper objects placed in them for example.

Navigated to Assessing Object Types