import cv2
import os
import subprocess

from tracker import SentinelTracker
from events import SentinelEventEngine
from database import SentinelDatabase


class SentinelVideoProcessor:

    def __init__(
        self,
        input_video,
        output_video="/content/sentinel/output/sentinel_result.mp4",
        camera_name="Camera",
        restricted_zone=None
    ):

        self.input_video = input_video
        self.output_video = output_video
        self.camera_name = camera_name
        self.restricted_zone = restricted_zone

        os.makedirs(
            os.path.dirname(self.output_video),
            exist_ok=True
        )

        self.tracker = SentinelTracker()

        self.events = SentinelEventEngine(
            camera_name=self.camera_name,
            restricted_zone=self.restricted_zone
        )

        self.database = SentinelDatabase()

    def process(self):

        cap = cv2.VideoCapture(self.input_video)

        if not cap.isOpened():
            raise RuntimeError(
                f"Unable to open video: {self.input_video}"
            )

        fps = cap.get(cv2.CAP_PROP_FPS)

        if fps <= 0:
            fps = 30

        width = int(
            cap.get(cv2.CAP_PROP_FRAME_WIDTH)
        )

        height = int(
            cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
        )

        frame_count = int(
            cap.get(cv2.CAP_PROP_FRAME_COUNT)
        )

        # Temporary output
        temp_output = (
            self.output_video +
            ".temp.mp4"
        )

        fourcc = cv2.VideoWriter_fourcc(
            *"mp4v"
        )

        writer = cv2.VideoWriter(
            temp_output,
            fourcc,
            fps,
            (width, height)
        )

        frame_number = 0

        print("\nSENTINEL PROCESSING")
        print("-------------------")
        print("Input:", self.input_video)
        print("Frames:", frame_count)
        print("FPS:", fps)
        print("Resolution:", width, "x", height)

        while True:

            ret, frame = cap.read()

            if not ret:
                break

            frame_number += 1

            # -----------------------------
            # YOLO + BYTE TRACK
            # -----------------------------
            result = self.tracker.track(frame)

            objects = []

            if result.boxes is not None:

                boxes = result.boxes

                xyxy = boxes.xyxy.cpu().numpy()

                classes = boxes.cls.cpu().numpy()

                track_ids = (
                    boxes.id.cpu().numpy()
                    if boxes.id is not None
                    else [None] * len(xyxy)
                )

                for box, class_id, track_id in zip(
                    xyxy,
                    classes,
                    track_ids
                ):

                    x1, y1, x2, y2 = box

                    center = (
                        int((x1 + x2) / 2),
                        int((y1 + y2) / 2)
                    )

                    objects.append({
                        "class_id": int(class_id),
                        "track_id": (
                            int(track_id)
                            if track_id is not None
                            else None
                        ),
                        "center": center
                    })

            # -----------------------------
            # EVENT ENGINE
            # -----------------------------
            timestamp = frame_number / fps

            incidents = self.events.process(
                objects,
                frame_number,
                timestamp
            )

            # -----------------------------
            # DATABASE
            # -----------------------------
            if incidents:

                latest = incidents[-1]

                # Insert only if this incident
                # hasn't already been stored.
                self.database.insert(latest)

            # -----------------------------
            # ANNOTATED FRAME
            # -----------------------------
            annotated = result.plot()

            # Draw restricted zone
            if self.restricted_zone:

                x1, y1, x2, y2 = (
                    self.restricted_zone
                )

                cv2.rectangle(
                    annotated,
                    (x1, y1),
                    (x2, y2),
                    (0, 0, 255),
                    2
                )

                cv2.putText(
                    annotated,
                    "RESTRICTED AREA",
                    (x1, max(30, y1 - 10)),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.7,
                    (0, 0, 255),
                    2
                )

            writer.write(annotated)

            # Progress
            if frame_number % 100 == 0:

                print(
                    f"Processed {frame_number}/"
                    f"{frame_count}"
                )

        cap.release()
        writer.release()

        print("\nOpenCV processing complete.")

        # -----------------------------
        # AUTOMATIC H.264 CONVERSION
        # -----------------------------
        print("Converting output to H.264...")

        command = [
            "ffmpeg",
            "-y",
            "-i",
            temp_output,
            "-c:v",
            "libx264",
            "-pix_fmt",
            "yuv420p",
            "-movflags",
            "+faststart",
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

            print(
                "WARNING: H.264 conversion failed."
            )

            print(result.stderr)

            # Fall back to temporary output
            os.replace(
                temp_output,
                self.output_video
            )

        else:

            if os.path.exists(temp_output):
                os.remove(temp_output)

            print(
                "H.264 conversion complete."
            )

        print(
            "\nOutput:",
            self.output_video
        )

        print(
            "Incidents:",
            len(self.events.incidents)
        )

        return self.events.incidents
