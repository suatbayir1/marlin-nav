---
title: "AI2-THOR"
source: "https://ai2thor.allenai.org/ithor/documentation/scenes"
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

There are 120 scenes in iTHOR, evenly spread across kitchens, living rooms, bedrooms, and bathrooms. The list of scenes is defined as:

```python
kitchens = [f"FloorPlan{i}" for i in range(1, 31)]
living_rooms = [f"FloorPlan{200 + i}" for i in range(1, 31)]
bedrooms = [f"FloorPlan{300 + i}" for i in range(1, 31)]
bathrooms = [f"FloorPlan{400 + i}" for i in range(1, 31)]

scenes = kitchens + living_rooms + bedrooms + bathrooms
```

```
["FloorPlan1", "FloorPlan2", "FloorPlan3", {...}, "FloorPlan430"]
```

Remark

Explore the scenes in the [demo](https://ai2thor.allenai.org/demo)!

## [Scene Utility](https://ai2thor.allenai.org/ithor/documentation/scenes/#scene-utility)

We provide a cached alias to the above definitions using the

ithor\_scenes

method:

```python
controller.ithor_scenes(
    include_kitchens=True,
    include_living_rooms=True,
    include_bedrooms=True,
    include_bathrooms=True
)
```

```
[
    "FloorPlan1",
    "FloorPlan2",
    {...},
    "FloorPlan201",
    {...},
    "FloorPlan301",
    {...},
    "FloorPlan430",
]
```

### Parameters#### [include\_kitchens](https://ai2thor.allenai.org/ithor/documentation/scenes/#ithor-scenes-include_kitchens)

[: bool = True](https://ai2thor.allenai.org/ithor/documentation/scenes/#ithor-scenes-include_kitchens)

Includes the 30 kitchens (i.e., FloorPlan\[1:30\]) in the returned list when True.#### [include\_living\_rooms](https://ai2thor.allenai.org/ithor/documentation/scenes/#ithor-scenes-include_living_rooms)

[: bool = True](https://ai2thor.allenai.org/ithor/documentation/scenes/#ithor-scenes-include_living_rooms)

Includes the 30 living rooms (i.e., FloorPlan\[201:230\]) in the returned list when

True

.#### [include\_bedrooms](https://ai2thor.allenai.org/ithor/documentation/scenes/#ithor-scenes-include_bedrooms)

[: bool = True](https://ai2thor.allenai.org/ithor/documentation/scenes/#ithor-scenes-include_bedrooms)

Includes the 30 bedrooms (i.e., FloorPlan\[301:330\]) in list when

True#### [include\_bathrooms](https://ai2thor.allenai.org/ithor/documentation/scenes/#ithor-scenes-include_bathrooms)

[: bool = True](https://ai2thor.allenai.org/ithor/documentation/scenes/#ithor-scenes-include_bathrooms)

Includes the 30 bathrooms (i.e., FloorPlan\[401:430\]) in list when

True

.

## [Train/Val/Test Splits](https://ai2thor.allenai.org/ithor/documentation/scenes/#trainvaltest-splits)

It is common to train agents on a subset of scenes, in order to validate and test how well they generalize to new scenes and environments. For each room type, it is standard practice to treat the first $20$ scenes as training scenes, the next $5$ scenes as validation scenes, and the last $5$ scenes as testing scenes.

Navigated to Scene Distribution