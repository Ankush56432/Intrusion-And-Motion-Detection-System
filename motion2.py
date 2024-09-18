import os

# Paths to the files
weights_path = "C:/open cv python/yolo/yolov3-tiny.weights"
config_path = "C:/open cv python/yolo/yolov3-tiny.cfg"
names_path = "C:/open cv python/yolo/coco.names"

# Check if files exist
if not os.path.exists(weights_path):
    print(f"Weights file not found: {weights_path}")
else:
    print(f"Weights file found: {weights_path}")

if not os.path.exists(config_path):
    print(f"Config file not found: {config_path}")
else:
    print(f"Config file found: {config_path}")

if not os.path.exists(names_path):
    print(f"Names file not found: {names_path}")
else:
    print(f"Names file found: {names_path}")
