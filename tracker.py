
from ultralytics import YOLO


class SentinelTracker:

    def __init__(
        self,
        model_path="yolo11n.pt",
        confidence=0.40,
        tracker_config="bytetrack.yaml"
    ):
        self.model = YOLO(model_path)
        self.confidence = confidence
        self.tracker_config = tracker_config

    def track(self, frame):
        results = self.model.track(
            source=frame,
            persist=True,
            tracker=self.tracker_config,
            conf=self.confidence,
            verbose=False
        )

        return results[0]
