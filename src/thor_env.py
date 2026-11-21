"""AI2-THOR ortamı için paylaşılan başlatma ve yardımcı fonksiyonlar."""

import tkinter as tk
from typing import Tuple

from ai2thor.controller import Controller

SCENE = "FloorPlan1"
WINDOW_NAME = f"AI2-THOR — {SCENE}"
DEFAULT_WIDTH = 1024
DEFAULT_HEIGHT = 768


def get_screen_resolution() -> Tuple[int, int]:
    try:
        root = tk.Tk()
        root.withdraw()
        width = root.winfo_screenwidth()
        height = root.winfo_screenheight()
        root.destroy()
        return width, height
    except Exception:
        return DEFAULT_WIDTH, DEFAULT_HEIGHT


def create_controller(
    width: int = DEFAULT_WIDTH,
    height: int = DEFAULT_HEIGHT,
    scene: str = SCENE,
) -> Controller:
    """Wiki/raw initialization kurallarına uygun Controller oluşturur.
    
    macOS üzerinde çift pencere ve ekran taşması sorununu önlemek için
    varsayılan olarak dengeli bir pencere çözünürlüğü (1024x768) kullanılır.
    """
    return Controller(
        agentMode="default",
        visibilityDistance=1.5,
        scene=scene,
        gridSize=0.25,
        snapToGrid=True,
        rotateStepDegrees=90,
        renderDepthImage=False,
        renderInstanceSegmentation=False,
        width=width,
        height=height,
        fieldOfView=90,
    )


def verify_agent_position(controller: Controller) -> bool:
    metadata = controller.last_event.metadata
    agent = metadata.get("agent")
    if not agent or "position" not in agent:
        return False
    position = agent["position"]
    if not all(key in position for key in ("x", "y", "z")):
        return False
    return metadata.get("sceneName") == SCENE

