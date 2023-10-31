from ultralytics import YOLO

model = YOLO("/home/aspagteq/Downloads/ultimate.pt")

model.export(format="openvino", imgsz=224, half=True)