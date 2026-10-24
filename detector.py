
from ultralytics import YOLO


class SentinelDetector:

    def __init__(self, model_path="yolo11n.pt", confidence=0.40):
        self.model = YOLO(model_path)
        self.confidence = confidence

    def detect(self, frame):
        results = self.model.predict(
            source=frame,
            conf=self.confidence,
            verbose=False
        )

        return results[0]
