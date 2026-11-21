import ai2thor.controller
from tqdm import tqdm

controller = ai2thor.controller.Controller()

controller.reset(
    width=1500,
    height=1500,
    renderDepthImage=False,
    renderNormalsImage=False,
    renderInstanceSegmentation=False,
    renderSemanticSegmentation=False
)

frames = []

rotate = 90
degrees = 5
for _ in tqdm(range(rotate // degrees)):
  controller.step(action="RotateLeft", degrees=degrees)
  frames.append(controller.last_event.frame)