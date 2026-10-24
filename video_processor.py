
import cv2
import os
import subprocess

from detector import SentinelDetector
from tracker import SentinelTracker
from events import SentinelEventEngine
from database import SentinelDatabase


class SentinelVideoProcessor:

    def __init__(
        self,
        input_video,
        output_video=None,
        confidence=0.40,
        restricted_zone=None
    ):
        self.input_video = input_video

        self.output_video = output_video or (
            "/content/sentinel/output/sentinel_result.mp4"
        )

        self.detector = SentinelDetector(confidence=confidence)
        self.tracker = SentinelTracker(confidence=confidence)

        self.events = SentinelEventEngine(
            restricted_zone=restricted_zone
        )

        self.database = SentinelDatabase()

    def process(self):

        cap = cv2.VideoCapture(self.input_video)

        if not cap.isOpened():
            raise RuntimeError(
                f"Cannot open video: {self.input_video}"
            )

        fps = cap.get(cv2.CAP_PROP_FPS) or 30
        width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

        os.makedirs(
            os.path.dirname(self.output_video),
            exist_ok=True
        )

        # Temporary OpenCV output
        temp_output = self.output_video.replace(
            ".mp4", "_temp.mp4"
        )

        writer = cv2.VideoWriter(
            temp_output,
            cv2.VideoWriter_fourcc(*"mp4v"),
            fps,
            (width, height)
        )

        frame_number = 0

        print("=" * 50)
        print("SENTINEL PROCESSING")
        print("=" * 50)
        print("Input :", self.input_video)
        print("Output:", self.output_video)

        while True:

            success, frame = cap.read()

            if not success:
                break

            frame_number += 1
            timestamp = frame_number / fps

            result = self.tracker.track(frame)

            objects = []

            if result.boxes is not None:

                boxes = result.boxes

                for i in range(len(boxes)):

                    cls = int(boxes.cls[i].item())
                    conf = float(boxes.conf[i].item())

                    track_id = None

                    if boxes.id is not None:
                        track_id = int(boxes.id[i].item())

                    x1, y1, x2, y2 = boxes.xyxy[i].tolist()

                    center = (
                        int((x1 + x2) / 2),
                        int((y1 + y2) / 2)
                    )

                    objects.append({
                        "class_id": cls,
                        "confidence": conf,
                        "track_id": track_id,
                        "center": center,
                        "bbox": (
                            int(x1),
                            int(y1),
                            int(x2),
                            int(y2)
                        )
                    })

            incidents_before = len(self.events.incidents)

            self.events.process(
                objects,
                frame_number,
                timestamp
            )

            new_incidents = self.events.incidents[
                incidents_before:
            ]

            for incident in new_incidents:

                self.database.insert(incident)

                print(
                    f"🚨 {incident['Event']} | "
                    f"{incident['Timestamp_seconds']}s | "
                    f"{incident['Severity']}"
                )

            # YOLO boxes + tracking IDs
            annotated = result.plot()

            writer.write(annotated)

        cap.release()
        writer.release()

        # Convert automatically to browser-compatible H.264
        print("\nConverting output to H.264...")

        command = [
            "ffmpeg",
            "-y",
            "-i", temp_output,
            "-c:v", "libx264",
            "-pix_fmt", "yuv420p",
            "-movflags", "+faststart",
            "-an",
            self.output_video
        ]

        result = subprocess.run(
            command,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )

        if result.returncode != 0:
            raise RuntimeError(
                "FFmpeg conversion failed:\n" +
                result.stderr[-2000:]
            )

        os.remove(temp_output)

        print("=" * 50)
        print("✅ PROCESSING COMPLETE")
        print("Frames:", frame_number)
        print("Incidents:", len(self.events.incidents))
        print("Result:", self.output_video)
        print("=" * 50)

        return self.events.incidents
