---
title: "AI2-THOR"
source: "https://ai2thor.allenai.org/ithor/documentation"
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

iTHOR comes packaged with AI2-THOR, which can be installed in Python using pip:

```bash
pip install ai2thor
```

or conda:

```bash
conda install -c conda-forge ai2thor
```

Optionally, one may also choose to install AI2-THOR from an exact [Git commit](https://github.com/allenai/ai2thor/commits/main). Here, we can pass in the commit id to:

```bash
pip install --extra-index-url https://ai2thor-pypi.allenai.org ai2thor==0+COMMIT_ID
```

For example, we may have:

```bash
# Example commit id: d74c4a9bf9ec558f27d4bd1779d5e33983b99db0
pip install --extra-index-url https://ai2thor-pypi.allenai.org ai2thor==0+d74c4a9bf9ec558f27d4bd1779d5e33983b99db0
```

To verify that your setup is correct, try initializing a

Controller

and executing an action:

```python
from ai2thor.controller import Controller
controller = Controller()
event = controller.step("MoveAhead")
```

The first time a

Controller

is initialized, the game environment containing the 3D scenes will be locally downloaded to

~/.ai2thor

. The size of the download is approximately 500MB.

By default AI2-THOR currently opens up a Unity window each time a

Controller

is initialized. However, AI applications often do not need a window that renders the on-screen view and administrators of compute clusters might restrict the use of Xorg on the machines due to security concerns and the large number of dependencies that make the updates inconvenient.

Therefore, we have been worked with Unity to enable headless (off-screen) rendering of AI2-THOR. Headless mode can be enabled by setting the

platform

to

CloudRendering

upon initialization:

```python
from ai2thor.controller import Controller
from ai2thor.platform import CloudRendering
controller = Controller(platform=CloudRendering)
```

To get started with AI2-THOR, you may find it useful to use [AI2-THOR Colab](https://github.com/allenai/ai2thor-colab). It enables you to run AI2-THOR on Google Cloud for free in a browser, without any setup on your local device!

Remark

By default, AI2-THOR does not work out of the box with Google Colab, as it requires the use of Xorg for AI2-THOR to work.

For users that prefer Docker, we provide [AI2-THOR Docker](https://github.com/allenai/ai2thor-docker) as a mini-framework to simplify the setup.

Navigated to Installation